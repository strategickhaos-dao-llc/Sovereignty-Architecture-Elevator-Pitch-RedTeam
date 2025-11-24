// StrategicKhaos PID-RANCO v1.2 Trading Bot
// "Mythic Love Layer + Deterministic Kill-Switch Core"
// 
// This is a reference implementation showing how to integrate
// the failure matrix invariants into an actual cAlgo trading bot.

using System;
using cAlgo.API;
using cAlgo.API.Indicators;
using cAlgo.API.Internals;

namespace cAlgo.Robots
{
    [Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.None)]
    public class PIDRancoBot : Robot
    {
        #region Parameters
        
        [Parameter("Sim Only (No Real Trades)", DefaultValue = true)]
        public bool SimOnly { get; set; }
        
        [Parameter("Risk Percentage", DefaultValue = 0.69, MinValue = 0.01, MaxValue = 5.0)]
        public double RiskPercentage { get; set; }
        
        [Parameter("Max Drawdown", DefaultValue = 3.37, MinValue = 1.0, MaxValue = 50.0)]
        public double MaxDrawdownPercentage { get; set; }
        
        [Parameter("EMA Fast Period", DefaultValue = 12)]
        public int EmaFastPeriod { get; set; }
        
        [Parameter("EMA Slow Period", DefaultValue = 26)]
        public int EmaSlowPeriod { get; set; }
        
        [Parameter("RSI Period", DefaultValue = 14)]
        public int RsiPeriod { get; set; }
        
        [Parameter("Stop Loss (pips)", DefaultValue = 20)]
        public int StopLossPips { get; set; }
        
        [Parameter("Take Profit (pips)", DefaultValue = 40)]
        public int TakeProfitPips { get; set; }
        
        [Parameter("Enable Voice Features", DefaultValue = false)]
        public bool EnableVoice { get; set; }
        
        [Parameter("Enable Hug Protocol (99 Losses)", DefaultValue = true)]
        public bool EnableHugProtocol { get; set; }
        
        #endregion
        
        #region Private Fields
        
        private ExponentialMovingAverage _emaFast;
        private ExponentialMovingAverage _emaSlow;
        private RelativeStrengthIndex _rsi;
        
        private double _peakEquity;
        private double _maxDrawdown;
        private bool _tradingStopped;
        
        private int _sessionLossCount;
        private bool _hugProtocolTriggered;
        
        #endregion
        
        #region Lifecycle Methods
        
        protected override void OnStart()
        {
            PrintBanner();
            LogModeStatus();
            
            // Initialize indicators
            _emaFast = Indicators.ExponentialMovingAverage(Bars.ClosePrices, EmaFastPeriod);
            _emaSlow = Indicators.ExponentialMovingAverage(Bars.ClosePrices, EmaSlowPeriod);
            _rsi = Indicators.RelativeStrengthIndex(Bars.ClosePrices, RsiPeriod);
            
            // Initialize risk management
            _peakEquity = Account.Equity;
            _maxDrawdown = MaxDrawdownPercentage / 100.0;
            _tradingStopped = false;
            
            // Initialize state machine
            _sessionLossCount = 0;
            _hugProtocolTriggered = false;
            
            Print($"[INIT] Bot started successfully");
            Print($"[INIT] SimOnly = {SimOnly}");
            Print($"[INIT] Risk = {RiskPercentage}%, Max DD = {MaxDrawdownPercentage}%");
        }
        
        protected override void OnBar()
        {
            // Critical: Check all invariants FIRST
            if (!AssertInvariants())
            {
                // Invariant violation triggers panic mode
                return;
            }
            
            // Check if trading is stopped
            if (_tradingStopped)
            {
                return;
            }
            
            // Check warmup period (F-001)
            int minBars = Math.Max(EmaSlowPeriod, RsiPeriod) + 1;
            if (Bars.Count < minBars)
            {
                // Not enough bars for indicators
                return;
            }
            
            // Update peak equity for drawdown tracking
            if (Account.Equity > _peakEquity)
            {
                _peakEquity = Account.Equity;
            }
            
            // Check drawdown limit (F-019)
            double currentDrawdown = 1.0 - (Account.Equity / _peakEquity);
            if (currentDrawdown > _maxDrawdown)
            {
                HardPanic($"[F-019] Drawdown {currentDrawdown:P2} exceeds limit {_maxDrawdown:P2}");
                return;
            }
            
            // Get voice volume (with safe fallback)
            double voiceVolume = GetSafeVoiceVolume();
            
            // Trading logic (simplified example)
            if (ShouldEnterLong())
            {
                ExecuteTrade(TradeType.Buy, "LONG", voiceVolume);
            }
            else if (ShouldEnterShort())
            {
                ExecuteTrade(TradeType.Sell, "SHORT", voiceVolume);
            }
        }
        
        protected override void OnStop()
        {
            Print($"[STOP] Bot stopped. Session loss count: {_sessionLossCount}");
            Print($"[STOP] Final equity: {Account.Equity:F2}, Peak: {_peakEquity:F2}");
        }
        
        #endregion
        
        #region Invariant Checks
        
        /// <summary>
        /// Assert all critical invariants. Returns false if any invariant is violated.
        /// This is the "kill-switch" layer that prevents trading with bad data.
        /// </summary>
        private bool AssertInvariants()
        {
            // Invariant 1: Account data must be valid (F-005, F-020)
            if (Account == null)
            {
                HardPanic("[F-005] Account object is null");
                return false;
            }
            
            if (double.IsNaN(Account.Equity) || double.IsInfinity(Account.Equity))
            {
                HardPanic("[F-020] Account.Equity is NaN or Infinity");
                return false;
            }
            
            if (Account.Equity <= 0)
            {
                HardPanic("[F-020] Account.Equity is zero or negative");
                return false;
            }
            
            // Invariant 2: Symbol data must be valid (F-004, F-018)
            if (Symbol == null)
            {
                HardPanic("[F-004] Symbol object is null");
                return false;
            }
            
            if (Symbol.TickValue <= 0 || double.IsNaN(Symbol.TickValue) || double.IsInfinity(Symbol.TickValue))
            {
                HardPanic("[F-018] Symbol.TickValue is invalid");
                return false;
            }
            
            // Invariant 3: Indicator data must be valid (F-016, F-017)
            if (_emaFast != null && _emaFast.Result.Count > 0)
            {
                double lastEmaFast = _emaFast.Result.LastValue;
                if (double.IsNaN(lastEmaFast) || double.IsInfinity(lastEmaFast))
                {
                    Print("[F-016] EMA Fast contains NaN/Infinity — skipping bar");
                    return false;
                }
            }
            
            if (_emaSlow != null && _emaSlow.Result.Count > 0)
            {
                double lastEmaSlow = _emaSlow.Result.LastValue;
                if (double.IsNaN(lastEmaSlow) || double.IsInfinity(lastEmaSlow))
                {
                    Print("[F-016] EMA Slow contains NaN/Infinity — skipping bar");
                    return false;
                }
            }
            
            if (_rsi != null && _rsi.Result.Count > 0)
            {
                double lastRsi = _rsi.Result.LastValue;
                if (double.IsNaN(lastRsi) || double.IsInfinity(lastRsi))
                {
                    Print("[F-017] RSI contains NaN/Infinity — skipping bar");
                    return false;
                }
            }
            
            // Invariant 4: SimOnly mode must never have real positions (critical!)
            if (SimOnly && Positions.Count > 0)
            {
                Print("[CRITICAL] SimOnly mode but real positions exist!");
                Print("[CRITICAL] This should NEVER happen. Verify account mode.");
                // Note: We can't close positions that shouldn't exist in sim mode
                // This indicates a configuration error
            }
            
            // Invariant 5: Network connectivity (F-010)
            if (!IsConnected)
            {
                HardPanic("[F-010] Network disconnection detected");
                return false;
            }
            
            return true;
        }
        
        #endregion
        
        #region Trading Logic
        
        private bool ShouldEnterLong()
        {
            if (Positions.Count > 0)
                return false;
            
            // Simple crossover strategy (example)
            if (_emaFast.Result.LastValue > _emaSlow.Result.LastValue &&
                _rsi.Result.LastValue < 70)
            {
                return true;
            }
            
            return false;
        }
        
        private bool ShouldEnterShort()
        {
            if (Positions.Count > 0)
                return false;
            
            // Simple crossover strategy (example)
            if (_emaFast.Result.LastValue < _emaSlow.Result.LastValue &&
                _rsi.Result.LastValue > 30)
            {
                return true;
            }
            
            return false;
        }
        
        private void ExecuteTrade(TradeType tradeType, string label, double voiceVolume)
        {
            // Calculate position size with safety checks
            double riskAmount = Account.Equity * (RiskPercentage / 100.0);
            
            // Check for F-011: Risk amount calculates to zero
            if (riskAmount <= 0)
            {
                Print("[F-011] Risk amount is zero or negative — skipping trade");
                return;
            }
            
            // Calculate quantity based on risk and stop loss
            double stopLossValue = Symbol.PipValue * StopLossPips;
            long quantity = Symbol.NormalizeVolumeInUnits(riskAmount / stopLossValue);
            
            // Check for F-012: Quantity floors to zero
            if (quantity <= 0)
            {
                Print("[F-012] Position quantity is zero — skipping trade");
                return;
            }
            
            // Route through the order placement safety layer
            PlaceOrder(tradeType, label, quantity);
        }
        
        #endregion
        
        #region Order Routing (SimOnly Safety Layer)
        
        /// <summary>
        /// Single order routing function that enforces SimOnly mode.
        /// ALL order placement MUST go through this method.
        /// </summary>
        private void PlaceOrder(TradeType tradeType, string label, long quantity)
        {
            if (quantity <= 0)
            {
                Print("[F-012] Quantity <= 0, skipping order");
                return;
            }
            
            string direction = tradeType == TradeType.Buy ? "LONG" : "SHORT";
            
            if (SimOnly)
            {
                // SIMULATION MODE - Log only, never place real orders
                Print($"[SIM] {direction} {quantity} units @ {Symbol.Bid:F5}");
                Print($"[SIM] Tag: {label}, SL: {StopLossPips} pips, TP: {TakeProfitPips} pips");
                return;
            }
            
            // LIVE MODE - Actually place the order
            Print($"[LIVE] Placing {direction} order: {quantity} units");
            
            var result = ExecuteMarketOrder(
                tradeType,
                SymbolName,
                quantity,
                label,
                StopLossPips,
                TakeProfitPips
            );
            
            if (!result.IsSuccessful)
            {
                Print($"[ERROR] Order failed: {result.Error}");
            }
        }
        
        /// <summary>
        /// Close all positions safely (respects SimOnly mode).
        /// </summary>
        private void CloseAllPositions(string reason)
        {
            Print($"[FLATTEN] Closing all positions. Reason: {reason}");
            
            foreach (var position in Positions)
            {
                if (SimOnly)
                {
                    Print($"[SIM] Would close position {position.Id} ({position.TradeType})");
                    continue;
                }
                
                var result = ClosePosition(position);
                if (!result.IsSuccessful)
                {
                    Print($"[ERROR] Failed to close position {position.Id}: {result.Error}");
                }
            }
        }
        
        #endregion
        
        #region Voice Integration (Safe Fallbacks)
        
        /// <summary>
        /// Get voice volume with all failure modes handled.
        /// Returns 0.0 if any error occurs (safe default).
        /// </summary>
        private double GetSafeVoiceVolume()
        {
            if (!EnableVoice)
            {
                return 0.0;
            }
            
            try
            {
                // This would be your actual voice capture code
                // For now, return safe default
                // double volume = VoiceCapture.GetHerVoiceVolume();
                
                double volume = 0.0; // Placeholder
                
                // Check for F-033, F-034: Invalid volume values
                if (double.IsNaN(volume) || double.IsInfinity(volume))
                {
                    Print("[F-034] Voice volume is NaN/Infinity — using 0.0");
                    return 0.0;
                }
                
                // Clamp to valid range
                if (volume < 0.0) volume = 0.0;
                if (volume > 1.0) volume = 1.0;
                
                return volume;
            }
            catch (Exception ex)
            {
                // F-031, F-032: Microphone or driver issues
                Print($"[F-031] Voice capture failed: {ex.Message} — using 0.0");
                return 0.0;
            }
        }
        
        #endregion
        
        #region State Machine (Hug Protocol & Apoptosis)
        
        private void OnPositionClosed(PositionClosedEventArgs args)
        {
            double netPnL = args.Position.NetProfit;
            
            if (netPnL < 0)
            {
                // Loss - increment counter
                _sessionLossCount++;
                Print($"[STATE] Loss #{_sessionLossCount} — P&L: {netPnL:F2}");
                
                // Check for hug protocol trigger (F-052, F-054, F-055)
                if (EnableHugProtocol && _sessionLossCount == 99 && !_hugProtocolTriggered)
                {
                    TriggerHugProtocol();
                }
            }
            else
            {
                // Win - reset counter (F-053)
                if (_sessionLossCount > 0)
                {
                    Print($"[STATE] Win after {_sessionLossCount} losses — resetting counter");
                    _sessionLossCount = 0;
                    _hugProtocolTriggered = false;
                }
            }
        }
        
        private void TriggerHugProtocol()
        {
            _hugProtocolTriggered = true;
            Print("[HUG] ═══════════════════════════════════════════");
            Print("[HUG] 99 losses detected. Hug protocol activated.");
            Print("[HUG] Trade #100 is the universe giving you one more shot.");
            Print("[HUG] ═══════════════════════════════════════════");
            
            // Optional: Could reduce risk, increase take profit, etc.
            // Or just log the moment and continue
        }
        
        #endregion
        
        #region Panic & Emergency Stop
        
        /// <summary>
        /// Emergency stop with position flattening.
        /// Called when an invariant is violated or critical error occurs.
        /// </summary>
        private void HardPanic(string reason)
        {
            Print("╔═══════════════════════════════════════════╗");
            Print($"║ [PANIC] {reason}");
            Print("║ Flattening all positions and stopping bot");
            Print("╚═══════════════════════════════════════════╝");
            
            _tradingStopped = true;
            
            // Flatten all positions
            CloseAllPositions("PANIC MODE");
            
            // Stop the bot
            Stop();
        }
        
        #endregion
        
        #region Logging & Display
        
        private void PrintBanner()
        {
            Print("╔═══════════════════════════════════════════════════════════╗");
            Print("║     StrategicKhaos PID-RANCO v1.2 Trading Engine         ║");
            Print("║     'Mythic Love Layer + Deterministic Kill-Switch'      ║");
            Print("╚═══════════════════════════════════════════════════════════╝");
        }
        
        private void LogModeStatus()
        {
            if (SimOnly)
            {
                Print("");
                Print("╔═══════════════════════════════════════════════════════════╗");
                Print("║                    SIMULATION MODE ACTIVE                 ║");
                Print("║                                                           ║");
                Print("║              NO REAL TRADES WILL BE PLACED                ║");
                Print("║                                                           ║");
                Print("║   All signals will be logged but not executed on broker  ║");
                Print("╚═══════════════════════════════════════════════════════════╝");
                Print("");
            }
            else
            {
                Print("");
                Print("╔═══════════════════════════════════════════════════════════╗");
                Print("║                    ⚠️  LIVE TRADING MODE  ⚠️               ║");
                Print("║                                                           ║");
                Print("║              REAL ORDERS WILL BE PLACED                   ║");
                Print("║                                                           ║");
                Print("║   Verify account, risk settings, and broker connection   ║");
                Print("╚═══════════════════════════════════════════════════════════╝");
                Print("");
            }
        }
        
        #endregion
    }
}
