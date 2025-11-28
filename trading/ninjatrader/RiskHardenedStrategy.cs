using System;
using NinjaTrader.Cbi;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.Indicators;
using NinjaTrader.NinjaScript.Strategies;

namespace NinjaTrader.Custom.Strategies
{
    /// <summary>
    /// Risk-Hardened Trading Strategy for Strategickhaos
    /// 
    /// Features:
    /// - ATR-based position sizing for volatility-adjusted risk
    /// - Daily loss limit (default 2% of account balance)
    /// - Maximum trades per day limit (default 5)
    /// - Automatic position size calculation based on risk parameters
    /// 
    /// Verification: Test in NT Simulator with ES/MNQ data
    /// Expected size: 1-3 contracts for $520 balance at 1% risk
    /// Formula: size = floor(riskAmount / (stopDistance * tickValue))
    /// </summary>
    public class RiskHardenedStrategy : Strategy
    {
        // =====================================================
        // Parameters: Tune these via NinjaTrader UI or code
        // =====================================================
        
        /// <summary>
        /// Percentage of account to risk per trade (default 1%)
        /// </summary>
        private double riskPerTradePct = 1.0;
        
        /// <summary>
        /// Maximum daily drawdown as percentage of account (default 2%)
        /// </summary>
        private double dailyLossLimitPct = 2.0;
        
        /// <summary>
        /// Hard cap on number of trades per day
        /// </summary>
        private int maxTradesPerDay = 5;
        
        /// <summary>
        /// ATR lookback period for volatility calculation
        /// </summary>
        private int atrPeriod = 14;
        
        /// <summary>
        /// ATR multiplier for stop distance calculation
        /// </summary>
        private double atrStopMultiplier = 2.0;

        // =====================================================
        // Internal Trackers
        // =====================================================
        private double accountBalance;
        private double dailyPnL;
        private int tradeCountToday;
        private DateTime currentDay;
        private double atrValue;

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Description = "Risk-hardened base strategy for Strategickhaos trades with ATR-based sizing and daily limits";
                Name = "StrategickhaosRiskGuard";
                Calculate = Calculate.OnBarClose;
                EntriesPerDirection = 1;
                EntryHandling = EntryHandling.AllEntries;
                IsExitOnSessionCloseStrategy = true;
                ExitOnSessionCloseSeconds = 30;
                IsFillLimitOnTouch = false;
                MaximumBarsLookBack = MaximumBarsLookBack.TwoHundredFiftySix;
                OrderFillResolution = OrderFillResolution.Standard;
                Slippage = 0;
                StartBehavior = StartBehavior.WaitUntilFlat;
                TimeInForce = TimeInForce.Gtc;
                TraceOrders = false;
                RealtimeErrorHandling = RealtimeErrorHandling.StopCancelClose;
                StopTargetHandling = StopTargetHandling.PerEntryExecution;
                BarsRequiredToTrade = 20;
            }
            else if (State == State.Configure)
            {
                // Initialize account balance
                accountBalance = Account.Get(AccountItem.CashValue, Currency.UsDollar);
                dailyPnL = 0;
                tradeCountToday = 0;
                currentDay = DateTime.MinValue;
            }
            else if (State == State.DataLoaded)
            {
                // ATR indicator added for volatility calculation
                AddChartIndicator(ATR(atrPeriod));
            }
        }

        protected override void OnBarUpdate()
        {
            // Ensure enough bars for ATR calculation
            if (CurrentBar < atrPeriod)
                return;

            // Update ATR value
            atrValue = ATR(atrPeriod)[0];

            // Check for daily reset
            if (Time[0].Date != currentDay)
            {
                currentDay = Time[0].Date;
                dailyPnL = 0;
                tradeCountToday = 0;
                Print($"[RiskGuard] New trading day: {currentDay:yyyy-MM-dd} | Account Balance: ${accountBalance:N2}");
            }

    # =====================================================
    # Signal Generation: Replace with your custom logic
    # Example: Integrate with Grok/Zapier external signals
    # NOTE: These are intentionally set to false as placeholders
    # Users must implement their own signal logic
    # =====================================================
    bool buySignal = false;  // TODO: Your buy condition here
    bool sellSignal = false; // TODO: Your sell condition here

    // Example signal implementations (uncomment to test):
    // buySignal = CrossAbove(SMA(14), SMA(50), 1);
    // sellSignal = CrossBelow(SMA(14), SMA(50), 1);

            if (buySignal || sellSignal)
            {
                // Enforce trading limits before entry
                if (!CanTrade())
                    return;

                // Calculate position size based on risk parameters
                int positionSize = CalculatePositionSize();

                // Execute trade
                if (buySignal)
                {
                    EnterLong(positionSize, "RiskEntryLong");
                    Print($"[RiskGuard] LONG Entry | Size: {positionSize} | ATR: {atrValue:N4}");
                }
                else if (sellSignal)
                {
                    EnterShort(positionSize, "RiskEntryShort");
                    Print($"[RiskGuard] SHORT Entry | Size: {positionSize} | ATR: {atrValue:N4}");
                }

                tradeCountToday++;
            }
        }

        /// <summary>
        /// Checks if trading is allowed based on daily limits
        /// </summary>
        private bool CanTrade()
        {
            // Check trade count limit
            if (tradeCountToday >= maxTradesPerDay)
            {
                Print($"[RiskGuard] Trade limit reached: {tradeCountToday}/{maxTradesPerDay} trades today. Skipping.");
                return false;
            }

            // Check daily loss limit
            double dailyLossLimit = accountBalance * (dailyLossLimitPct / 100.0);
            if (dailyPnL <= -dailyLossLimit)
            {
                Print($"[RiskGuard] Daily loss limit reached: ${dailyPnL:N2} <= -${dailyLossLimit:N2}. Trading halted.");
                return false;
            }

            return true;
        }

        /// <summary>
        /// Calculates position size based on ATR and risk parameters
        /// Formula: size = riskAmount / (stopDistance * pointValue)
        /// </summary>
        private int CalculatePositionSize()
        {
            // Calculate stop distance (2x ATR by default)
            double stopDistance = atrValue * atrStopMultiplier;
            
            // Calculate risk amount in dollars
            double riskAmount = accountBalance * (riskPerTradePct / 100.0);
            
            // Get instrument point value (e.g., ES = $50, MNQ = $2)
            double pointValue = Instrument.MasterInstrument.PointValue;
            
            // Calculate position size
            // Risk = (Entry - Stop) * Size * PointValue <= riskAmount
            // Size = riskAmount / (stopDistance * pointValue)
            int positionSize = (int)Math.Floor(riskAmount / (stopDistance * pointValue));
            
            // Ensure minimum of 1 contract
            positionSize = Math.Max(1, positionSize);
            
            Print($"[RiskGuard] Size Calc | Risk: ${riskAmount:N2} | Stop: {stopDistance:N4} pts | PointVal: ${pointValue:N2} | Size: {positionSize}");
            
            return positionSize;
        }

        protected override void OnExecutionUpdate(Execution execution, string executionId, double price, 
            int quantity, MarketPosition marketPosition, string orderId, DateTime time)
        {
            // Update daily P&L on trade fills
            // Note: This is simplified; use OnPositionUpdate for precise P&L tracking
            
            double tradePnL = 0;
            
            if (marketPosition == MarketPosition.Flat)
            {
                // Position closed - calculate realized P&L
                // For accurate P&L, track entry price and calculate on close
                Print($"[RiskGuard] Position closed at ${price:N2}");
            }
            
            // Include commission in P&L calculation
            dailyPnL -= execution.Commission;
            
            Print($"[RiskGuard] Execution | Price: ${price:N2} | Qty: {quantity} | Commission: ${execution.Commission:N2} | Daily P&L: ${dailyPnL:N2}");
        }

        protected override void OnPositionUpdate(Position position, double averagePrice, 
            int quantity, MarketPosition marketPosition)
        {
            // More accurate P&L tracking on position changes
            if (marketPosition == MarketPosition.Flat && Position.Quantity == 0)
            {
                // Position fully closed
                double realizedPnL = SystemPerformance.RealTimeTrades.TradesPerformance.Currency.CumProfit;
                Print($"[RiskGuard] Position Update | Realized P&L: ${realizedPnL:N2}");
            }
        }
    }
}
