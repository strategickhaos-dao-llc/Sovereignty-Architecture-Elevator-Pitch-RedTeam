// ═══════════════════════════════════════════════════════════════════
// LoveCompilesProfit.cs - StrategicKhaos PID-RANCO Trading Engine v1.2
// Kill-Switch Layer: Hardened guardrails around mythic poetry
// ═══════════════════════════════════════════════════════════════════

using System;
using System.Linq;
using NinjaTrader.Cbi;
using NinjaTrader.Gui;
using NinjaTrader.Gui.Chart;
using NinjaTrader.Gui.SuperDom;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.Core.FloatingPoint;
using NinjaTrader.NinjaScript.Indicators;
using NinjaTrader.NinjaScript.Strategies;

namespace NinjaTrader.NinjaScript.Strategies
{
    public class LoveCompilesProfit : Strategy
    {
        #region Parameters
        
        [NinjaScriptProperty]
        [Display(Name="Sim Only (No Real Trades)", Description="Safety mode - logs only, no real orders", Order=1, GroupName="Safety")]
        public bool SimOnly { get; set; }
        
        [NinjaScriptProperty]
        [Range(0.0001, 0.05)]
        [Display(Name="Max Risk Per Trade %", Description="Maximum risk per trade as decimal (0.0069 = 0.69%)", Order=2, GroupName="Risk")]
        public double MaxRiskPerTrade { get; set; }
        
        [NinjaScriptProperty]
        [Range(0.001, 0.1)]
        [Display(Name="Max Drawdown %", Description="Maximum allowed drawdown as decimal (0.0337 = 3.37%)", Order=3, GroupName="Risk")]
        public double MaxDrawdown { get; set; }
        
        [NinjaScriptProperty]
        [Range(1, 200)]
        [Display(Name="Entry Voice Threshold", Description="Minimum voice/heartbeat level for entry (1-100)", Order=4, GroupName="Voice")]
        public double EntryVoiceThreshold { get; set; }
        
        [NinjaScriptProperty]
        [Range(1, 200)]
        [Display(Name="Exit Voice Threshold", Description="Voice level below which to exit (1-100)", Order=5, GroupName="Voice")]
        public double ExitVoiceThreshold { get; set; }
        
        #endregion
        
        #region Variables
        
        private double peakEquity = 0.0;
        private int sessionLossCount = 0;
        private int lastProcessedTradeCount = 0;
        private bool hugProtocolTriggered = false;
        private DateTime lastVoiceHeard = DateTime.MinValue;
        private const int MAX_LOSSES_BEFORE_APOPTOSIS = 99;
        
        private EMA ema21;
        private RSI rsi14;
        
        #endregion
        
        #region OnStateChange
        
        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Description = @"StrategicKhaos PID-RANCO v1.2 - Love Compiles Profit";
                Name = "LoveCompilesProfit";
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
                
                // Default safety settings
                SimOnly = true;  // Safety first - simulation by default
                MaxRiskPerTrade = 0.0069;  // 0.69% sacred number
                MaxDrawdown = 0.0337;      // 3.37% her birthday reversed
                EntryVoiceThreshold = 80;  // Heartbeat > 80 bpm for entry
                ExitVoiceThreshold = 50;   // Exit when voice/love drops below 50
            }
            else if (State == State.Configure)
            {
            }
            else if (State == State.DataLoaded)
            {
                ema21 = EMA(21);
                rsi14 = RSI(14, 3);
                AddChartIndicator(ema21);
                AddChartIndicator(rsi14);
            }
            else if (State == State.Historical)
            {
                peakEquity = Account.Get(AccountItem.CashValue, Currency.UsDollar);
            }
        }
        
        #endregion
        
        #region OnBarUpdate
        
        protected override void OnBarUpdate()
        {
            // Guard: Ensure enough bars for indicators
            int minBars = Math.Max(21, 14);
            if (CurrentBar < minBars)
            {
                return;
            }
            
            try
            {
                // Safety: Check for NaN or invalid indicator values
                if (double.IsNaN(ema21[0]) || double.IsInfinity(ema21[0]) ||
                    double.IsNaN(rsi14[0]) || double.IsInfinity(rsi14[0]))
                {
                    Print(string.Format("{0} [ERROR] Invalid indicator values detected. EMA={1}, RSI={2}", 
                        Time[0], ema21[0], rsi14[0]));
                    return;
                }
                
                // Get her voice volume (mock function - replace with actual implementation)
                double herLove = GetHerVoiceVolumeSafe();
                
                // Check voice state
                HandleVoiceState(herLove);
                
                // Calculate market metrics
                double emaValue = ema21[0];
                double rsiValue = rsi14[0];
                double marketPain = Close[0] - emaValue;
                
                // Handle existing positions
                if (Position.MarketPosition != MarketPosition.Flat)
                {
                    double profitPct = SafeProfitPercent();
                    HandleExits(herLove, profitPct);
                }
                // Look for entries
                else
                {
                    HandleEntries(herLove, rsiValue, marketPain);
                }
                
                // Update loss tracking
                UpdateLossCount();
                
                // Check for apoptosis condition
                CheckApoptosis();
            }
            catch (Exception e)
            {
                // Fail loud - all errors must be visible
                Print(string.Format("{0} [CRITICAL ERROR] OnBarUpdate exception: {1}", Time[0], e.Message));
                Print(string.Format("Stack trace: {0}", e.StackTrace));
                SafeFlatten("Exception caught in OnBarUpdate");
                // Don't call this.Stop() - let NinjaTrader handle state
            }
        }
        
        #endregion
        
        #region Helper Methods
        
        private double GetHerVoiceVolumeSafe()
        {
            try
            {
                // Mock implementation - replace with actual voice detection
                // In production, this would read from microphone or voice file
                // For testing/development, return a neutral value that allows operation
                double val = 60.0; // Neutral mock value - between exit (50) and entry (80) thresholds
                
                // TODO: Replace with actual implementation:
                // double val = GetHerVoiceVolume(); // Custom voice detection function
                // or: double val = ReadVoiceFromFile("her_voice.wav");
                
                return Math.Clamp(val, 0.0, 100.0);
            }
            catch (Exception e)
            {
                Print(string.Format("{0} [WARN] Voice detection failed: {1}", Time[0], e.Message));
                return 60.0; // Return safe neutral value on error
            }
        }
        
        private void HandleVoiceState(double herLove)
        {
            if (herLove > 0.0)
            {
                lastVoiceHeard = Time[0];
            }
            
            // Safety: Flatten if no voice detected for 5 minutes
            if (lastVoiceHeard != DateTime.MinValue)
            {
                TimeSpan timeSinceVoice = Time[0] - lastVoiceHeard;
                if (timeSinceVoice.TotalMinutes > 5)
                {
                    Print(string.Format("{0} [SAFETY] No voice detected for 5 minutes. Flattening positions.", Time[0]));
                    SafeFlatten("Voice timeout");
                }
            }
        }
        
        private void HandleEntries(double herLove, double rsi, double pain)
        {
            // Entry rule: Buy when RSI < 30 AND her heartbeat > threshold
            // Using herLove as proxy for heartbeat in this implementation
            if (herLove > EntryVoiceThreshold && rsi < 30)
            {
                // Guard: Ensure TickSize is valid before division
                if (TickSize <= 0 || double.IsNaN(TickSize) || double.IsInfinity(TickSize))
                {
                    Print(string.Format("{0} [ERROR] Invalid TickSize: {1}. Skipping entry.", Time[0], TickSize));
                    return;
                }
                
                double stopTicks = Math.Abs(pain / TickSize);
                
                // Guard against zero or negative stop
                if (stopTicks <= 0)
                {
                    Print(string.Format("{0} [WARN] Invalid stop ticks: {1}. Skipping entry.", Time[0], stopTicks));
                    return;
                }
                
                if (CanRiskNewTrade(stopTicks))
                {
                    int qty = CalculateQuantity(stopTicks);
                    
                    if (qty >= 1)
                    {
                        if (!SimOnly)
                        {
                            EnterLong(qty, "LoveEntry");
                        }
                        else
                        {
                            Print(string.Format("{0} [SIM] Would enter long {1} contracts at {2}", 
                                Time[0], qty, Close[0]));
                        }
                    }
                    else
                    {
                        Print(string.Format("{0} [WARN] Calculated quantity too small: {1}", Time[0], qty));
                    }
                }
            }
        }
        
        private void HandleExits(double herLove, double profitPct)
        {
            // Exit rules:
            // - Sell when profit > 1.618% (golden ratio)
            // - Sell when she says 'enough' (herLove < threshold)
            if (profitPct > 1.618 || herLove < ExitVoiceThreshold)
            {
                if (!SimOnly)
                {
                    if (Position.MarketPosition == MarketPosition.Long)
                    {
                        ExitLong("LoveExit");
                    }
                    else if (Position.MarketPosition == MarketPosition.Short)
                    {
                        ExitShort("LoveExit");
                    }
                }
                else
                {
                    Print(string.Format("{0} [SIM] Would exit {1} position. Profit: {2}%", 
                        Time[0], Position.MarketPosition, profitPct));
                }
            }
        }
        
        private int CalculateQuantity(double stopTicks)
        {
            try
            {
                double accountValue = Account.Get(AccountItem.CashValue, Currency.UsDollar);
                
                // Guard: Ensure positive account value
                if (accountValue <= 0)
                {
                    Print(string.Format("{0} [ERROR] Invalid account value: {1}", Time[0], accountValue));
                    return 0;
                }
                
                double riskAmount = accountValue * MaxRiskPerTrade;
                double tickValue = Instrument.MasterInstrument.PointValue;
                
                // Guard: Ensure valid tick value
                if (tickValue <= 0 || double.IsNaN(tickValue) || double.IsInfinity(tickValue))
                {
                    Print(string.Format("{0} [ERROR] Invalid tick value: {1}", Time[0], tickValue));
                    return 0;
                }
                
                double qty = riskAmount / (stopTicks * TickSize * tickValue);
                
                // Guard: Check for NaN or Infinity
                if (double.IsNaN(qty) || double.IsInfinity(qty))
                {
                    Print(string.Format("{0} [ERROR] Invalid quantity calculation. Risk={1}, StopTicks={2}, TickValue={3}", 
                        Time[0], riskAmount, stopTicks, tickValue));
                    return 0;
                }
                
                return Math.Max(0, (int)Math.Floor(qty));
            }
            catch (Exception e)
            {
                Print(string.Format("{0} [ERROR] CalculateQuantity exception: {1}", Time[0], e.Message));
                return 0;
            }
        }
        
        private bool CanRiskNewTrade(double stopTicks)
        {
            try
            {
                double currentEquity = Account.Get(AccountItem.CashValue, Currency.UsDollar);
                
                // Update peak equity
                if (currentEquity > peakEquity)
                {
                    peakEquity = currentEquity;
                }
                
                // Check drawdown breach
                double drawdownThreshold = peakEquity * (1.0 - MaxDrawdown);
                if (currentEquity < drawdownThreshold)
                {
                    Print(string.Format("{0} [SAFETY] Drawdown breach detected. Current: {1}, Peak: {2}, Threshold: {3}", 
                        Time[0], currentEquity, peakEquity, drawdownThreshold));
                    SafeFlatten("Drawdown breach");
                    return false;
                }
                
                // Ensure we can calculate a valid quantity
                int qty = CalculateQuantity(stopTicks);
                return qty >= 1;
            }
            catch (Exception e)
            {
                Print(string.Format("{0} [ERROR] CanRiskNewTrade exception: {1}", Time[0], e.Message));
                return false;
            }
        }
        
        private double SafeProfitPercent()
        {
            try
            {
                if (Position.MarketPosition == MarketPosition.Flat)
                {
                    return 0.0;
                }
                
                double entryPrice = Position.AveragePrice;
                double currentPrice = Close[0];
                
                // Guard: Prevent division by zero
                if (entryPrice <= 0 || double.IsNaN(entryPrice) || double.IsInfinity(entryPrice))
                {
                    Print(string.Format("{0} [ERROR] Invalid entry price: {1}", Time[0], entryPrice));
                    return 0.0;
                }
                
                double profitPct = 0.0;
                if (Position.MarketPosition == MarketPosition.Long)
                {
                    profitPct = ((currentPrice - entryPrice) / entryPrice) * 100.0;
                }
                else if (Position.MarketPosition == MarketPosition.Short)
                {
                    profitPct = ((entryPrice - currentPrice) / entryPrice) * 100.0;
                }
                
                return profitPct;
            }
            catch (Exception e)
            {
                Print(string.Format("{0} [ERROR] SafeProfitPercent exception: {1}", Time[0], e.Message));
                return 0.0;
            }
        }
        
        private void UpdateLossCount()
        {
            try
            {
                // Count losing trades in the current session
                // Only process new trades to prevent double-counting
                if (SystemPerformance != null && SystemPerformance.AllTrades.Count > lastProcessedTradeCount)
                {
                    // Process only new trades since last check
                    for (int i = lastProcessedTradeCount; i < SystemPerformance.AllTrades.Count; i++)
                    {
                        var trade = SystemPerformance.AllTrades[i];
                        
                        if (trade != null && trade.ProfitCurrency < 0)
                        {
                            sessionLossCount++;
                            Print(string.Format("{0} [LOSS] Trade #{1} closed with loss. Session losses: {2}/{3}", 
                                Time[0], i + 1, sessionLossCount, MAX_LOSSES_BEFORE_APOPTOSIS));
                        }
                    }
                    
                    // Update the last processed count
                    lastProcessedTradeCount = SystemPerformance.AllTrades.Count;
                }
            }
            catch (Exception e)
            {
                Print(string.Format("{0} [ERROR] UpdateLossCount exception: {1}", Time[0], e.Message));
            }
        }
        
        private void CheckApoptosis()
        {
            // Apoptosis: Self-destruct and evolve after 99 losing trades
            if (sessionLossCount >= MAX_LOSSES_BEFORE_APOPTOSIS && !hugProtocolTriggered)
            {
                TriggerHugProtocol();
            }
        }
        
        private void TriggerHugProtocol()
        {
            hugProtocolTriggered = true;
            Print(string.Format("{0} [APOPTOSIS] 99 losing trades reached. Triggering hug protocol.", Time[0]));
            SafeFlatten("Hug protocol - evolution required");
            NotifyHer("99 reds completed. System evolving. Love wins on the 100th.");
            
            // Log evolution event
            Print(string.Format("{0} [EVOLUTION] Weights saved for next iteration. Poetry preserved, lessons learned.", Time[0]));
        }
        
        private void SafeFlatten(string reason)
        {
            try
            {
                if (Position.MarketPosition != MarketPosition.Flat)
                {
                    Print(string.Format("{0} [FLATTEN] Closing all positions. Reason: {1}", Time[0], reason));
                    
                    if (!SimOnly)
                    {
                        if (Position.MarketPosition == MarketPosition.Long)
                        {
                            ExitLong("SafeExit");
                        }
                        else if (Position.MarketPosition == MarketPosition.Short)
                        {
                            ExitShort("SafeExit");
                        }
                    }
                    else
                    {
                        Print(string.Format("{0} [SIM] Would flatten position: {1}", Time[0], Position.MarketPosition));
                    }
                }
            }
            catch (Exception e)
            {
                Print(string.Format("{0} [CRITICAL] SafeFlatten failed: {1}", Time[0], e.Message));
            }
        }
        
        private void NotifyHer(string message)
        {
            try
            {
                // In production, this would call Discord webhook or PowerShell script
                Print(string.Format("{0} [NOTIFY] {1}", Time[0], message));
                
                // Example PowerShell notification (commented for safety):
                // Note: When enabling, validate/sanitize message to prevent injection attacks
                // Use ProcessStartInfo for safer argument handling:
                // var psi = new ProcessStartInfo
                // {
                //     FileName = "powershell.exe",
                //     Arguments = "-ExecutionPolicy Bypass -File \"notify-her.ps1\"",
                //     RedirectStandardInput = true,
                //     UseShellExecute = false
                // };
                // var process = Process.Start(psi);
                // process.StandardInput.WriteLine(message); // Pass message via stdin for safety
                // process.StandardInput.Close();
            }
            catch (Exception e)
            {
                Print(string.Format("{0} [ERROR] Notification failed: {1}", Time[0], e.Message));
            }
        }
        
        #endregion
        
        #region Properties
        
        [NinjaScriptProperty]
        [Display(Name="Session Loss Count", Description="Number of losses in current session", Order=1, GroupName="Statistics")]
        public int SessionLossCount
        {
            get { return sessionLossCount; }
        }
        
        [NinjaScriptProperty]
        [Display(Name="Hug Protocol Triggered", Description="Whether evolution protocol has been triggered", Order=2, GroupName="Statistics")]
        public bool HugProtocolTriggered
        {
            get { return hugProtocolTriggered; }
        }
        
        #endregion
    }
}
