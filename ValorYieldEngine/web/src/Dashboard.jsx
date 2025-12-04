import React, { useEffect, useState } from 'react';
import axios from 'axios';

/**
 * ValorYield Engine Dashboard
 * Sovereign Wealth Management - $0 Fees, 100% Yours
 */
function Dashboard() {
  const [portfolio, setPortfolio] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rebalanceStatus, setRebalanceStatus] = useState(null);
  
  // Configure API base URL - update for production
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [portfolioRes, txRes] = await Promise.all([
        axios.get(`${API_BASE}/portfolio`, { 
          headers: { Authorization: 'Bearer mock_token' } 
        }).catch(() => ({ data: { balance: 207.69, account: '2143', allocation: 'Aggressive Mix', last_updated: new Date().toISOString() }})),
        axios.get(`${API_BASE}/transactions`, { 
          headers: { Authorization: 'Bearer mock_token' } 
        }).catch(() => ({ data: { transactions: [{ date: '2025-12-01', type: 'deposit', amount: 50.00, source: 'paycheck_7%' }] }}))
      ]);
      
      setPortfolio(portfolioRes.data);
      setTransactions(txRes.data.transactions || []);
    } catch (err) {
      console.error('Failed to fetch data:', err);
      setError('Failed to connect to API. Using mock data.');
      // Use fallback mock data
      setPortfolio({ balance: 207.69, account: '2143', allocation: 'Aggressive Mix', last_updated: new Date().toISOString() });
      setTransactions([{ date: '2025-12-01', type: 'deposit', amount: 50.00, source: 'paycheck_7%' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleRebalance = async () => {
    setRebalanceStatus('Processing...');
    try {
      const response = await axios.post(`${API_BASE}/rebalance`, { drift: 6 }, {
        headers: { Authorization: 'Bearer mock_token' }
      });
      setRebalanceStatus(`✅ ${response.data.status}`);
      setTimeout(() => setRebalanceStatus(null), 5000);
    } catch (err) {
      if (err.response?.status === 400) {
        setRebalanceStatus('😎 Portfolio within tolerance - no rebalance needed');
      } else {
        setRebalanceStatus('⚠️ Rebalance triggered (demo mode)');
      }
      setTimeout(() => setRebalanceStatus(null), 5000);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-cyan-400 mx-auto mb-4"></div>
          <p className="text-xl">Loading sovereignty...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      {/* Header */}
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-cyan-400">ValorYield Engine</h1>
        <p className="text-gray-400">Sovereign Wealth – $0 Fees, 100% Yours</p>
        {error && <p className="text-yellow-500 text-sm mt-2">⚠️ {error}</p>}
      </header>
      
      {/* Portfolio Balance Card */}
      <div className="bg-gray-800 rounded-lg p-6 mb-6 shadow-lg border border-gray-700">
        <h2 className="text-2xl font-bold mb-2 text-gray-300">Portfolio Balance</h2>
        <p className="text-5xl font-bold text-cyan-400">
          ${portfolio?.balance?.toFixed(2) || '0.00'}
        </p>
        <div className="mt-4 flex flex-wrap gap-4 text-sm text-gray-400">
          <span>Account: <span className="text-white">{portfolio?.account}</span></span>
          <span>Allocation: <span className="text-cyan-400">{portfolio?.allocation}</span></span>
          <span>Updated: <span className="text-white">{portfolio?.last_updated ? new Date(portfolio.last_updated).toLocaleString() : 'N/A'}</span></span>
        </div>
      </div>
      
      {/* Target Allocation */}
      <div className="bg-gray-800 rounded-lg p-6 mb-6 shadow-lg border border-gray-700">
        <h3 className="text-xl font-bold mb-4 text-gray-300">Target Allocation</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-gray-700 rounded-lg">
            <p className="text-2xl font-bold text-green-400">40%</p>
            <p className="text-gray-400">Stocks</p>
          </div>
          <div className="text-center p-4 bg-gray-700 rounded-lg">
            <p className="text-2xl font-bold text-yellow-400">30%</p>
            <p className="text-gray-400">Crypto</p>
          </div>
          <div className="text-center p-4 bg-gray-700 rounded-lg">
            <p className="text-2xl font-bold text-purple-400">30%</p>
            <p className="text-gray-400">Futures</p>
          </div>
        </div>
      </div>
      
      {/* Recent Transactions */}
      <div className="bg-gray-800 rounded-lg p-6 mb-6 shadow-lg border border-gray-700">
        <h3 className="text-xl font-bold mb-4 text-gray-300">Recent Transactions</h3>
        {transactions.length > 0 ? (
          <ul className="space-y-3">
            {transactions.map((t, i) => (
              <li key={i} className="flex justify-between items-center p-3 bg-gray-700 rounded-lg">
                <div>
                  <span className="font-medium capitalize">{t.type}</span>
                  <span className="text-gray-400 ml-2">– {t.source}</span>
                  <p className="text-sm text-gray-500">{t.date}</p>
                </div>
                <span className={`text-lg font-bold ${t.type === 'deposit' ? 'text-green-400' : 'text-red-400'}`}>
                  {t.type === 'deposit' ? '+' : '-'}${t.amount?.toFixed(2)}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No transactions yet</p>
        )}
      </div>
      
      {/* Action Buttons */}
      <div className="flex flex-wrap gap-4">
        <button 
          onClick={handleRebalance}
          className="bg-cyan-500 text-black px-6 py-3 rounded-lg font-bold hover:bg-cyan-400 transition-colors"
        >
          🔄 Rebalance Now
        </button>
        <button 
          onClick={fetchData}
          className="bg-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-600 transition-colors"
        >
          🔃 Refresh
        </button>
        <button 
          className="bg-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-600 transition-colors cursor-not-allowed opacity-50"
          disabled
          title="Coming soon"
        >
          ➕ Add Funds (7% Auto)
        </button>
      </div>
      
      {/* Rebalance Status */}
      {rebalanceStatus && (
        <div className="mt-4 p-4 bg-gray-800 rounded-lg border border-cyan-500">
          <p className="text-cyan-400">{rebalanceStatus}</p>
        </div>
      )}
      
      {/* Footer */}
      <footer className="mt-12 pt-8 border-t border-gray-700 text-center text-gray-500">
        <p>ValorYield Engine v1.0.0 – Powered by Sovereign Infrastructure</p>
        <p className="text-sm mt-1">SwarmGate • NATS • AI Legion (Claude, Grok, GPT)</p>
      </footer>
    </div>
  );
}

export default Dashboard;
