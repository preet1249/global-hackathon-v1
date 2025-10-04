"use client"

import { motion } from "framer-motion"
import { Brain, Filter, Search, BarChart3, Flame, Check } from "lucide-react"
import { useState, useEffect } from "react"
import { getJobStatus } from "@/lib/api"

const agents = [
  { name: "Qwen3-VL", icon: Brain, task: "Parsing pitch decks", x: 50, y: 20 },
  { name: "GPT-5 mini", icon: Filter, task: "Filtering deals", x: 20, y: 50 },
  { name: "DeepSeek", icon: Search, task: "Validating tech claims", x: 50, y: 50 },
  { name: "Gemini", icon: BarChart3, task: "Market analysis", x: 80, y: 50 },
  { name: "Grok", icon: Flame, task: "Risk assessment", x: 50, y: 80 },
]

const connections = [
  { from: 0, to: 1 }, // Qwen3 → GPT-5
  { from: 0, to: 2 }, // Qwen3 → DeepSeek
  { from: 1, to: 2 }, // GPT-5 → DeepSeek
  { from: 0, to: 3 }, // Qwen3 → Gemini
  { from: 2, to: 3 }, // DeepSeek → Gemini
  { from: 1, to: 4 }, // GPT-5 → Grok
  { from: 2, to: 4 }, // DeepSeek → Grok
  { from: 3, to: 4 }, // Gemini → Grok
]

interface ProgressViewProps {
  jobId: string
  onComplete: () => void
}

export function ProgressView({ jobId, onComplete }: ProgressViewProps) {
  const [activeAgent, setActiveAgent] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<number[]>([])
  const [statusMessage, setStatusMessage] = useState("Initializing...")

  useEffect(() => {
    // Poll job status every 3 seconds - NO MOCK DATA
    const pollInterval = setInterval(async () => {
      try {
        const jobData = await getJobStatus(jobId)

        // Update status message
        const progress = jobData.progress || {}
        setStatusMessage(progress.status_message || "Processing...")

        // Map job status to agent steps
        const status = jobData.status
        if (status === "parsing") {
          setActiveAgent(0)
          setCompletedSteps([])
        } else if (status === "filtering") {
          setActiveAgent(1)
          setCompletedSteps([0])
        } else if (status === "dd_running") {
          const percent = progress.percent || 60
          if (percent >= 60 && percent < 70) {
            setActiveAgent(2)
            setCompletedSteps([0, 1])
          } else if (percent >= 70 && percent < 80) {
            setActiveAgent(3)
            setCompletedSteps([0, 1, 2])
          } else {
            setActiveAgent(4)
            setCompletedSteps([0, 1, 2, 3])
          }
        } else if (status === "completed") {
          setCompletedSteps([0, 1, 2, 3, 4])
          clearInterval(pollInterval)
          setTimeout(() => onComplete(), 2000)
        } else if (status === "failed") {
          clearInterval(pollInterval)
          alert(`Job failed: ${jobData.error_log || "Unknown error"}`)
        }
      } catch (error) {
        console.error("Failed to poll job status:", error)
      }
    }, 3000)

    return () => clearInterval(pollInterval)
  }, [jobId, onComplete])

  return (
    <div className="min-h-screen relative overflow-hidden flex items-center justify-center bg-background">
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <svg className="absolute inset-0 w-full h-full" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet">
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="6" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <linearGradient id="brain-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#00D1FF" stopOpacity="0.9" />
              <stop offset="50%" stopColor="#0066FF" stopOpacity="0.7" />
              <stop offset="100%" stopColor="#00D1FF" stopOpacity="0.5" />
            </linearGradient>
            <radialGradient id="brain-radial" cx="50%" cy="50%">
              <stop offset="0%" stopColor="#00D1FF" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0066FF" stopOpacity="0.3" />
            </radialGradient>
          </defs>

          {/* Detailed anatomical brain structure - frontal lobe */}
          <motion.path
            d="M 300 150 Q 250 120 220 140 Q 190 160 180 190 Q 175 220 185 250"
            stroke="url(#brain-gradient)"
            strokeWidth="2"
            fill="none"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: "easeInOut" }}
          />

          {/* Parietal lobe */}
          <motion.path
            d="M 185 250 Q 180 280 190 310 Q 200 340 230 360"
            stroke="url(#brain-gradient)"
            strokeWidth="2"
            fill="none"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: "easeInOut", delay: 0.3 }}
          />

          {/* Temporal lobe */}
          <motion.path
            d="M 230 360 Q 260 380 300 390 Q 320 392 340 390"
            stroke="url(#brain-gradient)"
            strokeWidth="2"
            fill="none"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: "easeInOut", delay: 0.6 }}
          />

          {/* Occipital lobe - right side */}
          <motion.path
            d="M 340 390 Q 370 380 400 360 Q 430 340 440 310 Q 450 280 445 250"
            stroke="url(#brain-gradient)"
            strokeWidth="2"
            fill="none"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: "easeInOut", delay: 0.9 }}
          />

          {/* Frontal lobe - right side */}
          <motion.path
            d="M 445 250 Q 450 220 445 190 Q 440 160 410 140 Q 380 120 330 150"
            stroke="url(#brain-gradient)"
            strokeWidth="2"
            fill="none"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: "easeInOut", delay: 1.2 }}
          />

          {/* Corpus callosum - connecting both hemispheres */}
          <motion.path
            d="M 300 150 Q 315 145 330 150 M 230 360 Q 300 375 340 390 M 185 250 Q 315 240 445 250"
            stroke="url(#brain-gradient)"
            strokeWidth="1.5"
            fill="none"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 0.9 }}
            transition={{ duration: 3, ease: "easeInOut", delay: 1.5 }}
          />

          {/* Cerebellum */}
          <motion.ellipse
            cx="315"
            cy="420"
            rx="60"
            ry="35"
            stroke="url(#brain-gradient)"
            strokeWidth="1.5"
            fill="url(#brain-radial)"
            fillOpacity="0.1"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: "easeInOut", delay: 1.8 }}
          />

          {/* Brain stem */}
          <motion.path
            d="M 315 455 L 315 490"
            stroke="url(#brain-gradient)"
            strokeWidth="8"
            strokeLinecap="round"
            filter="url(#glow)"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 2, ease: "easeInOut", delay: 2.1 }}
          />

          {/* Detailed neural pathways with slower animations */}
          {Array.from({ length: 50 }).map((_, i) => {
            const angle = (i / 50) * Math.PI * 2
            const radius = 90 + Math.random() * 90
            const cx = 315 + Math.cos(angle) * radius
            const cy = 270 + Math.sin(angle) * radius
            const endAngle = angle + (Math.random() - 0.5) * Math.PI * 0.8
            const endRadius = radius + (Math.random() - 0.5) * 70
            const ex = 315 + Math.cos(endAngle) * endRadius
            const ey = 270 + Math.sin(endAngle) * endRadius

            return (
              <motion.line
                key={i}
                x1={cx}
                y1={cy}
                x2={ex}
                y2={ey}
                stroke="url(#brain-gradient)"
                strokeWidth="0.6"
                opacity="0.5"
                filter="url(#glow)"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: [0, 1, 0] }}
                transition={{
                  duration: 4 + Math.random() * 3,
                  repeat: Number.POSITIVE_INFINITY,
                  delay: Math.random() * 3,
                }}
              />
            )
          })}

          {/* Neuron nodes - pulsing brain cells with slower animation */}
          {Array.from({ length: 40 }).map((_, i) => {
            const angle = (i / 40) * Math.PI * 2
            const radius = 90 + Math.random() * 90
            const cx = 315 + Math.cos(angle) * radius
            const cy = 270 + Math.sin(angle) * radius

            return (
              <motion.circle
                key={i}
                cx={cx}
                cy={cy}
                r="2.5"
                fill="#00D1FF"
                filter="url(#glow)"
                animate={{
                  opacity: [0.4, 1, 0.4],
                  scale: [1, 1.8, 1],
                }}
                transition={{
                  duration: 3 + Math.random() * 2,
                  repeat: Number.POSITIVE_INFINITY,
                  delay: Math.random() * 3,
                }}
              />
            )
          })}
        </svg>
      </div>

      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full blur-[120px]"
          style={{
            background: "radial-gradient(circle, rgba(0,209,255,0.15) 0%, rgba(0,102,255,0.08) 50%, transparent 70%)",
          }}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.4, 0.6, 0.4],
          }}
          transition={{
            duration: 5,
            repeat: Number.POSITIVE_INFINITY,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 sm:px-6 py-12 sm:py-20">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12 sm:mb-20"
          >
            <h1 className="text-2xl sm:text-3xl font-bold mb-2 sm:mb-3 text-foreground tracking-tight">
              AI Neural Processing
            </h1>
            <p className="text-foreground/60 text-xs sm:text-sm">Multi-agent intelligence analyzing your portfolio</p>
          </motion.div>

          <div className="relative h-[400px] sm:h-[500px] mb-12 sm:mb-16">
            <svg className="absolute inset-0 w-full h-full" style={{ zIndex: 0 }}>
              <defs>
                <linearGradient id="connection-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#00D1FF" stopOpacity="0.4" />
                  <stop offset="50%" stopColor="#0066FF" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#00D1FF" stopOpacity="0.4" />
                </linearGradient>
                <filter id="connection-glow">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur" />
                  <feMerge>
                    <feMergeNode in="coloredBlur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              </defs>

              {connections.map((conn, idx) => {
                const fromAgent = agents[conn.from]
                const toAgent = agents[conn.to]
                const isActive = activeAgent >= conn.from && activeAgent >= conn.to

                return (
                  <motion.line
                    key={idx}
                    x1={`${fromAgent.x}%`}
                    y1={`${fromAgent.y}%`}
                    x2={`${toAgent.x}%`}
                    y2={`${toAgent.y}%`}
                    stroke={isActive ? "#00D1FF" : "url(#connection-gradient)"}
                    strokeWidth={isActive ? "0.25" : "0.15"}
                    filter={isActive ? "url(#connection-glow)" : "none"}
                    initial={{ pathLength: 0, opacity: 0 }}
                    animate={{
                      pathLength: isActive ? 1 : 0.5,
                      opacity: isActive ? 0.9 : 0.3,
                    }}
                    transition={{ duration: 1 }}
                  />
                )
              })}

              {connections.map((conn, idx) => {
                const fromAgent = agents[conn.from]
                const toAgent = agents[conn.to]
                const isActive = activeAgent >= conn.from && activeAgent >= conn.to

                if (!isActive) return null

                return (
                  <g key={`diamond-${idx}`}>
                    <motion.path
                      d="M 0,-4 L 3,0 L 0,4 L -3,0 Z"
                      fill="#00D1FF"
                      filter="url(#connection-glow)"
                      initial={{
                        offsetDistance: "0%",
                        opacity: 0,
                      }}
                      animate={{
                        offsetDistance: ["0%", "100%"],
                        opacity: [0, 1, 1, 0],
                      }}
                      transition={{
                        duration: 2.5,
                        repeat: Number.POSITIVE_INFINITY,
                        ease: "linear",
                        delay: idx * 0.4,
                      }}
                      style={{
                        offsetPath: `path('M ${fromAgent.x * 8},${fromAgent.y * 5} L ${toAgent.x * 8},${toAgent.y * 5}')`,
                      }}
                    />
                  </g>
                )
              })}
            </svg>

            {agents.map((agent, idx) => {
              const Icon = agent.icon
              const isActive = activeAgent === idx
              const isCompleted = completedSteps.includes(idx)

              return (
                <motion.div
                  key={idx}
                  className="absolute"
                  style={{
                    left: `${agent.x}%`,
                    top: `${agent.y}%`,
                    transform: "translate(-50%, -50%)",
                  }}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: idx * 0.15, type: "spring" }}
                >
                  <motion.div
                    className={`relative backdrop-blur-sm border transition-all duration-300 ${
                      isActive
                        ? "bg-black/80 border-[#00D1FF] shadow-[0_0_30px_rgba(0,209,255,0.6)]"
                        : isCompleted
                          ? "bg-black/60 border-[#00D1FF]/40"
                          : "bg-black/40 border-[#00D1FF]/20"
                    }`}
                    style={{
                      width: "110px",
                      height: "85px",
                      borderRadius: "10px",
                      borderWidth: "1px",
                    }}
                    animate={
                      isActive
                        ? {
                            boxShadow: [
                              "0 0 20px rgba(0, 209, 255, 0.4)",
                              "0 0 40px rgba(0, 209, 255, 0.6)",
                              "0 0 20px rgba(0, 209, 255, 0.4)",
                            ],
                          }
                        : {}
                    }
                    transition={{
                      duration: 2,
                      repeat: isActive ? Number.POSITIVE_INFINITY : 0,
                    }}
                  >
                    <div className="flex flex-col items-center justify-center h-full p-2 gap-1.5">
                      <Icon
                        className={`w-5 h-5 transition-colors ${
                          isActive ? "text-[#00D1FF]" : isCompleted ? "text-[#00D1FF]/60" : "text-foreground/40"
                        }`}
                      />
                      <div className="text-center">
                        <p
                          className={`text-[11px] font-semibold tracking-tight ${
                            isActive ? "text-[#00D1FF]" : "text-foreground/80"
                          }`}
                        >
                          {agent.name}
                        </p>
                        <p className="text-[9px] text-foreground/50 mt-0.5 line-clamp-1">{agent.task}</p>
                      </div>
                    </div>

                    {isCompleted && !isActive && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-[#00D1FF] rounded-full flex items-center justify-center shadow-[0_0_10px_rgba(0,209,255,0.6)]"
                      >
                        <Check className="w-2.5 h-2.5 text-black" />
                      </motion.div>
                    )}
                  </motion.div>
                </motion.div>
              )
            })}
          </div>

          <motion.div
            key={activeAgent}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-8 sm:mb-12 px-4"
          >
            <p className="text-xs sm:text-sm text-foreground/60">
              Processing: <span className="text-[#00D1FF] font-semibold">{agents[activeAgent].name}</span>{" "}
              <span className="text-foreground/40">—</span> {agents[activeAgent].task}
            </p>
            <p className="text-xs text-foreground/40 mt-2">{statusMessage}</p>
          </motion.div>

          <div className="flex justify-center gap-2 sm:gap-3">
            {agents.map((_, idx) => {
              const isCompleted = completedSteps.includes(idx)
              const isActive = activeAgent === idx

              return (
                <motion.div
                  key={idx}
                  className={`h-1 rounded-full transition-all duration-300 ${
                    isActive
                      ? "w-10 sm:w-12 bg-[#00D1FF] shadow-[0_0_10px_rgba(0,209,255,0.6)]"
                      : isCompleted
                        ? "w-6 sm:w-8 bg-[#00D1FF]/60"
                        : "w-6 sm:w-8 bg-foreground/10"
                  }`}
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{ delay: idx * 0.1 }}
                />
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
