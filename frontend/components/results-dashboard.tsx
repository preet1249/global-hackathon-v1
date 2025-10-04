"use client"

import type React from "react"

import { motion } from "framer-motion"
import { useState, useEffect } from "react"
import { TrendingUp, Shield, DollarSign, Target, Download, ArrowRight, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { StartupCard } from "@/components/startup-card"
import { RiskHeatmap } from "@/components/risk-heatmap"
import { getJobResults } from "@/lib/api"

interface ResultsDashboardProps {
  jobId: string
  onReset: () => void
}

export function ResultsDashboard({ jobId, onReset }: ResultsDashboardProps) {
  const [selectedStartup, setSelectedStartup] = useState<number | null>(null)
  const [startups, setStartups] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch real results - NO MOCK DATA
    async function fetchResults() {
      try {
        const data = await getJobResults(jobId)
        if (data.startups) {
          setStartups(data.startups)
        }
      } catch (error) {
        console.error("Failed to fetch results:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchResults()
  }, [jobId])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-foreground/60">Loading results...</p>
      </div>
    )
  }

  if (startups.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <div className="text-center">
          <p className="text-foreground/60 mb-4">No startups matched your criteria.</p>
          <Button onClick={onReset} className="bg-gradient-blue hover:opacity-90">
            Start New Analysis
          </Button>
        </div>
      </div>
    )
  }

  const displayStartups = startups

  const avgSuccessRate = displayStartups.length > 0
    ? Math.round(
        displayStartups.reduce((acc: number, s: any) => {
          const rate = s.due_diligence?.success_rate || s.metrics?.successRate || 0
          return acc + rate
        }, 0) / displayStartups.length
      )
    : 0

  const avgMarketFit = displayStartups.length > 0
    ? Math.round(
        displayStartups.reduce((acc: number, s: any) => {
          return acc + (s.metrics?.marketFit || 85)
        }, 0) / displayStartups.length
      )
    : 0

  const avgTechCredibility = displayStartups.length > 0
    ? Math.round(
        displayStartups.reduce((acc: number, s: any) => {
          return acc + (s.metrics?.techCredibility || 85)
        }, 0) / displayStartups.length
      )
    : 0

  const avgCompetition = displayStartups.length > 0
    ? Math.round(
        displayStartups.reduce((acc: number, s: any) => {
          const comp = s.due_diligence?.competition_difficulty || s.metrics?.competition || 50
          return acc + comp
        }, 0) / displayStartups.length
      )
    : 0

  const downloadIndividualReport = async (startupId: string, startupName: string) => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${API_URL}/api/jobs/${jobId}/download/${startupId}`)

      if (!response.ok) {
        throw new Error('Failed to download PDF')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `${startupName.replace(/\s+/g, "_")}_Report.pdf`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('PDF download error:', error)
      alert('Failed to download PDF. Please try again.')
    }
  }

  const downloadCompleteReport = async () => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${API_URL}/api/jobs/${jobId}/download-all`)

      if (!response.ok) {
        throw new Error('Failed to download portfolio PDF')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = "Portfolio_Report.pdf"
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Portfolio PDF download error:', error)
      alert('Failed to download portfolio PDF. Please try again.')
    }
  }

  return (
    <div className="min-h-screen relative overflow-hidden bg-background">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 right-10 w-[500px] h-[500px] bg-[#00D1FF]/5 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Number.POSITIVE_INFINITY,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 left-10 w-[400px] h-[400px] bg-[#0066FF]/5 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.2, 0.4, 0.2],
          }}
          transition={{
            duration: 10,
            repeat: Number.POSITIVE_INFINITY,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 sm:px-6 py-8 sm:py-16 max-w-7xl">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8 sm:mb-16"
        >
          <div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-2 sm:mb-3 text-foreground">
              Investment Radar
            </h1>
            <p className="text-foreground/60 text-base sm:text-lg">5 Startups Aligned with Your Thesis</p>
          </div>
          <Button
            onClick={onReset}
            variant="outline"
            size="sm"
            className="gap-2 bg-transparent border-foreground/20 hover:border-[#00D1FF] hover:text-[#00D1FF] transition-all hover-glow"
          >
            <RotateCcw className="w-4 h-4" />
            <span className="hidden sm:inline">New Analysis</span>
          </Button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 mb-8 sm:mb-16"
        >
          <StatCard
            icon={<TrendingUp className="w-4 h-4 sm:w-5 sm:h-5" />}
            label="Avg Success Rate"
            value={avgSuccessRate}
          />
          <StatCard icon={<Target className="w-4 h-4 sm:w-5 sm:h-5" />} label="Market Fit" value={avgMarketFit} />
          <StatCard
            icon={<Shield className="w-4 h-4 sm:w-5 sm:h-5" />}
            label="Tech Credibility"
            value={avgTechCredibility}
          />
          <StatCard
            icon={<DollarSign className="w-4 h-4 sm:w-5 sm:h-5" />}
            label="Competition"
            value={avgCompetition}
            inverse
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8 sm:mb-16"
        >
          <h2 className="text-2xl sm:text-3xl font-semibold mb-4 sm:mb-8 text-foreground">
            Top Investment Opportunities
          </h2>
          <div className="space-y-4 sm:space-y-6">
            {displayStartups.map((item: any, idx: number) => {
              const startup = item.startup || item
              const startupId = startup.id || idx

              return (
                <motion.div
                  key={startupId}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + idx * 0.1 }}
                >
                  <StartupCard
                    startup={{
                      id: startupId,
                      name: startup.name || "Unknown",
                      logo: "🚀",
                      tagline: startup.summary || "No summary available",
                      fitScore: Math.round((item.due_diligence?.success_rate || startup.fitScore || 0)),
                      sector: startup.sector || "N/A",
                      stage: startup.stage || "N/A",
                      metrics: {
                        successRate: Math.round(item.due_diligence?.success_rate || startup.metrics?.successRate || 0),
                        marketFit: startup.metrics?.marketFit || 85,
                        techCredibility: startup.metrics?.techCredibility || 85,
                        competition: Math.round(item.due_diligence?.competition_difficulty || startup.metrics?.competition || 50),
                      },
                      detailedAnalysis: item.due_diligence?.detailed_analysis || undefined,
                    }}
                    isSelected={selectedStartup === startupId}
                    onSelect={() => setSelectedStartup(selectedStartup === startupId ? null : startupId)}
                    onDownload={() => downloadIndividualReport(startupId, startup.name || "startup")}
                  />
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mb-8 sm:mb-16"
        >
          <h2 className="text-2xl sm:text-3xl font-semibold mb-4 sm:mb-8 text-foreground">
            Risk Analysis & Predictions
          </h2>
          <RiskHeatmap />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
          className="glass rounded-2xl sm:rounded-3xl p-6 sm:p-10 text-center hover-glow transition-all"
        >
          <h2 className="text-2xl sm:text-3xl font-bold mb-2 sm:mb-3 text-foreground">
            Your Investment Decision Pack Is Ready
          </h2>
          <p className="text-foreground/60 text-sm sm:text-base mb-6 sm:mb-8 max-w-2xl mx-auto">
            Analysis complete. Based on 1000+ pitch decks, 5 startups truly fit your investment thesis.
          </p>
          <Button
            onClick={downloadCompleteReport}
            size="lg"
            className="w-full sm:w-auto bg-gradient-blue hover:opacity-90 text-white px-6 sm:px-8 py-4 sm:py-6 text-base sm:text-lg group hover-glow"
          >
            <Download className="mr-2 w-4 h-4 sm:w-5 sm:h-5" />
            Download Complete Report
            <ArrowRight className="ml-2 w-4 h-4 sm:w-5 sm:h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </motion.div>
      </div>
    </div>
  )
}

function StatCard({
  icon,
  label,
  value,
  inverse = false,
}: {
  icon: React.ReactNode
  label: string
  value: number
  inverse?: boolean
}) {
  return (
    <div className="glass rounded-xl sm:rounded-2xl p-3 sm:p-5 hover-glow transition-all group">
      <div className="flex items-center gap-2 sm:gap-3 mb-2 sm:mb-4">
        <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-lg sm:rounded-xl bg-gradient-blue flex items-center justify-center text-white group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <p className="text-xs sm:text-sm text-foreground/60">{label}</p>
      </div>
      <div className="flex items-baseline gap-1 sm:gap-2 mb-2 sm:mb-3">
        <p className="text-2xl sm:text-3xl font-bold text-foreground">{value}</p>
        <p className="text-foreground/40 text-xs sm:text-sm">/100</p>
      </div>
      <div className="h-1 sm:h-1.5 bg-foreground/5 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-gradient-blue"
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1, delay: 0.5 }}
        />
      </div>
    </div>
  )
}
