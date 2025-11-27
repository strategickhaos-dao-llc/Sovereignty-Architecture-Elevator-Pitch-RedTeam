'use client'

import { useState } from 'react'

// GiveWell top charities
const CHARITIES = [
  {
    name: 'Against Malaria Foundation',
    ein: '20-8521450',
    allocation: 25,
    distributed: 269.86,
    website: 'https://www.againstmalaria.com/',
    description: 'Distributes insecticide-treated bed nets to prevent malaria',
    color: '#10b981',
  },
  {
    name: 'Helen Keller International',
    ein: '13-5562162',
    allocation: 25,
    distributed: 269.86,
    website: 'https://www.hki.org/',
    description: 'Vitamin A supplementation to prevent blindness and death',
    color: '#f59e0b',
  },
  {
    name: 'Malaria Consortium',
    ein: '98-0627052',
    allocation: 25,
    distributed: 269.86,
    website: 'https://www.malariaconsortium.org/',
    description: 'Seasonal malaria chemoprevention for children',
    color: '#3b82f6',
  },
  {
    name: 'New Incentives',
    ein: '45-3321264',
    allocation: 25,
    distributed: 269.86,
    website: 'https://www.newincentives.org/',
    description: 'Cash transfers to increase childhood vaccination in Nigeria',
    color: '#8b5cf6',
  },
]

export function CharityAllocation() {
  const [expandedCharity, setExpandedCharity] = useState<string | null>(null)
  
  const totalDistributed = CHARITIES.reduce((sum, c) => sum + c.distributed, 0)
  
  return (
    <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
      <h2 className="text-xl font-semibold mb-2 flex items-center gap-2">
        <span className="text-2xl">🏥</span>
        Charity Allocation
      </h2>
      <p className="text-sm text-slate-400 mb-6">
        7% distributed pro-rata to GiveWell top charities
      </p>
      
      {/* Total Counter */}
      <div className="bg-dao-charity/10 rounded-xl p-4 border border-dao-charity/30 mb-6">
        <div className="text-sm text-dao-charity mb-1">Total to Charity Forever</div>
        <div className="text-3xl font-bold text-dao-charity">
          ${totalDistributed.toLocaleString('en-US', { minimumFractionDigits: 2 })}
        </div>
      </div>
      
      {/* Charity List */}
      <div className="space-y-3">
        {CHARITIES.map((charity) => (
          <div 
            key={charity.ein}
            className="bg-slate-700/30 rounded-xl overflow-hidden cursor-pointer hover:bg-slate-700/50 transition-colors"
            onClick={() => setExpandedCharity(
              expandedCharity === charity.ein ? null : charity.ein
            )}
          >
            <div className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: charity.color }}
                  />
                  <div>
                    <div className="font-medium text-white">{charity.name}</div>
                    <div className="text-xs text-slate-400">EIN: {charity.ein}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-white">
                    ${charity.distributed.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </div>
                  <div className="text-xs text-slate-400">{charity.allocation}%</div>
                </div>
              </div>
              
              {/* Expanded details */}
              {expandedCharity === charity.ein && (
                <div className="mt-4 pt-4 border-t border-slate-600">
                  <p className="text-sm text-slate-300 mb-3">{charity.description}</p>
                  <a 
                    href={charity.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-dao-charity hover:underline"
                    onClick={(e) => e.stopPropagation()}
                  >
                    Visit Website →
                  </a>
                </div>
              )}
            </div>
            
            {/* Progress bar */}
            <div 
              className="h-1 transition-all duration-500"
              style={{ 
                width: `${charity.allocation}%`, 
                backgroundColor: charity.color 
              }}
            />
          </div>
        ))}
      </div>
      
      {/* Verification Link */}
      <div className="mt-6 text-center">
        <a 
          href="#" 
          className="text-sm text-slate-400 hover:text-white transition-colors"
        >
          View all charity transactions on Basescan →
        </a>
      </div>
    </div>
  )
}
