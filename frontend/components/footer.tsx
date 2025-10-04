"use client"

import { Sparkles, Twitter, Linkedin, Github } from "lucide-react"
import Link from "next/link"

export function Footer() {
  return (
    <footer className="border-t border-border/50 mt-32">
      <div className="container mx-auto px-6 py-12">
        <div className="grid md:grid-cols-4 gap-12">
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-lg bg-gradient-blue flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold glow-text">InvestAI</span>
            </div>
            <p className="text-muted-foreground text-sm leading-relaxed max-w-md">
              AI-powered investment screening platform that delivers VC-grade analysis in minutes. Make smarter
              investment decisions with multi-agent intelligence.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Product</h4>
            <ul className="space-y-3">
              <li>
                <Link href="/product" className="text-sm text-muted-foreground hover:text-cyan-400 transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <Link href="/app" className="text-sm text-muted-foreground hover:text-cyan-400 transition-colors">
                  Start Screening
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Connect</h4>
            <div className="flex items-center gap-4">
              <a
                href="#"
                className="w-10 h-10 rounded-lg glass flex items-center justify-center hover:bg-gradient-blue transition-colors group"
              >
                <Twitter className="w-5 h-5 text-muted-foreground group-hover:text-white transition-colors" />
              </a>
              <a
                href="#"
                className="w-10 h-10 rounded-lg glass flex items-center justify-center hover:bg-gradient-blue transition-colors group"
              >
                <Linkedin className="w-5 h-5 text-muted-foreground group-hover:text-white transition-colors" />
              </a>
              <a
                href="#"
                className="w-10 h-10 rounded-lg glass flex items-center justify-center hover:bg-gradient-blue transition-colors group"
              >
                <Github className="w-5 h-5 text-muted-foreground group-hover:text-white transition-colors" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-border/50 mt-12 pt-8 text-center">
          <p className="text-sm text-muted-foreground">© 2025 InvestAI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
