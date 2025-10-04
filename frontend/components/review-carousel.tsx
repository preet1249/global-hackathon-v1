"use client"

import { motion } from "framer-motion"
import { Star } from "lucide-react"

const reviews = [
  {
    name: "Sarah Chen",
    role: "Partner at Sequoia Capital",
    avatar: "/professional-asian-woman.png",
    rating: 5,
    text: "InvestAI cut our deal screening time by 70%. The AI agents catch patterns we'd miss manually.",
  },
  {
    name: "Michael Rodriguez",
    role: "Managing Director, a16z",
    avatar: "/professional-hispanic-man.png",
    rating: 5,
    text: "Finally, a tool that understands deep tech. The technical validation is incredibly thorough.",
  },
  {
    name: "Emily Watson",
    role: "GP at Benchmark",
    avatar: "/professional-woman-caucasian.jpg",
    rating: 5,
    text: "The risk heatmap alone is worth it. We've avoided 3 bad deals in the last quarter.",
  },
  {
    name: "David Kim",
    role: "Investment Lead, Tiger Global",
    avatar: "/professional-korean-man.png",
    rating: 5,
    text: "Best investment tool I've used in 15 years. The multi-agent approach is genius.",
  },
  {
    name: "Lisa Thompson",
    role: "Principal at Kleiner Perkins",
    avatar: "/professional-blonde-woman.png",
    rating: 5,
    text: "Our portfolio performance improved 40% after adopting InvestAI. Data-driven decisions work.",
  },
  {
    name: "James Park",
    role: "Partner at Lightspeed",
    avatar: "/professional-man-asian-glasses.jpg",
    rating: 5,
    text: "The AI catches red flags in pitch decks that even experienced partners miss. Incredible.",
  },
]

export function ReviewCarousel() {
  const duplicatedReviews = [...reviews, ...reviews]

  return (
    <div className="relative overflow-hidden py-8 sm:py-12">
      <div className="absolute inset-0 bg-gradient-to-r from-background via-transparent to-background z-10 pointer-events-none" />

      <motion.div
        className="flex gap-4 sm:gap-6"
        animate={{
          x: [0, -50 * reviews.length * 16],
        }}
        transition={{
          x: {
            duration: 25,
            repeat: Number.POSITIVE_INFINITY,
            ease: "linear",
          },
        }}
      >
        {duplicatedReviews.map((review, idx) => (
          <div
            key={idx}
            className="glass rounded-xl sm:rounded-2xl p-4 sm:p-6 min-w-[280px] sm:min-w-[350px] hover-glow transition-all flex-shrink-0"
          >
            <div className="flex items-start gap-3 sm:gap-4 mb-3 sm:mb-4">
              <img
                src={review.avatar || "/placeholder.svg"}
                alt={review.name}
                className="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover border-2 border-[#00D1FF]/20"
              />
              <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-foreground text-sm sm:text-base truncate">{review.name}</h4>
                <p className="text-xs sm:text-sm text-foreground/60 truncate">{review.role}</p>
              </div>
            </div>
            <div className="flex gap-0.5 sm:gap-1 mb-2 sm:mb-3">
              {Array.from({ length: review.rating }).map((_, i) => (
                <Star key={i} className="w-3.5 h-3.5 sm:w-4 sm:h-4 fill-[#00D1FF] text-[#00D1FF]" />
              ))}
            </div>
            <p className="text-foreground/80 text-xs sm:text-sm leading-relaxed">{review.text}</p>
          </div>
        ))}
      </motion.div>
    </div>
  )
}
