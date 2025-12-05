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

// This namespace holds Strategies in this folder and is required. Do not change it. 
namespace NinjaTrader.NinjaScript.Strategies
{
    public class BabySolvernMACross : Strategy
    {
        private EMA fastMA;  // Fast EMA (e.g., 9-period)
        private EMA slowMA;  // Slow EMA (e.g., 21-period)

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Description = @"Baby's Simple MA Crossover Simulator - Buys on fast cross above slow, sells on cross below.";
                Name = "BabySolvernMACross";
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
                BarsRequiredToTrade = 21;  // Need enough bars for slow MA

                // User inputs - tweak these!
                FastPeriod = 9;
                SlowPeriod = 21;
                Quantity = 1;  // Contracts (keep small for sim)
            }
            else if (State == State.DataLoaded)
            {
                fastMA = EMA(Close, FastPeriod);
                slowMA = EMA(Close, SlowPeriod);
                AddChartIndicator(fastMA);  // Plot MAs on chart for visuals
                AddChartIndicator(slowMA);
            }
        }

        protected override void OnBarUpdate()
        {
            if (CurrentBar < BarsRequiredToTrade)
                return;  // Wait for enough data

            // Entry Logic: Long on crossover up, Short on crossover down
            if (CrossAbove(fastMA, slowMA, 1))  // Fast crossed above slow in last bar
            {
                EnterLong(Quantity, "BabyLong");  // Buy signal
                Print(Time[0] + ": Baby BUY at " + Close[0]);  // Log to output
            }
            else if (CrossBelow(fastMA, slowMA, 1))  // Fast crossed below slow
            {
                EnterShort(Quantity, "BabyShort");  // Sell signal
                Print(Time[0] + ": Baby SELL at " + Close[0]);
            }

            // Optional: Add stops/targets here if you want auto-exits
            // e.g., SetStopLoss("BabyLong", CalculationMode.Ticks, 20 * TickSize);
        }

        #region Properties - Tweak these in strategy params
        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name="Fast MA Period", Description="Fast EMA period", Order=1, GroupName="Parameters")]
        public int FastPeriod { get; set; }

        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name="Slow MA Period", Description="Slow MA period", Order=2, GroupName="Parameters")]
        public int SlowPeriod { get; set; }

        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name="Quantity", Description="Contracts to trade", Order=3, GroupName="Parameters")]
        public int Quantity { get; set; }
        #endregion
    }
}
