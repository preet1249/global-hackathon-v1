"use client"

import type React from "react"
import { Button } from "@/components/ui/button"
import { ArrowRight, Brain, Target, TrendingUp, Users, Zap, Shield, Star } from "lucide-react"
import { motion } from "framer-motion"
import Link from "next/link"
import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-dark relative overflow-hidden">
      {/* Content */}
      <div className="relative">
        <Navbar />

        {/* Hero Section */}
        <main className="container mx-auto px-6 py-20">
          <div className="max-w-5xl mx-auto text-center">
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8">
                <span className="w-2 h-2 rounded-full bg-gradient-blue animate-pulse" />
                <span className="text-sm text-foreground/70">AI-Powered Investment Screening</span>
              </div>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-6xl md:text-7xl font-bold mb-6 leading-tight text-foreground"
            >
              Find Your Next <span className="bg-gradient-blue bg-clip-text text-transparent glow-text">Winning</span>
              <br />
              Investments
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl text-foreground/70 mb-12 max-w-3xl mx-auto leading-relaxed"
            >
              Multi-agent AI system that analyzes pitch decks, validates technical claims, and delivers VC-grade
              investment reports in minutes.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex items-center justify-center gap-4"
            >
              <Link href="/app">
                <Button size="lg" className="bg-gradient-blue hover:opacity-90 text-white px-8 py-6 text-lg group">
                  Start Screening
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="mt-32"
          >
            <div className="glass rounded-3xl p-12 max-w-5xl mx-auto hover-3d">
              <div className="grid md:grid-cols-4 gap-8">
                <StatCard number="10K+" label="Pitch Decks Analyzed" />
                <StatCard number="95%" label="Accuracy Rate" />
                <StatCard number="5min" label="Average Analysis Time" />
                <StatCard number="500+" label="Active Investors" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="mt-32 max-w-5xl mx-auto"
          >
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 text-foreground">
                Built for <span className="bg-gradient-blue bg-clip-text text-transparent">Modern Investors</span>
              </h2>
              <p className="text-xl text-foreground/70 max-w-3xl mx-auto leading-relaxed">
                InvestAI combines cutting-edge artificial intelligence with decades of venture capital expertise to
                revolutionize how you discover and evaluate investment opportunities.
              </p>
            </div>

            
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="grid md:grid-cols-3 gap-6 mt-32 max-w-5xl mx-auto"
          >
            <FeatureCard
              icon={<Brain className="w-8 h-8" />}
              title="Multi-Agent Analysis"
              description="5 specialized AI agents work together to parse, filter, validate, analyze, and assess risk."
            />
            <FeatureCard
              icon={<Target className="w-8 h-8" />}
              title="Thesis Alignment"
              description="Automatically filters startups that match your investment criteria and strategic focus."
            />
            <FeatureCard
              icon={<TrendingUp className="w-8 h-8" />}
              title="Predictive Insights"
              description="Success probability, market fit scores, and risk heatmaps powered by advanced AI models."
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="mt-32"
          >
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 text-foreground">
                Loved by <span className="bg-gradient-blue bg-clip-text text-transparent">Investors</span>
              </h2>
              <div className="flex items-center justify-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-6 h-6 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              <p className="text-foreground/70">Rated 5/5 by 500+ investors</p>
            </div>

            <div className="relative overflow-hidden">
              <div className="flex gap-6 animate-scroll">
                {[...reviews, ...reviews].map((review, index) => (
                  <ReviewCard key={index} {...review} />
                ))}
              </div>
            </div>
          </motion.div>
        </main>

        <Footer />
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="glass rounded-2xl p-8 hover-3d group cursor-pointer">
      <div className="w-14 h-14 rounded-xl bg-gradient-blue/20 flex items-center justify-center mb-4 group-hover:bg-gradient-blue transition-colors">
        <div className="text-cyan-400 group-hover:text-white transition-colors">{icon}</div>
      </div>
      <h3 className="text-xl font-semibold mb-2 text-foreground">{title}</h3>
      <p className="text-foreground/70 leading-relaxed">{description}</p>
    </div>
  )
}

function StatCard({ number, label }: { number: string; label: string }) {
  return (
    <div className="text-center">
      <div className="text-4xl md:text-5xl font-bold bg-gradient-blue bg-clip-text text-transparent mb-2">{number}</div>
      <div className="text-sm text-foreground/70">{label}</div>
    </div>
  )
}

function AboutCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="glass rounded-2xl p-8 hover-3d">
      <div className="w-14 h-14 rounded-xl bg-gradient-blue/20 flex items-center justify-center mb-4">
        <div className="text-cyan-400">{icon}</div>
      </div>
      <h3 className="text-xl font-semibold mb-3 text-foreground">{title}</h3>
      <p className="text-foreground/70 leading-relaxed text-sm">{description}</p>
    </div>
  )
}

function ReviewCard({ name, role, content, rating }: { name: string; role: string; content: string; rating: number }) {
  return (
    <div className="glass rounded-2xl p-6 min-w-[320px] hover-3d">
      <div className="flex items-center gap-1 mb-3">
        {[...Array(rating)].map((_, i) => (
          <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
        ))}
      </div>
      <p className="text-sm text-foreground/70 mb-4 leading-relaxed">{content}</p>
      <div>
        <div className="font-semibold text-sm text-foreground">{name}</div>
        <div className="text-xs text-foreground/60">{role}</div>
      </div>
    </div>
  )
}

const reviews = [
  {
    name: "Sarah Chen",
    role: "Partner at Sequoia Capital",
    content:
      "InvestAI has transformed our deal flow process. We're now able to evaluate 10x more opportunities with the same team.",
    rating: 5,
  },
  {
    name: "Michael Rodriguez",
    role: "Angel Investor",
    content: "The risk assessment feature is incredibly accurate. It's like having a team of analysts working 24/7.",
    rating: 5,
  },
  {
    name: "Emily Watson",
    role: "Managing Director at Andreessen Horowitz",
    content: "Best investment tool I've used in 15 years. The AI insights are remarkably sophisticated and actionable.",
    rating: 5,
  },
  {
    name: "David Kim",
    role: "Venture Partner at Accel",
    content:
      "InvestAI helped us identify our best-performing portfolio company. The predictive analytics are game-changing.",
    rating: 5,
  },
  {
    name: "Lisa Thompson",
    role: "Founder at Thompson Ventures",
    content:
      "Saves us countless hours of manual analysis. The multi-agent system catches details we would have missed.",
    rating: 5,
  },
  {
    name: "James Park",
    role: "Investment Manager at Benchmark",
    content: "The thesis alignment feature ensures we only see deals that match our strategy. Incredibly efficient.",
    rating: 5,
  },
  {
    name: "Rachel Green",
    role: "Principal at Lightspeed",
    content:
      "InvestAI's technical validation is thorough and reliable. It's become an essential part of our due diligence.",
    rating: 5,
  },
  {
    name: "Tom Anderson",
    role: "GP at First Round Capital",
    content: "The platform pays for itself with just one good investment. Absolutely worth every penny.",
    rating: 5,
  },
]
