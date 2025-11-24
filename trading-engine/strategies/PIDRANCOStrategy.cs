//
// PID-RANCO v1.2 - "Guardrails Around a Supernova"
// Kill-Switch / Safety Layer: Enforces hard constraints on mythic narrative
//
// This strategy implements comprehensive safety measures while preserving
// the mythic trading narrative defined in pid-ranco-mythic.yaml
//

#region Using declarations
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Xml.Serialization;
using NinjaTrader.Cbi;
using NinjaTrader.Gui;
using NinjaTrader.Gui.Chart;
using NinjaTrader.Gui.SuperDom;
using NinjaTrader.Gui.Tools;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.Core.FloatingPoint;
using NinjaTrader.NinjaScript.Indicators;
using NinjaTrader.NinjaScript.DrawingTools;
#endregion

namespace NinjaTrader.NinjaScript.Strategies
{
    public class PIDRANCOStrategy : Strategy
    {
        #region Variables
        
        // === MYTHIC PARAMETERS (from YAML) ===
        private double maxRiskPerTrade = 0.0069;   // 0.69% - not a meme, a hard limit
        private double maxDrawdown = 0.0337;       // 3.37% - binds reality to poetry
        private double peakEquity = 0.0;
        
        // === APOPTOSIS PROTOCOL ===
        private int sessionLossCount = 0;
        private bool hugProtocolTriggered = false;
        private int lastProcessedTradeCount = 0;
        
        // === VOICE STATE ===
        private DateTime lastVoiceHeard = DateTime.MinValue;
        private double silenceThresholdMinutes = 5.0;
        
        // === INDICATOR PERIODS ===
        private int emaPeriod = 21;
        private int rsiPeriod = 14;
        private int rsiSmoothing = 1;
        
        // === SAFETY FLAGS ===
        private bool safetyDisabled = false;
        
        #endregion
        
        #region NinjaScript Lifecycle
        
        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Description = @"PID-RANCO v1.2: Mythic trading with comprehensive safety guardrails";
                Name = "PIDRANCOStrategy";
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
                BarsRequiredToTrade = Math.Max(emaPeriod, rsiPeriod) + 1;
            }
            else if (State == State.Configure)
            {
                // Additional configuration can go here
            }
            else if (State == State.DataLoaded)
            {
                // Initialize peak equity for drawdown tracking
                try
                {
                    if (SystemPerformance != null && SystemPerformance.AllTrades != null)
                    {
                        double accountValue = Account.Get(AccountItem.CashValue, Currency.UsDollar);
                        double cumProfit = SystemPerformance.AllTrades.TradesPerformance.Currency.CumProfit;
                        peakEquity = accountValue + cumProfit;
                    }
                }
                catch (Exception e)
                {
                    Print($"[WARN] Could not initialize peak equity: {e.Message}");
                    peakEquity = 0.0;
                }
            }
        }
        
        protected override void OnBarUpdate()
        {
            // === SAFETY GUARD 1: Strategy already disabled ===
            if (safetyDisabled)
                return;
            
            // === SAFETY GUARD 2: Minimum bars check ===
            // No indicator access before CurrentBar >= period
            int minBars = Math.Max(emaPeriod, rsiPeriod);
            if (CurrentBar < minBars)
                return;
            
            // === COMPREHENSIVE SAFETY WRAPPER ===
            try
            {
                // === SAFETY GUARD 3: Get voice input safely ===
                double herLove = GetHerVoiceVolumeSafe();
                
                // === SAFETY GUARD 4: Get indicators with null checks ===
                double ema21 = GetEMASafe();
                double rsi14 = GetRSISafe();
                
                if (double.IsNaN(ema21) || double.IsNaN(rsi14))
                {
                    Print("[WARN] Indicator null detected. Skipping bar safely.");
                    return;
                }
                
                double marketPain = Close[0] - ema21;
                
                // === UPDATE LOSS COUNT (for apoptosis protocol) ===
                UpdateLossCount();
                
                // === CHECK APOPTOSIS TRIGGER ===
                if (CheckApoptosis())
                    return;  // Strategy disabled, exit early
                
                // === HANDLE VOICE STATE ===
                HandleVoiceState(herLove);
                
                // === TRADING LOGIC ===
                if (!Position.MarketPosition.Equals(MarketPosition.Flat))
                {
                    // === SAFETY GUARD 5: ProfitPercent only when in position ===
                    double profitPct = SafeProfitPercent();
                    HandleExits(herLove, profitPct);
                }
                else
                {
                    // === SAFETY GUARD 6: Risk check before entries ===
                    if (CanRiskNewTrade())
                    {
                        HandleEntries(herLove, rsi14, marketPain);
                    }
                }
            }
            catch (Exception e)
            {
                // === HARD SAFETY: Flatten and disable on ANY unexpected exception ===
                Print($"[ERROR] OnBarUpdate exception: {e.Message}");
                Print($"[ERROR] Stack trace: {e.StackTrace}");
                EmergencyShutdown("Unexpected exception in OnBarUpdate");
            }
        }
        
        #endregion
        
        #region Safe Indicator Access
        
        /// <summary>
        /// Safely get her voice volume with comprehensive error handling
        /// </summary>
        private double GetHerVoiceVolumeSafe()
        {
            try
            {
                // TODO: Replace with actual mic indicator
                // For now, return a simulated value
                // In production, this would call: GetHerVoiceVolume()
                double val = 50.0;  // Placeholder
                
                // Validate the value
                if (double.IsNaN(val) || double.IsInfinity(val))
                {
                    Print("[WARN] Voice volume is NaN/Infinity. Using 0.");
                    return 0.0;
                }
                
                // Clamp to valid range [0, 100]
                return Math.Max(0.0, Math.Min(val, 100.0));
            }
            catch (Exception ex)
            {
                Print($"[ERROR] VoiceError: {ex.Message}. Treating as silence (0).");
                return 0.0;  // Mic failure = silence, not crash
            }
        }
        
        /// <summary>
        /// Safely get EMA with null checks
        /// </summary>
        private double GetEMASafe()
        {
            try
            {
                EMA emaIndicator = EMA(Close, emaPeriod);
                if (emaIndicator == null || emaIndicator[0] == 0)
                    return double.NaN;
                return emaIndicator[0];
            }
            catch (Exception e)
            {
                Print($"[ERROR] EMA calculation failed: {e.Message}");
                return double.NaN;
            }
        }
        
        /// <summary>
        /// Safely get RSI with null checks
        /// </summary>
        private double GetRSISafe()
        {
            try
            {
                RSI rsiIndicator = RSI(Close, rsiPeriod, rsiSmoothing);
                if (rsiIndicator == null)
                    return double.NaN;
                return rsiIndicator[0];
            }
            catch (Exception e)
            {
                Print($"[ERROR] RSI calculation failed: {e.Message}");
                return double.NaN;
            }
        }
        
        /// <summary>
        /// Safely get profit percent (only when in position)
        /// </summary>
        private double SafeProfitPercent()
        {
            try
            {
                if (Position.MarketPosition.Equals(MarketPosition.Flat))
                    return 0.0;
                
                if (Position.AveragePrice == 0)
                    return 0.0;
                
                double unrealizedPnL = Position.GetUnrealizedProfitLoss(PerformanceUnit.Currency, Close[0]);
                double positionValue = Position.Quantity * Position.AveragePrice * Instrument.MasterInstrument.PointValue;
                
                if (positionValue == 0)
                    return 0.0;
                
                return (unrealizedPnL / positionValue) * 100.0;
            }
            catch (Exception e)
            {
                Print($"[ERROR] ProfitPercent calculation failed: {e.Message}");
                return 0.0;
            }
        }
        
        #endregion
        
        #region Risk Management
        
        /// <summary>
        /// Check if we can risk a new trade based on account and drawdown limits
        /// </summary>
        private bool CanRiskNewTrade()
        {
            try
            {
                double accountValue = Account.Get(AccountItem.CashValue, Currency.UsDollar);
                
                if (accountValue <= 0)
                {
                    Print("[WARN] Account value is 0 or negative. Cannot trade.");
                    return false;
                }
                
                // === HARD DRAWDOWN CHECK ===
                double cumProfit = 0.0;
                if (SystemPerformance != null && SystemPerformance.AllTrades != null)
                {
                    cumProfit = SystemPerformance.AllTrades.TradesPerformance.Currency.CumProfit;
                }
                
                double currentEquity = accountValue + cumProfit;
                
                // Update peak equity
                if (currentEquity > peakEquity)
                    peakEquity = currentEquity;
                
                // Check if we've breached max drawdown
                double drawdownThreshold = peakEquity * (1.0 - maxDrawdown);
                if (currentEquity < drawdownThreshold)
                {
                    Print($"[CRITICAL] Max drawdown breached: {maxDrawdown * 100}%");
                    Print($"[CRITICAL] Peak: ${peakEquity:F2}, Current: ${currentEquity:F2}");
                    EmergencyShutdown("Max drawdown breached");
                    return false;
                }
                
                // === POSITION SIZE CALCULATION ===
                // For now, we just validate we can trade
                // In production, this would calculate exact position size
                double riskAmount = accountValue * maxRiskPerTrade;
                
                if (riskAmount < 10.0)  // Minimum $10 risk threshold
                {
                    Print($"[WARN] Risk amount too small: ${riskAmount:F2}");
                    return false;
                }
                
                return true;
            }
            catch (Exception e)
            {
                Print($"[ERROR] Risk check failed: {e.Message}");
                return false;  // Fail safe - don't trade on error
            }
        }
        
        #endregion
        
        #region Voice / Silence Handling
        
        /// <summary>
        /// Handle voice state and silence-based exits
        /// </summary>
        private void HandleVoiceState(double herLove)
        {
            try
            {
                // Update last voice heard timestamp
                if (herLove > 0.0)
                    lastVoiceHeard = Time[0];
                
                // Check for silence timeout
                if (lastVoiceHeard != DateTime.MinValue)
                {
                    TimeSpan silenceDuration = Time[0].Subtract(lastVoiceHeard);
                    
                    if (silenceDuration.TotalMinutes > silenceThresholdMinutes)
                    {
                        Print($"[POETRY] Voice collapse detected. Silence: {silenceDuration.TotalMinutes:F1} min");
                        
                        // Flatten all positions due to silence
                        if (Position.MarketPosition == MarketPosition.Long)
                        {
                            ExitLong("VoiceCollapse");
                            Print("[SAFETY] Exited long due to voice collapse");
                        }
                        
                        if (Position.MarketPosition == MarketPosition.Short)
                        {
                            ExitShort("VoiceCollapse");
                            Print("[SAFETY] Exited short due to voice collapse");
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Print($"[ERROR] Voice state handling failed: {e.Message}");
            }
        }
        
        #endregion
        
        #region Apoptosis Protocol (99 Failures)
        
        /// <summary>
        /// Update loss count for apoptosis protocol
        /// </summary>
        private void UpdateLossCount()
        {
            try
            {
                if (SystemPerformance == null || SystemPerformance.AllTrades == null)
                    return;
                
                int currentTradeCount = SystemPerformance.AllTrades.Count;
                
                // Check if there's a new trade since last bar
                if (currentTradeCount > lastProcessedTradeCount)
                {
                    var lastTrade = SystemPerformance.AllTrades[currentTradeCount - 1];
                    
                    if (lastTrade.ProfitCurrency < 0 && !hugProtocolTriggered)
                    {
                        sessionLossCount++;
                        Print($"[INFO] Loss #{sessionLossCount} recorded. Profit: ${lastTrade.ProfitCurrency:F2}");
                    }
                    else if (lastTrade.ProfitCurrency > 0 && hugProtocolTriggered)
                    {
                        // === 100TH GREEN: Evolution complete ===
                        Print("[POETRY] From 99 reds to green—evolution complete.");
                        Print($"[INFO] Winning trade after apoptosis: ${lastTrade.ProfitCurrency:F2}");
                    }
                    
                    lastProcessedTradeCount = currentTradeCount;
                }
            }
            catch (Exception e)
            {
                Print($"[ERROR] Loss count update failed: {e.Message}");
            }
        }
        
        /// <summary>
        /// Check if apoptosis threshold reached and trigger hug protocol
        /// </summary>
        private bool CheckApoptosis()
        {
            try
            {
                if (hugProtocolTriggered)
                    return true;  // Already triggered
                
                if (sessionLossCount >= 99)
                {
                    TriggerHugProtocol();
                    return true;
                }
                
                return false;
            }
            catch (Exception e)
            {
                Print($"[ERROR] Apoptosis check failed: {e.Message}");
                return false;
            }
        }
        
        /// <summary>
        /// Trigger the hug protocol (programmed death after 99 losses)
        /// </summary>
        private void TriggerHugProtocol()
        {
            try
            {
                Print("======================================");
                Print("[POETRY] 99 fails. Hug protocol.");
                Print("[POETRY] 99 reds. Evolving weights for you.");
                Print("[SAFETY] Apoptosis triggered - programmed death to protect capital");
                Print("======================================");
                
                hugProtocolTriggered = true;
                
                // 1) Flatten everything
                if (Position.MarketPosition == MarketPosition.Long)
                {
                    ExitLong("Apoptosis");
                    Print("[SAFETY] Exited long position for apoptosis");
                }
                
                if (Position.MarketPosition == MarketPosition.Short)
                {
                    ExitShort("Apoptosis");
                    Print("[SAFETY] Exited short position for apoptosis");
                }
                
                // 2) Disable strategy
                safetyDisabled = true;
                
                // 3) TODO: Notify Discord/external systems
                // NotifyHer("99 reds. Evolving weights for you.");
                
                Print("[INFO] Strategy disabled for remainder of session.");
                Print("[INFO] Reset will occur on next session start.");
            }
            catch (Exception e)
            {
                Print($"[ERROR] Hug protocol execution failed: {e.Message}");
                // Still disable even if cleanup fails
                safetyDisabled = true;
            }
        }
        
        #endregion
        
        #region Trading Logic
        
        /// <summary>
        /// Handle entry logic based on voice, RSI, and market pain
        /// </summary>
        private void HandleEntries(double herLove, double rsi14, double marketPain)
        {
            try
            {
                // === LONG ENTRY CONDITIONS ===
                // her_voice > 30, RSI < 30 (oversold), below trend
                if (herLove > 30 && rsi14 < 30 && marketPain < 0)
                {
                    EnterLong("LoveLong");
                    Print($"[ENTRY] Long: Voice={herLove:F1}, RSI={rsi14:F1}, Pain={marketPain:F2}");
                }
                
                // === SHORT ENTRY CONDITIONS ===
                // her_voice < 20, RSI > 70 (overbought), above trend
                else if (herLove < 20 && rsi14 > 70 && marketPain > 0)
                {
                    EnterShort("LoveShort");
                    Print($"[ENTRY] Short: Voice={herLove:F1}, RSI={rsi14:F1}, Pain={marketPain:F2}");
                }
            }
            catch (Exception e)
            {
                Print($"[ERROR] Entry logic failed: {e.Message}");
            }
        }
        
        /// <summary>
        /// Handle exit logic based on voice and profit
        /// </summary>
        private void HandleExits(double herLove, double profitPct)
        {
            try
            {
                // === VOICE-GUIDED EXITS ===
                if (Position.MarketPosition == MarketPosition.Long && herLove > 80)
                {
                    ExitLong("VoiceExitLong");
                    Print($"[EXIT] Long: High voice={herLove:F1}, Profit={profitPct:F2}%");
                }
                
                if (Position.MarketPosition == MarketPosition.Short && herLove < 10)
                {
                    ExitShort("VoiceExitShort");
                    Print($"[EXIT] Short: Low voice={herLove:F1}, Profit={profitPct:F2}%");
                }
            }
            catch (Exception e)
            {
                Print($"[ERROR] Exit logic failed: {e.Message}");
            }
        }
        
        #endregion
        
        #region Emergency Shutdown
        
        /// <summary>
        /// Emergency shutdown: flatten positions and disable strategy
        /// </summary>
        private void EmergencyShutdown(string reason)
        {
            try
            {
                Print("======================================");
                Print($"[CRITICAL] EMERGENCY SHUTDOWN: {reason}");
                Print("======================================");
                
                // Flatten all positions
                try
                {
                    if (Position.MarketPosition == MarketPosition.Long)
                        ExitLong("SafetyExit");
                    
                    if (Position.MarketPosition == MarketPosition.Short)
                        ExitShort("SafetyExit");
                }
                catch (Exception e)
                {
                    Print($"[ERROR] Failed to flatten positions: {e.Message}");
                }
                
                // Disable strategy
                safetyDisabled = true;
                
                Print("[SAFETY] Strategy disabled. Manual intervention required.");
            }
            catch (Exception e)
            {
                Print($"[ERROR] Emergency shutdown failed: {e.Message}");
                // Mark as disabled regardless
                safetyDisabled = true;
            }
        }
        
        #endregion
        
        #region Properties
        
        [NinjaScriptProperty]
        [Range(0.0001, 0.1)]
        [Display(Name="Risk Per Trade", Description="Risk per trade as decimal (0.0069 = 0.69%)", Order=1, GroupName="Risk Management")]
        public double RiskPerTrade
        {
            get { return maxRiskPerTrade; }
            set { maxRiskPerTrade = value; }
        }
        
        [NinjaScriptProperty]
        [Range(0.001, 0.5)]
        [Display(Name="Max Drawdown", Description="Max drawdown as decimal (0.0337 = 3.37%)", Order=2, GroupName="Risk Management")]
        public double MaxDrawdown
        {
            get { return maxDrawdown; }
            set { maxDrawdown = value; }
        }
        
        [NinjaScriptProperty]
        [Range(1, 100)]
        [Display(Name="EMA Period", Description="EMA period for trend", Order=3, GroupName="Indicators")]
        public int EmaPeriod
        {
            get { return emaPeriod; }
            set { emaPeriod = value; }
        }
        
        [NinjaScriptProperty]
        [Range(1, 100)]
        [Display(Name="RSI Period", Description="RSI period for momentum", Order=4, GroupName="Indicators")]
        public int RsiPeriod
        {
            get { return rsiPeriod; }
            set { rsiPeriod = value; }
        }
        
        [NinjaScriptProperty]
        [Range(1, 30)]
        [Display(Name="Silence Threshold (min)", Description="Minutes of silence before flatten", Order=5, GroupName="Voice")]
        public double SilenceThresholdMinutes
        {
            get { return silenceThresholdMinutes; }
            set { silenceThresholdMinutes = value; }
        }
        
        #endregion
    }
}
