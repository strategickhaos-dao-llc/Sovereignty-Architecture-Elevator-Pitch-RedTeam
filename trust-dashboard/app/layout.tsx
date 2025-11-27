import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Strategickhaos DAO - Trust Dashboard',
  description: 'Real-time transparency for treasury and charity allocations. 7% to charity, forever, no rug pulls.',
  openGraph: {
    title: 'Strategickhaos DAO - Trust Dashboard',
    description: '7% to charity, forever. Verify it on-chain.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
