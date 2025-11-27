'use client'

import { useState, useEffect } from 'react'

// Mock data - in production, this would come from on-chain data
const MOCK_METRICS = {
  totalReceived: 15420.50,
  totalToCharity: 1079.44, // 7%
  totalToOperations: 14341.06, // 93%
  charityPercentage: 7,
  operationsPercentage: 93,
}

function AnimatedCounter({ value, prefix = '', suffix = '', duration = 2000 }: {
  value: number
  prefix?: string
  suffix?: string
  duration?: number
}) {
  const [displayValue, setDisplayValue] = useState(0)
  
  useEffect(() => {
    const startTime = Date.now()
    const endValue = value
    
    const updateValue = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      
      // Easing function for smooth animation
      const easeOutQuart = 1 - Math.pow(1 - progress, 4)
      setDisplayValue(endValue * easeOutQuart)
      
      if (progress < 1) {
        requestAnimationFrame(updateValue)
      }
    }
    
    requestAnimationFrame(updateValue)
  }, [value, duration])
  
  return (
    <span>
      {prefix}{displayValue.toLocaleString('en-US', { 
        minimumFractionDigits: 2, 
        maximumFractionDigits: 2 
      })}{suffix}
    </span>
  )
}

export function TrustMetrics() {
  const [metrics] = useState(MOCK_METRICS)
  
  return (
    <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
      <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
        <span className="text-2xl">📊</span>
        Treasury Overview
      </h2>
      
      {/* Total Received */}
      <div className="mb-8">
        <div className="text-sm text-slate-400 mb-1">Total Received (All Time)</div>
        <div className="text-4xl font-bold text-white">
          <AnimatedCounter value={metrics.totalReceived} prefix="$" />
        </div>
      </div>
      
      {/* Split Visualization */}
      <div className="grid grid-cols-2 gap-4">
        {/* Charity */}
        <div className="bg-dao-charity/10 rounded-xl p-4 border border-dao-charity/30">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-3 h-3 bg-dao-charity rounded-full" />
            <span className="text-sm text-dao-charity font-medium">
              {metrics.charityPercentage}% to Charity
            </span>
          </div>
          <div className="text-2xl font-bold text-dao-charity">
            <AnimatedCounter value={metrics.totalToCharity} prefix="$" />
          </div>
          <div className="text-xs text-slate-400 mt-1">IRREVOCABLE</div>
        </div>
        
        {/* Operations */}
        <div className="bg-dao-operations/10 rounded-xl p-4 border border-dao-operations/30">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-3 h-3 bg-dao-operations rounded-full" />
            <span className="text-sm text-dao-operations font-medium">
              {metrics.operationsPercentage}% to Operations
            </span>
          </div>
          <div className="text-2xl font-bold text-dao-operations">
            <AnimatedCounter value={metrics.totalToOperations} prefix="$" />
          </div>
          <div className="text-xs text-slate-400 mt-1">DAO Treasury</div>
        </div>
      </div>
      
      {/* Progress Bar */}
      <div className="mt-6">
        <div className="h-4 bg-slate-700 rounded-full overflow-hidden flex">
          <div 
            className="bg-dao-charity h-full transition-all duration-1000"
            style={{ width: `${metrics.charityPercentage}%` }}
          />
          <div 
            className="bg-dao-operations h-full transition-all duration-1000"
            style={{ width: `${metrics.operationsPercentage}%` }}
          />
        </div>
        <div className="flex justify-between mt-2 text-xs text-slate-400">
          <span>7% Charity (Locked)</span>
          <span>93% Operations</span>
        </div>
      </div>
    </div>
  )
}
