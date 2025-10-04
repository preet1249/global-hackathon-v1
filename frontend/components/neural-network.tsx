"use client"

import { motion } from "framer-motion"

export function NeuralNetwork() {
  return (
    <div className="relative w-full h-64">
      <svg className="w-full h-full" viewBox="0 0 400 250">
        {/* Animated connections */}
        {[
          { x1: 50, y1: 125, x2: 200, y2: 80 },
          { x1: 50, y1: 125, x2: 200, y2: 125 },
          { x1: 50, y1: 125, x2: 200, y2: 170 },
          { x1: 200, y1: 80, x2: 350, y2: 125 },
          { x1: 200, y1: 125, x2: 350, y2: 125 },
          { x1: 200, y1: 170, x2: 350, y2: 125 },
        ].map((line, idx) => (
          <motion.line
            key={idx}
            x1={line.x1}
            y1={line.y1}
            x2={line.x2}
            y2={line.y2}
            stroke="url(#gradient)"
            strokeWidth="2"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 0.6 }}
            transition={{
              duration: 2,
              delay: idx * 0.2,
              repeat: Number.POSITIVE_INFINITY,
              repeatType: "reverse",
            }}
          />
        ))}

        {/* Gradient definition */}
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#00D1FF" />
            <stop offset="100%" stopColor="#0066FF" />
          </linearGradient>
        </defs>

        {/* Nodes */}
        {[
          { cx: 50, cy: 125, delay: 0 },
          { cx: 200, cy: 80, delay: 0.3 },
          { cx: 200, cy: 125, delay: 0.4 },
          { cx: 200, cy: 170, delay: 0.5 },
          { cx: 350, cy: 125, delay: 0.8 },
        ].map((node, idx) => (
          <motion.circle
            key={idx}
            cx={node.cx}
            cy={node.cy}
            r="8"
            fill="url(#gradient)"
            initial={{ scale: 0 }}
            animate={{ scale: [1, 1.2, 1] }}
            transition={{
              duration: 2,
              delay: node.delay,
              repeat: Number.POSITIVE_INFINITY,
            }}
          />
        ))}
      </svg>
    </div>
  )
}
