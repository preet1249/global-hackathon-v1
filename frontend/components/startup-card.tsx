"use client"

import type React from "react"

import { motion, AnimatePresence } from "framer-motion"
import { ChevronDown, TrendingUp, Shield, Target, Users, FileDown } from "lucide-react"
import { Button } from "@/components/ui/button"

interface Startup {
  id: number
  name: string
  logo: string
  tagline: string
  fitScore: number
  sector: string
  stage: string
  metrics: {
    successRate: number
    marketFit: number
    techCredibility: number
    competition: number
  }
  detailedAnalysis?: string
}

interface StartupCardProps {
  startup: Startup
  isSelected: boolean
  onSelect: () => void
  onDownload: () => void
}

export function StartupCard({ startup, isSelected, onSelect, onDownload }: StartupCardProps) {
  return (
    <motion.div
      className="glass rounded-xl sm:rounded-2xl overflow-hidden hover-glow transition-all cursor-pointer"
      whileHover={{ y: -4 }}
      onClick={onSelect}
    >
      <div className="p-4 sm:p-6">
        <div className="flex items-start justify-between mb-4 gap-3">
          <div className="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
            <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-xl bg-gradient-blue flex items-center justify-center text-xl sm:text-2xl flex-shrink-0">
              {startup.logo}
            </div>
            <div className="min-w-0 flex-1">
              <h3 className="text-base sm:text-xl font-semibold mb-1 text-foreground truncate">{startup.name}</h3>
              <p className="text-xs sm:text-sm text-foreground/60 line-clamp-2">{startup.tagline}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 sm:gap-4 flex-shrink-0">
            <div className="text-right">
              <p className="text-[10px] sm:text-xs text-foreground/60 mb-1">Fit Score</p>
              <div className="flex items-center gap-1 sm:gap-2">
                <motion.div
                  className="text-2xl sm:text-3xl font-bold text-[#00D1FF]"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 200 }}
                >
                  {startup.fitScore}
                </motion.div>
                <span className="text-foreground/40 text-xs sm:text-sm">/100</span>
              </div>
            </div>
            <motion.div animate={{ rotate: isSelected ? 180 : 0 }} transition={{ duration: 0.3 }}>
              <ChevronDown className="w-5 h-5 sm:w-6 sm:h-6 text-foreground/60" />
            </motion.div>
          </div>
        </div>

        <div className="flex gap-2 mb-4">
          <span className="px-2.5 sm:px-3 py-1 rounded-full bg-[#00D1FF]/10 text-[#00D1FF] text-xs sm:text-sm font-medium border border-[#00D1FF]/20">
            {startup.sector}
          </span>
          <span className="px-2.5 sm:px-3 py-1 rounded-full bg-foreground/5 text-foreground/80 text-xs sm:text-sm font-medium border border-foreground/10">
            {startup.stage}
          </span>
        </div>

        <AnimatePresence>
          {isSelected && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="pt-4 sm:pt-6 border-t border-foreground/10 mt-4">
                <div className="grid grid-cols-2 gap-3 sm:gap-4 mb-4 sm:mb-6">
                  <MetricItem
                    icon={<TrendingUp className="w-3.5 h-3.5 sm:w-4 sm:h-4" />}
                    label="Success Rate"
                    value={startup.metrics.successRate}
                  />
                  <MetricItem
                    icon={<Target className="w-3.5 h-3.5 sm:w-4 sm:h-4" />}
                    label="Market Fit"
                    value={startup.metrics.marketFit}
                  />
                  <MetricItem
                    icon={<Shield className="w-3.5 h-3.5 sm:w-4 sm:h-4" />}
                    label="Tech Credibility"
                    value={startup.metrics.techCredibility}
                  />
                  <MetricItem
                    icon={<Users className="w-3.5 h-3.5 sm:w-4 sm:h-4" />}
                    label="Competition"
                    value={startup.metrics.competition}
                  />
                </div>

                {startup.detailedAnalysis && (
                  <div className="mb-4 sm:mb-6 p-4 rounded-lg bg-foreground/5 border border-foreground/10">
                    <h4 className="text-sm sm:text-base font-semibold mb-3 text-[#00D1FF]">Detailed Analysis</h4>
                    <p className="text-xs sm:text-sm text-foreground/80 leading-relaxed whitespace-pre-line">
                      {startup.detailedAnalysis}
                    </p>
                  </div>
                )}

                <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
                  <Button className="flex-1 bg-gradient-blue hover:opacity-90 text-white hover-glow text-sm sm:text-base">
                    View Full Report
                  </Button>
                  <Button
                    variant="outline"
                    onClick={(e) => {
                      e.stopPropagation()
                      onDownload()
                    }}
                    className="flex-1 bg-transparent border-foreground/20 hover:border-[#00D1FF] hover:text-[#00D1FF] hover-glow text-sm sm:text-base gap-2"
                  >
                    <FileDown className="w-4 h-4" />
                    Download 1-Pager
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  )
}

function MetricItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode
  label: string
  value: number
}) {
  return (
    <div>
      <div className="flex items-center gap-1.5 sm:gap-2 mb-1.5 sm:mb-2">
        <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-gradient-blue flex items-center justify-center text-white flex-shrink-0">
          {icon}
        </div>
        <span className="text-xs sm:text-sm text-foreground/60 truncate">{label}</span>
      </div>
      <div className="flex items-end gap-1 mb-1.5 sm:mb-2">
        <span className="text-xl sm:text-2xl font-bold text-foreground">{value}</span>
        <span className="text-foreground/40 text-xs sm:text-sm mb-0.5">/100</span>
      </div>
      <div className="h-1 sm:h-1.5 bg-foreground/5 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-gradient-blue"
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1, delay: 0.2 }}
        />
      </div>
    </div>
  )
}
