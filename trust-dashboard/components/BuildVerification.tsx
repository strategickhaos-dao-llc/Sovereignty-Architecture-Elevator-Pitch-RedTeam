'use client'

import { useState } from 'react'

// Mock build verification data
const BUILD_INFO = {
  version: '1.0.0',
  gitCommit: 'abc123def456',
  buildTime: '2024-01-15T10:30:00Z',
  contractsHash: 'a1b2c3d4e5f6...',
  legalHash: 'f6e5d4c3b2a1...',
  openTimestampsProof: 'pending',
  lastVerified: new Date().toISOString(),
}

const CONTRACTS = [
  {
    name: 'IrrevocableCharitySplitter',
    address: '0x1234...5678',
    network: 'Base',
    verified: true,
    deployedAt: '2024-01-10T12:00:00Z',
  },
  {
    name: 'MerkleCharityDistributor',
    address: '0x8765...4321',
    network: 'Base',
    verified: true,
    deployedAt: '2024-01-10T12:05:00Z',
  },
]

export function BuildVerification() {
  const [showHashes, setShowHashes] = useState(false)
  
  return (
    <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
      <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
        <span className="text-2xl">🔐</span>
        Build Verification
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Code Verification */}
        <div className="bg-slate-700/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
              <span>✓</span>
            </div>
            <span className="font-medium">Source Code</span>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Version</span>
              <span className="font-mono">v{BUILD_INFO.version}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Commit</span>
              <span className="font-mono text-xs">{BUILD_INFO.gitCommit}</span>
            </div>
            <a 
              href="https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-"
              target="_blank"
              rel="noopener noreferrer"
              className="block text-dao-primary hover:underline mt-2"
            >
              View on GitHub →
            </a>
          </div>
        </div>
        
        {/* Contract Verification */}
        <div className="bg-slate-700/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
              <span>✓</span>
            </div>
            <span className="font-medium">Smart Contracts</span>
          </div>
          <div className="space-y-2 text-sm">
            {CONTRACTS.map((contract) => (
              <div key={contract.address} className="flex justify-between items-center">
                <span className="text-slate-400 text-xs">{contract.name}</span>
                <div className="flex items-center gap-1">
                  {contract.verified && (
                    <span className="text-green-500 text-xs">Verified</span>
                  )}
                </div>
              </div>
            ))}
            <a 
              href="#"
              className="block text-dao-primary hover:underline mt-2"
            >
              View on Basescan →
            </a>
          </div>
        </div>
        
        {/* OpenTimestamps */}
        <div className="bg-slate-700/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 bg-yellow-500/20 rounded-full flex items-center justify-center">
              <span>⏳</span>
            </div>
            <span className="font-medium">OpenTimestamps</span>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Status</span>
              <span className="text-yellow-500">Pending</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Network</span>
              <span>Bitcoin</span>
            </div>
            <p className="text-xs text-slate-400 mt-2">
              Proof anchored to Bitcoin blockchain for permanent timestamping
            </p>
          </div>
        </div>
      </div>
      
      {/* Hash Details (Expandable) */}
      <div className="mt-6">
        <button
          onClick={() => setShowHashes(!showHashes)}
          className="text-sm text-slate-400 hover:text-white transition-colors"
        >
          {showHashes ? '▼' : '▶'} Show cryptographic hashes
        </button>
        
        {showHashes && (
          <div className="mt-4 bg-slate-900/50 rounded-lg p-4 font-mono text-xs overflow-x-auto">
            <div className="space-y-2">
              <div>
                <span className="text-slate-400">contracts_sha256: </span>
                <span className="text-green-400">{BUILD_INFO.contractsHash}</span>
              </div>
              <div>
                <span className="text-slate-400">legal_docs_sha256: </span>
                <span className="text-green-400">{BUILD_INFO.legalHash}</span>
              </div>
              <div>
                <span className="text-slate-400">ots_proof: </span>
                <span className="text-yellow-400">{BUILD_INFO.openTimestampsProof}</span>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* 7% Forever Badge */}
      <div className="mt-6 flex justify-center">
        <div className="inline-flex items-center gap-2 px-6 py-3 bg-dao-charity/20 rounded-full border border-dao-charity/40">
          <span className="text-2xl">🔒</span>
          <div>
            <div className="font-bold text-dao-charity">7% FOREVER</div>
            <div className="text-xs text-slate-400">Mathematically Irrevocable</div>
          </div>
        </div>
      </div>
    </div>
  )
}
