"use client"

import { motion } from "framer-motion"
import { Sparkles } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

export function Navbar() {
  const pathname = usePathname()

  return (
    <header className="container mx-auto px-6 py-8">
      <nav className="flex items-center justify-between">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-2">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-lg bg-gradient-blue flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold glow-text">InvestAI</span>
          </Link>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-8">
          <Link
            href="/"
            className={`text-sm font-medium transition-colors hover:text-cyan-400 ${
              pathname === "/" ? "text-cyan-400" : "text-muted-foreground"
            }`}
          >
            Home
          </Link>
          <Link
            href="/product"
            className={`text-sm font-medium transition-colors hover:text-cyan-400 ${
              pathname === "/product" ? "text-cyan-400" : "text-muted-foreground"
            }`}
          >
            Product
          </Link>
        </motion.div>
      </nav>
    </header>
  )
}
