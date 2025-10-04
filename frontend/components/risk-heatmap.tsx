"use client"

import { motion } from "framer-motion"
import { TrendingUp, Shield, DollarSign, AlertTriangle } from "lucide-react"

const riskData = {
  techRisk: 28,
  marketRisk: 35,
  financeRisk: 22,
  complianceRisk: 18,
}

const predictions = [
  { label: "Success Probability", value: 84, icon: TrendingUp },
  { label: "Competition Difficulty", value: 37, icon: Shield },
  { label: "Revenue Projection", value: "$18M", icon: DollarSign, isText: true },
  { label: "Profit Margin", value: "24%", icon: AlertTriangle, isText: true },
]

export function RiskHeatmap() {
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      {/* Hexagonal Radar Chart */}
      <div className="glass rounded-2xl p-8 hover-glow transition-all">
        <h3 className="text-2xl font-semibold mb-8 text-foreground">Risk Heatmap</h3>
        <div className="relative w-full aspect-square max-w-md mx-auto">
          <svg viewBox="0 0 200 200" className="w-full h-full">
            {/* Background hexagon grid */}
            {[100, 75, 50, 25].map((size, idx) => (
              <polygon
                key={idx}
                points={getHexagonPoints(100, 100, size)}
                fill="none"
                stroke="rgba(255,255,255,0.05)"
                strokeWidth="1"
              />
            ))}

            {/* Axis lines */}
            {[0, 60, 120, 180, 240, 300].map((angle, idx) => {
              const x = 100 + 80 * Math.cos(((angle - 90) * Math.PI) / 180)
              const y = 100 + 80 * Math.sin(((angle - 90) * Math.PI) / 180)
              return <line key={idx} x1="100" y1="100" x2={x} y2={y} stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
            })}

            {/* Data polygon */}
            <motion.polygon
              points={getRiskPolygonPoints(100, 100, riskData)}
              fill="url(#risk-gradient)"
              fillOpacity="0.4"
              stroke="#00D1FF"
              strokeWidth="2"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 1, type: "spring" }}
            />

            {/* Data points */}
            {Object.values(riskData).map((value, idx) => {
              const angle = idx * 90 - 90
              const radius = (value / 100) * 80
              const x = 100 + radius * Math.cos((angle * Math.PI) / 180)
              const y = 100 + radius * Math.sin((angle * Math.PI) / 180)
              return (
                <motion.circle
                  key={idx}
                  cx={x}
                  cy={y}
                  r="4"
                  fill="#00D1FF"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.5 + idx * 0.1 }}
                />
              )
            })}

            <defs>
              <linearGradient id="risk-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00D1FF" />
                <stop offset="100%" stopColor="#0066FF" />
              </linearGradient>
            </defs>
          </svg>

          {/* Labels */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-6 text-sm font-medium text-foreground/80">
            Tech Risk
          </div>
          <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-16 text-sm font-medium text-foreground/80">
            Market Risk
          </div>
          <div className="absolute bottom-0 right-1/4 translate-y-6 text-sm font-medium text-foreground/80">
            Finance
          </div>
          <div className="absolute bottom-0 left-1/4 translate-y-6 text-sm font-medium text-foreground/80">
            Compliance
          </div>
        </div>
      </div>

      {/* Predictions */}
      <div className="glass rounded-2xl p-8 hover-glow transition-all">
        <h3 className="text-2xl font-semibold mb-8 text-foreground">Key Predictions</h3>
        <div className="space-y-6">
          {predictions.map((prediction, idx) => {
            const Icon = prediction.icon
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="relative"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-gradient-blue flex items-center justify-center text-white">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="font-medium text-foreground">{prediction.label}</span>
                  </div>
                  <span className="text-2xl font-bold text-foreground">
                    {prediction.value}
                    {!prediction.isText && "/100"}
                  </span>
                </div>
                {!prediction.isText && (
                  <div className="h-2 bg-foreground/5 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-blue relative"
                      initial={{ width: 0 }}
                      animate={{ width: `${prediction.value}%` }}
                      transition={{ duration: 1, delay: 0.5 + idx * 0.1 }}
                    >
                      {/* Sparkline effect */}
                      <motion.div
                        className="absolute inset-0 bg-white/30"
                        initial={{ x: "-100%" }}
                        animate={{ x: "200%" }}
                        transition={{
                          duration: 2,
                          repeat: Number.POSITIVE_INFINITY,
                          repeatDelay: 1,
                          ease: "easeInOut",
                        }}
                      />
                    </motion.div>
                  </div>
                )}
              </motion.div>
            )
          })}
        </div>
        <p className="text-xs text-foreground/50 mt-6 italic">Calculated from Agent 5 (Grok) consolidated data</p>
      </div>
    </div>
  )
}

function getHexagonPoints(cx: number, cy: number, radius: number): string {
  const points = []
  for (let i = 0; i < 6; i++) {
    const angle = ((i * 60 - 90) * Math.PI) / 180
    const x = cx + radius * Math.cos(angle)
    const y = cy + radius * Math.sin(angle)
    points.push(`${x},${y}`)
  }
  return points.join(" ")
}

function getRiskPolygonPoints(cx: number, cy: number, data: typeof riskData): string {
  const values = [data.techRisk, data.marketRisk, data.financeRisk, data.complianceRisk]
  const points = []

  values.forEach((value, idx) => {
    const angle = ((idx * 90 - 90) * Math.PI) / 180
    const radius = (value / 100) * 80
    const x = cx + radius * Math.cos(angle)
    const y = cy + radius * Math.sin(angle)
    points.push(`${x},${y}`)
  })

  return points.join(" ")
}
