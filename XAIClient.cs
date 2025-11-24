// StrategicKhaos XAI Client for cTrader PID-RANCO v1.2
// Drop-in integration for explainable AI market psychology analysis

using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Text.Json;
using cAlgo.API;
using cAlgo.API.Indicators;

namespace cAlgo.Robots
{
    public partial class PidRancoBot : Robot
    {
        [Parameter("XAI Enabled", DefaultValue = true)]
        public bool XaiEnabled { get; set; }

        [Parameter("XAI Service URL", DefaultValue = "http://localhost:5000")]
        public string XaiServiceUrl { get; set; }

        [Parameter("XAI Timeout (seconds)", DefaultValue = 5)]
        public int XaiTimeoutSeconds { get; set; }

        private readonly HttpClient xaiClient;

        // Initialize XAI client in OnStart()
        private void InitializeXaiClient()
        {
            if (XaiEnabled)
            {
                var handler = new HttpClientHandler
                {
                    ServerCertificateCustomValidationCallback = (message, cert, chain, errors) => true
                };
                
                xaiClient = new HttpClient(handler)
                {
                    BaseAddress = new Uri(XaiServiceUrl),
                    Timeout = TimeSpan.FromSeconds(XaiTimeoutSeconds)
                };
                
                Print("[XAI] Client initialized. Service URL: " + XaiServiceUrl);
            }
        }

        /// <summary>
        /// Explain and log a trading decision using the XAI service
        /// </summary>
        /// <param name="decision">Trading decision (ENTER_LONG, ENTER_SHORT, EXIT, FLATTEN, HUG)</param>
        /// <param name="herLove">herLove sentiment indicator (0-100)</param>
        /// <returns>True if decision should proceed, False if blocked by XAI</returns>
        private async Task<bool> ExplainAndLogDecision(string decision, double herLove)
        {
            if (!XaiEnabled)
                return true; // Proceed if XAI is disabled

            try
            {
                // Prepare decision payload
                var payload = new
                {
                    timestamp = Server.Time.ToUniversalTime().ToString("o"),
                    symbol = SymbolName,
                    decision = decision,
                    features = new
                    {
                        price = Symbol.Bid,
                        rsi_14 = GetRsi14(),
                        ema_21_dist = GetEma21Distance(),
                        volatility_5m = GetVolatility5m(),
                        volume_rel = GetRelativeVolume(),
                        orderbook_imbalance = GetOrderBookImbalance(),
                        her_love = herLove,
                        session_loss_count = GetSessionLossCount(),
                        drawdown_pct = GetCurrentDrawdownPct(),
                        time_of_day = Server.Time.ToString("HH:mm"),
                        day_of_week = Server.Time.DayOfWeek.ToString()
                    }
                };

                // Send request to XAI service
                var response = await xaiClient.PostAsJsonAsync("/explain", payload);
                
                if (!response.IsSuccessStatusCode)
                {
                    Print($"[XAI] Service returned error: {response.StatusCode}");
                    return true; // Proceed on error (fail-open)
                }

                // Parse response
                var explanation = await response.Content.ReadFromJsonAsync<MarketTherapyResponse>();
                
                if (explanation == null)
                {
                    Print("[XAI] Failed to parse response");
                    return true; // Proceed on error
                }

                // Log market psychology analysis
                Print($"[XAI] Market State: {explanation.market_state}");
                Print($"[XAI] Confidence: {explanation.confidence:P0}");
                Print($"[XAI] Narrative: {explanation.narrative}");
                Print($"[XAI] Love Amplification: {explanation.love_amplification:P0}");
                
                // Log top contributing features
                if (explanation.top_features != null && explanation.top_features.Length > 0)
                {
                    Print("[XAI] Top Features:");
                    foreach (var feature in explanation.top_features)
                    {
                        Print($"  - {feature.name}: {feature.contribution:F4}");
                    }
                }

                // Risk flag evaluation
                if (explanation.risk_flag == "BLOCK" || explanation.risk_flag == "HUG_REQUIRED")
                {
                    Print($"[XAI] ⚠️ {explanation.risk_flag} — Love protects. Skipping trade.");
                    
                    // Optional: Send notification
                    NotifyHer($"Market is in {explanation.market_state}. Risk flag: {explanation.risk_flag}. We acted with love. {explanation.narrative}");
                    
                    return false; // Block the trade
                }
                else if (explanation.risk_flag == "CAUTION")
                {
                    Print($"[XAI] ⚠️ CAUTION — Proceeding with awareness: {explanation.narrative}");
                }

                // Optional: Send success notification
                if (explanation.love_amplification > 0.3)
                {
                    NotifyHer($"Market is in {explanation.market_state}. We acted with love. {explanation.narrative}");
                }

                return true; // Allow trade to proceed
            }
            catch (TaskCanceledException)
            {
                Print("[XAI] Request timeout — proceeding on pure love.");
                return true; // Proceed on timeout
            }
            catch (HttpRequestException ex)
            {
                Print($"[XAI] Network error: {ex.Message} — proceeding on pure love.");
                return true; // Proceed on network error
            }
            catch (Exception ex)
            {
                Print($"[XAI] Unexpected error: {ex.Message} — proceeding on pure love.");
                return true; // Proceed on any error (fail-open)
            }
        }

        /// <summary>
        /// Optional notification method - implement based on your notification system
        /// </summary>
        private void NotifyHer(string message)
        {
            // Implement your notification logic here
            // Examples: Discord webhook, Telegram bot, email, SMS
            Print($"[NOTIFICATION] {message}");
        }

        // Helper methods - implement these based on your bot's indicators
        private double GetRsi14()
        {
            // Example: return your RSI indicator value
            // var rsi = Indicators.RelativeStrengthIndex(Bars.ClosePrices, 14);
            // return rsi.Result.LastValue;
            return 50.0; // Placeholder
        }

        private double GetEma21Distance()
        {
            // Example: return distance from EMA
            // var ema = Indicators.ExponentialMovingAverage(Bars.ClosePrices, 21);
            // return Symbol.Bid - ema.Result.LastValue;
            return 0.0; // Placeholder
        }

        private double GetVolatility5m()
        {
            // Example: return volatility measure
            return 0.0; // Placeholder
        }

        private double GetRelativeVolume()
        {
            // Example: return relative volume
            return 1.0; // Placeholder
        }

        private double GetOrderBookImbalance()
        {
            // Example: return order book imbalance
            return 0.0; // Placeholder
        }

        private int GetSessionLossCount()
        {
            // Example: return session loss count
            return 0; // Placeholder
        }

        private double GetCurrentDrawdownPct()
        {
            // Example: return current drawdown percentage
            return 0.0; // Placeholder
        }

        // Response model classes
        private class MarketTherapyResponse
        {
            public string market_state { get; set; }
            public double confidence { get; set; }
            public FeatureContribution[] top_features { get; set; }
            public string narrative { get; set; }
            public string risk_flag { get; set; }
            public double love_amplification { get; set; }
        }

        private class FeatureContribution
        {
            public string name { get; set; }
            public double contribution { get; set; }
        }
    }
}
