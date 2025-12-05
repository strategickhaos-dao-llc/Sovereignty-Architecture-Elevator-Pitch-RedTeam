'use client'

import { useState } from 'react'
import { formatDistanceToNow } from 'date-fns'

// Mock transaction data
const TRANSACTIONS = [
  {
    id: '0x1234...5678',
    type: 'split',
    totalAmount: 1000,
    charityAmount: 70,
    operationsAmount: 930,
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    status: 'confirmed',
  },
  {
    id: '0x2345...6789',
    type: 'split',
    totalAmount: 500,
    charityAmount: 35,
    operationsAmount: 465,
    timestamp: new Date(Date.now() - 86400000).toISOString(),
    status: 'confirmed',
  },
  {
    id: '0x3456...7890',
    type: 'distribution',
    totalAmount: 105,
    recipients: ['Against Malaria Foundation', 'Helen Keller International'],
    timestamp: new Date(Date.now() - 172800000).toISOString(),
    status: 'confirmed',
  },
  {
    id: '0x4567...8901',
    type: 'split',
    totalAmount: 2500,
    charityAmount: 175,
    operationsAmount: 2325,
    timestamp: new Date(Date.now() - 259200000).toISOString(),
    status: 'confirmed',
  },
]

export function TransactionHistory() {
  const [filter, setFilter] = useState<'all' | 'splits' | 'distributions'>('all')
  
  const filteredTransactions = TRANSACTIONS.filter((tx) => {
    if (filter === 'all') return true
    if (filter === 'splits') return tx.type === 'split'
    if (filter === 'distributions') return tx.type === 'distribution'
    return true
  })
  
  return (
    <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-6">
        <h2 className="text-xl font-semibold flex items-center gap-2 mb-4 md:mb-0">
          <span className="text-2xl">📜</span>
          Transaction History
        </h2>
        
        {/* Filter buttons */}
        <div className="flex gap-2">
          {(['all', 'splits', 'distributions'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                filter === f
                  ? 'bg-dao-primary text-white'
                  : 'bg-slate-700/50 text-slate-400 hover:bg-slate-700'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>
      
      {/* Transaction List */}
      <div className="space-y-3">
        {filteredTransactions.map((tx) => (
          <div 
            key={tx.id}
            className="bg-slate-700/30 rounded-xl p-4 hover:bg-slate-700/50 transition-colors"
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              {/* Left side - Transaction info */}
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  tx.type === 'split' 
                    ? 'bg-dao-primary/20 text-dao-primary' 
                    : 'bg-dao-charity/20 text-dao-charity'
                }`}>
                  {tx.type === 'split' ? '⚡' : '💚'}
                </div>
                <div>
                  <div className="font-medium text-white">
                    {tx.type === 'split' ? 'Revenue Split' : 'Charity Distribution'}
                  </div>
                  <div className="text-xs text-slate-400 font-mono">{tx.id}</div>
                </div>
              </div>
              
              {/* Right side - Amount and time */}
              <div className="flex items-center gap-6">
                {tx.type === 'split' ? (
                  <div className="text-right">
                    <div className="font-bold text-white">
                      ${tx.totalAmount.toLocaleString()}
                    </div>
                    <div className="text-xs">
                      <span className="text-dao-charity">
                        ${tx.charityAmount} charity
                      </span>
                      {' / '}
                      <span className="text-dao-operations">
                        ${tx.operationsAmount} ops
                      </span>
                    </div>
                  </div>
                ) : (
                  <div className="text-right">
                    <div className="font-bold text-dao-charity">
                      ${tx.totalAmount.toLocaleString()}
                    </div>
                    <div className="text-xs text-slate-400">
                      to {tx.recipients?.length} charities
                    </div>
                  </div>
                )}
                
                <div className="text-right min-w-[100px]">
                  <div className="text-sm text-slate-300">
                    {formatDistanceToNow(new Date(tx.timestamp), { addSuffix: true })}
                  </div>
                  <div className="flex items-center gap-1 justify-end">
                    <div className="w-2 h-2 bg-green-500 rounded-full" />
                    <span className="text-xs text-green-500">Confirmed</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Load More */}
      <div className="mt-6 text-center">
        <button className="px-6 py-2 bg-slate-700/50 rounded-lg text-sm text-slate-400 hover:bg-slate-700 hover:text-white transition-colors">
          Load More Transactions
        </button>
      </div>
      
      {/* Basescan Link */}
      <div className="mt-4 text-center">
        <a 
          href="#" 
          className="text-sm text-slate-400 hover:text-white transition-colors"
        >
          View all transactions on Basescan →
        </a>
      </div>
    </div>
  )
}
