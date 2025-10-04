import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'VC Multi-Agent Platform',
  description: 'AI-powered startup due diligence platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
