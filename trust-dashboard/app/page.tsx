'use client'

import { useState, useEffect } from 'react'
import { TrustMetrics } from '@/components/TrustMetrics'
import { CharityAllocation } from '@/components/CharityAllocation'
import { BuildVerification } from '@/components/BuildVerification'
import { TransactionHistory } from '@/components/TransactionHistory'

export default function TrustDashboard() {
  const [mounted, setMounted] = useState(false)
  
  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-2xl">Loading Trust Dashboard...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            <span className="text-gradient">Strategickhaos DAO</span>
          </h1>
          <p className="text-xl md:text-2xl text-slate-300 mb-2">
            Trust Dashboard
          </p>
          <p className="text-lg text-slate-400">
            7% to charity, <span className="text-dao-charity font-bold">forever</span>. 
            No rug pulls. No governance capture. No trust required.
          </p>
        </header>

        {/* Live Status Indicator */}
        <div className="flex justify-center mb-8">
          <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 rounded-full border border-slate-700">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm text-slate-300">Live on Base Chain</span>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Trust Metrics */}
          <TrustMetrics />
          
          {/* Charity Allocation */}
          <CharityAllocation />
        </div>

        {/* Build Verification */}
        <div className="mb-8">
          <BuildVerification />
        </div>

        {/* Transaction History */}
        <div className="mb-8">
          <TransactionHistory />
        </div>

        {/* Footer */}
        <footer className="text-center py-8 border-t border-slate-700">
          <p className="text-slate-400 mb-4">
            "An unstoppable, Wyoming-registered, 501(c)(3)-blessed machine that turns 
            every dollar it touches into 7% guaranteed, eternal charity."
          </p>
          <div className="flex justify-center gap-6 text-sm text-slate-500">
            <a href="https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-" 
               className="hover:text-white transition-colors"
               target="_blank" rel="noopener noreferrer">
              GitHub
            </a>
            <a href="#" className="hover:text-white transition-colors">
              Basescan
            </a>
            <a href="#" className="hover:text-white transition-colors">
              Discord
            </a>
          </div>
        </footer>
      </div>
    </main>
  )
}
