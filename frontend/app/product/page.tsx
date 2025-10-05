"use client"

import type React from "react"

import { motion } from "framer-motion"
import {
  Upload,
  Filter,
  CheckCircle2,
  BarChart3,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  FileText,
  Brain,
  Target,
  TrendingUp,
  Shield,
} from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"

export default function ProductPage() {
  return (
    <div className="min-h-screen bg-gradient-dark relative overflow-hidden">
      <div className="relative">
        <Navbar />

        <main className="container mx-auto px-6 py-20">
          {/* Hero Section */}
          <div className="max-w-4xl mx-auto text-center mb-32">
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <span className="text-sm text-muted-foreground">How InvestAI Works</span>
              </div>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-5xl md:text-6xl font-bold mb-6 leading-tight"
            >
              Your AI-Powered
              <br />
              <span className="inline-block bg-gradient-blue bg-clip-text text-transparent glow-text">Investment Partner</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl text-muted-foreground leading-relaxed"
            >
              Discover how InvestAI transforms pitch decks into actionable investment insights using cutting-edge
              multi-agent AI technology.
            </motion.p>
          </div>

          {/* The Story */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="max-w-4xl mx-auto mb-32"
          >
            <div className="glass rounded-3xl p-12 hover-3d">
              <h2 className="text-3xl font-bold mb-6">The Challenge</h2>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Every day, venture capitalists and angel investors receive hundreds of pitch decks. Manually reviewing
                each one is time-consuming, expensive, and prone to human bias. Great opportunities slip through the
                cracks while mediocre ones consume valuable time.
              </p>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Traditional screening methods rely on gut feelings and surface-level metrics. They miss critical
                technical details, market signals, and risk factors that could make or break an investment.
              </p>
              <h2 className="text-3xl font-bold mb-6 mt-12">The Solution</h2>
              <p className="text-muted-foreground leading-relaxed">
                InvestAI changes everything. Our multi-agent AI system works like a team of expert analysts, each
                specializing in different aspects of investment evaluation. Together, they deliver comprehensive,
                unbiased reports in minutes—not weeks.
              </p>
            </div>
          </motion.div>

          {/* How It Works - Step by Step */}
          <div className="max-w-5xl mx-auto mb-32">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                How It <span className="inline-block bg-gradient-blue bg-clip-text text-transparent">Works</span>
              </h2>
              <p className="text-xl text-muted-foreground">Five intelligent agents working in perfect harmony</p>
            </motion.div>

            <div className="space-y-8">
              <StepCard
                number="01"
                icon={<Upload className="w-8 h-8" />}
                title="Upload Your Pitch Decks"
                description="Simply drag and drop your pitch deck PDFs. InvestAI supports multiple formats and can process dozens of decks simultaneously."
                details={[
                  "Accepts PDF, PowerPoint, and Google Slides",
                  "Batch upload up to 50 decks at once",
                  "Secure, encrypted file handling",
                  "Automatic text and image extraction",
                ]}
                delay={0.5}
              />

              <StepCard
                number="02"
                icon={<FileText className="w-8 h-8" />}
                title="Parser Agent Extracts Data"
                description="The Parser Agent reads every slide, extracting key information like company name, market size, revenue model, team credentials, and financial projections."
                details={[
                  "OCR technology for scanned documents",
                  "Identifies charts, graphs, and financial tables",
                  "Extracts team bios and credentials",
                  "Captures competitive landscape data",
                ]}
                delay={0.6}
              />

              <StepCard
                number="03"
                icon={<Filter className="w-8 h-8" />}
                title="Filter Agent Matches Your Thesis"
                description="The Filter Agent compares each startup against your investment criteria—industry focus, stage, geography, and strategic priorities."
                details={[
                  "Customizable investment thesis parameters",
                  "Industry and sector classification",
                  "Stage and funding round filtering",
                  "Geographic and market focus alignment",
                ]}
                delay={0.7}
              />

              <StepCard
                number="04"
                icon={<CheckCircle2 className="w-8 h-8" />}
                title="Validator Agent Verifies Claims"
                description="The Validator Agent fact-checks technical claims, validates market data, and cross-references team credentials against public databases."
                details={[
                  "Technical feasibility assessment",
                  "Market size and TAM verification",
                  "Team background validation",
                  "Patent and IP verification",
                ]}
                delay={0.8}
              />

              <StepCard
                number="05"
                icon={<Brain className="w-8 h-8" />}
                title="Analyzer Agent Evaluates Potential"
                description="The Analyzer Agent assesses business model viability, competitive positioning, growth potential, and calculates a success probability score."
                details={[
                  "Business model strength analysis",
                  "Competitive advantage assessment",
                  "Market timing and trends evaluation",
                  "Revenue and growth projections review",
                ]}
                delay={0.9}
              />

              <StepCard
                number="06"
                icon={<AlertTriangle className="w-8 h-8" />}
                title="Risk Agent Identifies Red Flags"
                description="The Risk Agent generates a comprehensive risk heatmap, highlighting potential concerns across market, technical, financial, and team dimensions."
                details={[
                  "Market risk assessment",
                  "Technical execution risks",
                  "Financial sustainability analysis",
                  "Team and operational risks",
                ]}
                delay={1.0}
              />
            </div>
          </div>

          {/* The Result */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1.1 }}
            className="max-w-4xl mx-auto mb-32"
          >
            <div className="glass rounded-3xl p-12 hover-3d">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 rounded-xl bg-gradient-blue flex items-center justify-center">
                  <BarChart3 className="w-8 h-8 text-white" />
                </div>
                <h2 className="text-3xl font-bold">The Result</h2>
              </div>
              <p className="text-muted-foreground leading-relaxed mb-6">
                Within minutes, you receive a comprehensive investment report for each startup, complete with:
              </p>
              <ul className="space-y-3 mb-8">
                <ResultItem icon={<Target />} text="Success probability score (0-100)" />
                <ResultItem icon={<TrendingUp />} text="Market fit and growth potential analysis" />
                <ResultItem icon={<Shield />} text="Risk heatmap with detailed breakdown" />
                <ResultItem icon={<CheckCircle2 />} text="Thesis alignment score" />
                <ResultItem icon={<Brain />} text="Key insights and recommendations" />
              </ul>
              <p className="text-muted-foreground leading-relaxed">
                All results are ranked and sortable, allowing you to focus on the most promising opportunities first.
                Export reports, share with your team, and make data-driven investment decisions with confidence.
              </p>
            </div>
          </motion.div>

          {/* CTA Section */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1.2 }}
            className="max-w-4xl mx-auto text-center"
          >
            <div className="glass rounded-3xl p-12 hover-3d">
              <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Investment Process?</h2>
              <p className="text-xl text-muted-foreground mb-8 leading-relaxed">
                Join hundreds of investors who are already using InvestAI to discover winning opportunities faster.
              </p>
              <Link href="/app">
                <Button size="lg" className="bg-gradient-blue hover:opacity-90 text-white px-8 py-6 text-lg group">
                  Start Screening Now
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            </div>
          </motion.div>
        </main>

        <Footer />
      </div>
    </div>
  )
}

function StepCard({
  number,
  icon,
  title,
  description,
  details,
  delay,
}: {
  number: string
  icon: React.ReactNode
  title: string
  description: string
  details: string[]
  delay: number
}) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -40 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6, delay }}
      className="glass rounded-3xl p-8 hover-3d"
    >
      <div className="flex items-start gap-6">
        <div className="flex-shrink-0">
          <div className="text-6xl font-bold inline-block bg-gradient-blue bg-clip-text text-transparent opacity-30">{number}</div>
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-blue/20 flex items-center justify-center">
              <div className="text-cyan-400">{icon}</div>
            </div>
            <h3 className="text-2xl font-bold">{title}</h3>
          </div>
          <p className="text-muted-foreground leading-relaxed mb-6">{description}</p>
          <ul className="space-y-2">
            {details.map((detail, index) => (
              <li key={index} className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">{detail}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </motion.div>
  )
}

function ResultItem({ icon, text }: { icon: React.ReactNode; text: string }) {
  return (
    <li className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-lg bg-gradient-blue/20 flex items-center justify-center flex-shrink-0">
        <div className="text-cyan-400 w-5 h-5">{icon}</div>
      </div>
      <span className="text-foreground">{text}</span>
    </li>
  )
}
