# Strategickhaos DAO - Trust Dashboard

> **Public "trust battery" dashboard that normies and regulators actually believe**

## Overview

A real-time transparency dashboard that shows:
- Current treasury balance (bank + on-chain)
- Running total sent to named charities with IRS receipts hashed
- Latest code release + reproducible build proof + OpenTimestamps hash on Bitcoin
- Live verification status

**This turns abstract "verifiability" into something your mom or a senator's staffer can grok in ten seconds.**

## Quick Start

```bash
cd trust-dashboard
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the dashboard.

## Features

### 📊 Treasury Overview
- Real-time balance from on-chain data
- Animated counters showing total received
- Visual 93/7 split breakdown

### 🏥 Charity Allocation
- List of GiveWell top charities
- EIN verification for each charity
- Running total distributed per charity
- Direct links to charity websites

### 🔐 Build Verification
- Source code hash verification
- Smart contract verification status
- OpenTimestamps Bitcoin attestation
- Cryptographic proof display

### 📜 Transaction History
- All splits and distributions
- Filterable by type
- Links to Basescan for verification

## Configuration

### Environment Variables

Create a `.env.local` file:

```bash
# On-chain data
NEXT_PUBLIC_SPLITTER_ADDRESS=0x...
NEXT_PUBLIC_DISTRIBUTOR_ADDRESS=0x...
NEXT_PUBLIC_CHAIN_ID=8453

# RPC
NEXT_PUBLIC_RPC_URL=https://mainnet.base.org

# Bank integration (optional)
BANK_API_KEY=your_bank_api_key
```

### Connecting to Real Data

To connect to actual on-chain data, update the hooks in `lib/hooks.ts`:

```typescript
import { useContractRead } from 'wagmi'
import { SPLITTER_ABI } from './abis'

export function useTreasuryStats() {
  const { data } = useContractRead({
    address: process.env.NEXT_PUBLIC_SPLITTER_ADDRESS,
    abi: SPLITTER_ABI,
    functionName: 'getEthStats',
  })
  
  return {
    totalReceived: data?.[0] || 0n,
    totalToCharity: data?.[1] || 0n,
    totalToOperations: data?.[2] || 0n,
  }
}
```

## Deployment

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to IPFS (ENS compatible)

```bash
npm run build
npm run export
ipfs add -r out/
```

Then update your ENS record to point to the IPFS hash.

## Architecture

```
trust-dashboard/
├── app/
│   ├── layout.tsx       # Root layout with metadata
│   ├── page.tsx         # Main dashboard page
│   └── globals.css      # Global styles
├── components/
│   ├── TrustMetrics.tsx      # Treasury overview
│   ├── CharityAllocation.tsx # Charity breakdown
│   ├── BuildVerification.tsx # Code verification
│   └── TransactionHistory.tsx # Tx history
├── lib/
│   ├── hooks.ts         # Data fetching hooks
│   └── utils.ts         # Utility functions
└── public/              # Static assets
```

## Customization

### Adding a Webcam Feed

To add a live webcam feed of the air-gapped signing laptop:

```typescript
// components/LiveFeed.tsx
export function LiveFeed() {
  return (
    <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700">
      <h2 className="text-xl font-semibold mb-4">📹 Live Signing Laptop</h2>
      <div className="aspect-video bg-black rounded-lg overflow-hidden">
        <iframe 
          src="your-webcam-stream-url"
          className="w-full h-full"
          allow="camera; microphone"
        />
      </div>
      <p className="text-sm text-slate-400 mt-2">
        Air-gapped hardware wallet signing station
      </p>
    </div>
  )
}
```

### Uploading Bank Statements

The dashboard supports manual bank statement uploads with cryptographic signatures:

1. Export CSV from your bank
2. Sign the CSV with your GPG key
3. Upload both files to the dashboard
4. The signature is verified and displayed

## Security Considerations

- Never expose private keys or API secrets in frontend code
- All sensitive operations should be server-side
- Bank data should be manually uploaded, not API-fetched
- Use environment variables for all configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See [LICENSE](../LICENSE)

---

**Built with 🔥 by Strategickhaos DAO LLC**

*Making trust verifiable, not required.*
