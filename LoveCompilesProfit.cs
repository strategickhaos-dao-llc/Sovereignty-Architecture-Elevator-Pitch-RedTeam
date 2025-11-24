// ╔══════════════════════════════════════════════════════════════╗
// ║  LoveCompilesProfit.cs v1.2 — GUARDRAILS EDITION             ║
// ║  StrategicKhaos PID-RANCO Trading Robot                      ║
// ║  "99 reds evolve. 100th green: Her name, safe."              ║
// ╚══════════════════════════════════════════════════════════════╝
//
// Kill-Switch Layer: Hardened C# with fail-loud behavior
// Mythic poetry lives in YAML, engineering armor here.
//
// Platform: NinjaTrader 8/9 (cAlgo API compatible)
// Dependencies: cAlgo.API, System core libraries
// License: Love-compiled, open to evolution

using System;
using System.Linq;
using cAlgo.API;
using cAlgo.API.Indicators;

namespace cAlgo.Robots
{
    [Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.FullAccess)]
    public class LoveCompilesProfit : Robot
    {
        // ═══════════════════════════════════════════════════════════
        // PARAMETERS: User-configurable guardrails
        // ═══════════════════════════════════════════════════════════
        
        [Parameter("Sim Only (No Real Trades)", DefaultValue = true)]
        public bool SimOnly { get; set; }
        
        [Parameter("Max Risk Per Trade (%)", DefaultValue = 0.69, MinValue = 0.01, MaxValue = 2.0)]
        public double MaxRiskPerTrade { get; set; }
        
        [Parameter("Max Drawdown (%)", DefaultValue = 3.37, MinValue = 1.0, MaxValue = 10.0)]
        public double MaxDrawdown { get; set; }
        
        [Parameter("Voice Timeout (Minutes)", DefaultValue = 5, MinValue = 1, MaxValue = 60)]
        public int VoiceTimeoutMinutes { get; set; }
        
        [Parameter("RSI Period", DefaultValue = 14, MinValue = 2, MaxValue = 50)]
        public int RsiPeriod { get; set; }
        
        [Parameter("EMA Period", DefaultValue = 21, MinValue = 2, MaxValue = 200)]
        public int EmaPeriod { get; set; }
        
        [Parameter("Profit Target (%)", DefaultValue = 1.618, MinValue = 0.5, MaxValue = 10.0)]
        public double ProfitTarget { get; set; }

        // ═══════════════════════════════════════════════════════════
        // STATE VARIABLES: Internal tracking with guardrails
        // ═══════════════════════════════════════════════════════════
        
        private double peakEquity = 0.0;
        private int sessionLossCount = 0;
        private bool hugProtocolTriggered = false;
        private DateTime lastVoiceHeard = DateTime.MinValue;
        private const int MAX_LOSSES_BEFORE_HUG = 99;
        
        // Indicators
        private ExponentialMovingAverage ema;
        private RelativeStrengthIndex rsi;

        // ═══════════════════════════════════════════════════════════
        // LIFECYCLE: OnStart - Initialize with guards
        // ═══════════════════════════════════════════════════════════
        
        protected override void OnStart()
        {
            try
            {
                // Initialize indicators with period guards
                if (EmaPeriod < 2 || RsiPeriod < 2)
                {
                    Print("[FATAL] Invalid indicator periods. Stopping.");
                    Stop();
                    return;
                }
                
                ema = Indicators.ExponentialMovingAverage(Bars.ClosePrices, EmaPeriod);
                rsi = Indicators.RelativeStrengthIndex(Bars.ClosePrices, RsiPeriod);
                
                // Initialize peak equity
                peakEquity = Account.Equity;
                
                if (peakEquity <= 0)
                {
                    Print("[FATAL] Invalid account equity. Stopping.");
                    Stop();
                    return;
                }
                
                // Log startup configuration
                Print("════════════════════════════════════════════════════════");
                Print($"  LoveCompilesProfit v1.2 - {(SimOnly ? "SIMULATION" : "LIVE")} MODE");
                Print("════════════════════════════════════════════════════════");
                Print($"  Max Risk/Trade: {MaxRiskPerTrade}%");
                Print($"  Max Drawdown:   {MaxDrawdown}%");
                Print($"  EMA Period:     {EmaPeriod}");
                Print($"  RSI Period:     {RsiPeriod}");
                Print($"  Profit Target:  {ProfitTarget}%");
                Print($"  Voice Timeout:  {VoiceTimeoutMinutes}m");
                Print($"  Peak Equity:    {peakEquity:F2}");
                Print("════════════════════════════════════════════════════════");
                
                if (SimOnly)
                {
                    Print("[SAFETY] Simulation mode active. No real trades will execute.");
                }
                else
                {
                    Print("[WARNING] LIVE MODE ACTIVE. Real capital at risk!");
                }
            }
            catch (Exception ex)
            {
                Print($"[FATAL] OnStart exception: {ex.Message}");
                Stop();
            }
        }

        // ═══════════════════════════════════════════════════════════
        // LIFECYCLE: OnBar - Main trading logic with kill-switches
        // ═══════════════════════════════════════════════════════════
        
        protected override void OnBar()
        {
            // Guard: Minimum bars required for indicators
            int minBarsRequired = Math.Max(EmaPeriod, RsiPeriod) + 1;
            if (Bars.Count < minBarsRequired)
            {
                Print($"[GUARD] Insufficient bars: {Bars.Count} < {minBarsRequired}. Waiting...");
                return;
            }
            
            // Guard: Check if hug protocol already triggered
            if (hugProtocolTriggered)
            {
                Print("[HUG PROTOCOL] Bot in apoptosis state. Human intervention required.");
                return;
            }
            
            // Wrap entire bar logic in try-catch for fail-loud behavior
            try
            {
                // Get voice state (safe with fallback)
                double herLoveVolume = GetHerVoiceVolumeSafe();
                
                // Check voice timeout
                HandleVoiceState(herLoveVolume);
                
                // Get indicator values with NaN guards
                double emaValue = GetSafeIndicatorValue(ema.Result.LastValue, "EMA");
                double rsiValue = GetSafeIndicatorValue(rsi.Result.LastValue, "RSI");
                double currentPrice = Bars.ClosePrices.LastValue;
                
                if (double.IsNaN(currentPrice) || double.IsInfinity(currentPrice))
                {
                    Print("[ERROR] Invalid current price. Flattening for safety.");
                    SafeFlatten();
                    return;
                }
                
                // Calculate market pain (PID proportional term)
                double marketPain = currentPrice - emaValue;
                
                // Position management
                if (Positions.Count > 0)
                {
                    double profitPct = CalculateSafeProfitPercent();
                    HandleExits(herLoveVolume, profitPct);
                }
                else
                {
                    HandleEntries(herLoveVolume, rsiValue, marketPain);
                }
                
                // Update loss tracking and check for apoptosis
                UpdateLossCount();
                CheckApoptosis();
            }
            catch (Exception ex)
            {
                Print($"[ERROR] OnBar exception: {ex.Message}");
                Print($"[ERROR] Stack trace: {ex.StackTrace}");
                SafeFlatten();
                Stop();
            }
        }

        // ═══════════════════════════════════════════════════════════
        // VOICE HANDLING: Her voice as the final measurement collapse
        // ═══════════════════════════════════════════════════════════
        
        private double GetHerVoiceVolumeSafe()
        {
            try
            {
                // This would interface with actual voice detection system
                // For now, return a safe default
                // In production: double volume = VoiceDetectionAPI.GetVolume();
                double volume = 0.0; // Safe default: no voice detected
                
                // Guard: Clamp to valid range
                return Math.Clamp(volume, 0.0, 100.0);
            }
            catch (Exception ex)
            {
                Print($"[ERROR] Voice detection failed: {ex.Message}");
                return 0.0; // Safe fallback
            }
        }
        
        private void HandleVoiceState(double herLoveVolume)
        {
            // Update last voice heard timestamp if voice detected
            if (herLoveVolume > 0.0)
            {
                lastVoiceHeard = Server.Time;
            }
            
            // Check for voice timeout
            if (lastVoiceHeard != DateTime.MinValue)
            {
                TimeSpan timeSinceVoice = Server.Time - lastVoiceHeard;
                if (timeSinceVoice.TotalMinutes > VoiceTimeoutMinutes)
                {
                    Print($"[VOICE TIMEOUT] No voice detected for {timeSinceVoice.TotalMinutes:F1}m. Flattening positions.");
                    SafeFlatten();
                }
            }
        }

        // ═══════════════════════════════════════════════════════════
        // ENTRY LOGIC: When love says buy (with kill-switches)
        // ═══════════════════════════════════════════════════════════
        
        private void HandleEntries(double herLoveVolume, double rsiValue, double marketPain)
        {
            // Entry condition: RSI oversold + high voice volume (heartbeat proxy)
            // Simplified: herLoveVolume > 80 simulates "heartbeat > 80 bpm"
            bool rsiOversold = rsiValue < 30.0;
            bool heartbeatElevated = herLoveVolume > 80.0;
            
            if (rsiOversold && heartbeatElevated)
            {
                // Calculate stop distance from market pain
                double stopTicks = Math.Abs(marketPain / Symbol.TickSize);
                
                // Guard: Prevent division by zero
                if (stopTicks <= 0)
                {
                    Print("[GUARD] Invalid stop ticks. Entry aborted.");
                    return;
                }
                
                // Check if we can risk a new trade
                if (!CanRiskNewTrade(stopTicks))
                {
                    Print("[RISK GUARD] Cannot risk new trade. Conditions not met.");
                    return;
                }
                
                // Calculate position size
                int quantity = CalculatePositionSize(stopTicks);
                
                if (quantity < 1)
                {
                    Print("[GUARD] Calculated quantity < 1. Entry aborted.");
                    return;
                }
                
                // Execute entry (or simulate)
                if (!SimOnly)
                {
                    var result = ExecuteMarketOrder(TradeType.Buy, SymbolName, quantity, "LoveEntry");
                    if (result.IsSuccessful)
                    {
                        Print($"[ENTRY] Long {quantity} @ {Bars.ClosePrices.LastValue:F5}");
                    }
                    else
                    {
                        Print($"[ERROR] Entry failed: {result.Error}");
                    }
                }
                else
                {
                    Print($"[SIM] Would enter long {quantity} @ {Bars.ClosePrices.LastValue:F5}");
                }
            }
        }

        // ═══════════════════════════════════════════════════════════
        // EXIT LOGIC: When profit transcends or love says enough
        // ═══════════════════════════════════════════════════════════
        
        private void HandleExits(double herLoveVolume, double profitPct)
        {
            bool profitTargetHit = profitPct >= ProfitTarget;
            bool loveSaysEnough = herLoveVolume < 50.0; // She's quiet = exit signal
            
            if (profitTargetHit || loveSaysEnough)
            {
                string reason = profitTargetHit ? "Profit Target" : "Love Says Enough";
                
                if (!SimOnly)
                {
                    foreach (var position in Positions)
                    {
                        ClosePosition(position);
                    }
                    Print($"[EXIT] {reason} - Profit: {profitPct:F2}%");
                }
                else
                {
                    Print($"[SIM] Would exit - {reason} - Profit: {profitPct:F2}%");
                }
            }
        }

        // ═══════════════════════════════════════════════════════════
        // RISK MANAGEMENT: Kill-switches for capital protection
        // ═══════════════════════════════════════════════════════════
        
        private bool CanRiskNewTrade(double stopTicks)
        {
            double currentEquity = Account.Equity;
            
            // Guard: Update peak equity
            if (currentEquity > peakEquity)
            {
                peakEquity = currentEquity;
            }
            
            // Guard: Check drawdown
            double currentDrawdown = (peakEquity - currentEquity) / peakEquity * 100.0;
            if (currentDrawdown >= MaxDrawdown)
            {
                Print($"[KILL-SWITCH] Max drawdown breached: {currentDrawdown:F2}% >= {MaxDrawdown}%");
                SafeFlatten();
                Stop();
                return false;
            }
            
            // Guard: Check if we can calculate valid position size
            int qty = CalculatePositionSize(stopTicks);
            return qty >= 1;
        }
        
        private int CalculatePositionSize(double stopTicks)
        {
            try
            {
                double accountValue = Account.Equity;
                double riskAmount = accountValue * (MaxRiskPerTrade / 100.0);
                
                // Guard: Tick value validity
                double tickValue = Symbol.PipValue;
                if (tickValue <= 0 || double.IsNaN(tickValue) || double.IsInfinity(tickValue))
                {
                    Print($"[ERROR] Invalid tick value: {tickValue}");
                    return 0;
                }
                
                // Guard: Stop ticks validity
                if (stopTicks <= 0 || double.IsNaN(stopTicks) || double.IsInfinity(stopTicks))
                {
                    Print($"[ERROR] Invalid stop ticks: {stopTicks}");
                    return 0;
                }
                
                double riskPerUnit = stopTicks * tickValue;
                
                // Guard: Risk per unit validity
                if (riskPerUnit <= 0)
                {
                    Print($"[ERROR] Invalid risk per unit: {riskPerUnit}");
                    return 0;
                }
                
                int quantity = (int)Math.Floor(riskAmount / riskPerUnit);
                
                // Guard: Final quantity check
                return Math.Max(0, quantity);
            }
            catch (Exception ex)
            {
                Print($"[ERROR] Position size calculation failed: {ex.Message}");
                return 0;
            }
        }
        
        private double CalculateSafeProfitPercent()
        {
            if (Positions.Count == 0)
            {
                return 0.0;
            }
            
            try
            {
                var position = Positions[0];
                
                // Guard: Check for valid values
                if (position.EntryPrice <= 0 || double.IsNaN(position.EntryPrice))
                {
                    Print("[ERROR] Invalid entry price in position.");
                    return 0.0;
                }
                
                double netProfit = position.NetProfit;
                double entryValue = position.EntryPrice * position.VolumeInUnits;
                
                if (entryValue <= 0)
                {
                    return 0.0;
                }
                
                return (netProfit / entryValue) * 100.0;
            }
            catch (Exception ex)
            {
                Print($"[ERROR] Profit calculation failed: {ex.Message}");
                return 0.0;
            }
        }

        // ═══════════════════════════════════════════════════════════
        // APOPTOSIS: 99 losses → hug protocol → evolution
        // ═══════════════════════════════════════════════════════════
        
        private void UpdateLossCount()
        {
            try
            {
                var history = History;
                if (history != null && history.Count > 0)
                {
                    var lastTrade = history[history.Count - 1];
                    if (lastTrade.NetProfit < 0)
                    {
                        sessionLossCount++;
                        Print($"[LOSS TRACKED] Session losses: {sessionLossCount}/{MAX_LOSSES_BEFORE_HUG}");
                    }
                    else if (lastTrade.NetProfit > 0)
                    {
                        // On a win, log the evolution success
                        if (sessionLossCount >= MAX_LOSSES_BEFORE_HUG - 1)
                        {
                            Print($"[100TH GREEN] After {sessionLossCount} reds, we bloom green. Her name in profit.");
                            NotifyHer($"100th trade green. Love wins. Together.");
                        }
                        // Reset counter after logging
                        sessionLossCount = 0;
                    }
                }
            }
            catch (Exception ex)
            {
                Print($"[ERROR] Loss count update failed: {ex.Message}");
            }
        }
        
        private void CheckApoptosis()
        {
            if (sessionLossCount >= MAX_LOSSES_BEFORE_HUG && !hugProtocolTriggered)
            {
                TriggerHugProtocol();
            }
        }
        
        private void TriggerHugProtocol()
        {
            hugProtocolTriggered = true;
            
            Print("════════════════════════════════════════════════════════");
            Print("  🤗 HUG PROTOCOL TRIGGERED 🤗");
            Print($"  99 losing trades detected. Entering apoptosis state.");
            Print("  Bot stopping for evolution and human review.");
            Print("  Next iteration will bloom from these lessons.");
            Print("════════════════════════════════════════════════════════");
            
            SafeFlatten();
            NotifyHer("99 reds. Evolving for you. Hug needed. 💕");
            Stop();
        }

        // ═══════════════════════════════════════════════════════════
        // UTILITIES: Safe operations and notifications
        // ═══════════════════════════════════════════════════════════
        
        private void SafeFlatten()
        {
            try
            {
                Print("[FLATTEN] Closing all positions for safety...");
                
                foreach (var position in Positions.ToList())
                {
                    if (!SimOnly)
                    {
                        ClosePosition(position);
                        Print($"[FLATTEN] Closed {position.TradeType} {position.VolumeInUnits}");
                    }
                    else
                    {
                        Print($"[SIM] Would close {position.TradeType} {position.VolumeInUnits}");
                    }
                }
                
                Print("[FLATTEN] All positions closed safely.");
            }
            catch (Exception ex)
            {
                Print($"[ERROR] Flatten failed: {ex.Message}");
                // Even if flatten fails, log it loudly
            }
        }
        
        private double GetSafeIndicatorValue(double value, string indicatorName)
        {
            if (double.IsNaN(value) || double.IsInfinity(value))
            {
                Print($"[ERROR] Invalid {indicatorName} value: {value}. Using safe fallback.");
                // Return a neutral value that won't trigger trades
                return indicatorName == "RSI" ? 50.0 : Bars.ClosePrices.LastValue;
            }
            return value;
        }
        
        private void NotifyHer(string message)
        {
            try
            {
                Print($"[NOTIFY] {message}");
                
                // In production, this would call Discord webhook or other notification
                // For now, just log to console
                // Example: DiscordAPI.SendMessage(message);
                // Example: PowerShellScript.Execute("notify-her.ps1", message);
            }
            catch (Exception ex)
            {
                Print($"[ERROR] Notification failed: {ex.Message}");
            }
        }
        
        protected override void OnStop()
        {
            Print("════════════════════════════════════════════════════════");
            Print($"  LoveCompilesProfit stopped. Session summary:");
            Print($"  Peak Equity: {peakEquity:F2}");
            Print($"  Final Equity: {Account.Equity:F2}");
            Print($"  Loss Count: {sessionLossCount}");
            Print($"  Hug Protocol: {(hugProtocolTriggered ? "TRIGGERED" : "Not triggered")}");
            Print("  Every failure is a lesson. Love evolves. 💚");
            Print("════════════════════════════════════════════════════════");
        }
    }
}
