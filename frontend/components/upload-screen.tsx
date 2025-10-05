"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { motion } from "framer-motion"
import { Upload, FileText, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { NeuralNetwork } from "@/components/neural-network"

interface UploadScreenProps {
  onStartScreening: (files: File[], filters: any, sheetsUrl: string) => void
}

export function UploadScreen({ onStartScreening }: UploadScreenProps) {
  const [files, setFiles] = useState<File[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const [thesis, setThesis] = useState("")
  const [sector, setSector] = useState("")
  const [stage, setStage] = useState("")
  const [geography, setGeography] = useState("")
  const [ticketSize, setTicketSize] = useState("")

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      (file) =>
        file.name.endsWith('.xlsx') ||
        file.name.endsWith('.xls') ||
        file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
        file.type === "application/vnd.ms-excel"
    )
    setFiles((prev) => {
      const combined = [...prev, ...droppedFiles]
      return combined.slice(0, 10) // Max 10 Excel files
    })
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files).filter(
        (file) =>
          file.name.endsWith('.xlsx') ||
          file.name.endsWith('.xls') ||
          file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
          file.type === "application/vnd.ms-excel"
      )
      setFiles((prev) => {
        const combined = [...prev, ...selectedFiles]
        return combined.slice(0, 10) // Max 10 Excel files
      })
    }
  }

  const handleStartScreening = () => {
    if (files.length > 0) {
      onStartScreening(files, { thesis, sector, stage, geography, ticketSize }, "")
    }
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      <div className="relative container mx-auto px-6 py-12">
        {/* Header */}
        

        <div className="grid lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
          {/* Left: Neural Network Animation */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="flex flex-col justify-center"
          >
            <h1 className="text-5xl font-bold mb-6 leading-tight">
              Let's find your next{" "}
              <span className="bg-gradient-blue bg-clip-text text-transparent glow-text">5 winning investments</span>
            </h1>
            <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
              Upload your Excel file with startup data and let our multi-agent AI system analyze, validate, and deliver investment-grade reports in minutes.
            </p>
            <NeuralNetwork />
          </motion.div>

          {/* Right: Upload Panel */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="glass rounded-3xl p-8"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl bg-gradient-blue/10 border border-[#00D1FF]/20">
                <Sparkles className="w-6 h-6 text-[#00D1FF]" />
              </div>
              <div>
                <h2 className="text-2xl font-semibold">Upload & Configure</h2>
                <p className="text-sm text-muted-foreground">Excel files only (.xls, .xlsx)</p>
              </div>
            </div>

            {/* File Upload */}
            <div className="mb-6">
              <Label className="text-sm font-medium mb-3 block flex items-center gap-2">
                📊 Upload Excel File(s)
                <span className="text-xs font-normal text-muted-foreground">(Max 10 files)</span>
              </Label>
              <div
                onDrop={handleDrop}
                onDragOver={(e) => {
                  e.preventDefault()
                  setIsDragging(true)
                }}
                onDragLeave={() => setIsDragging(false)}
                className={`border-2 border-dashed rounded-xl p-10 text-center transition-all cursor-pointer ${
                  isDragging
                    ? "border-[#00D1FF] bg-[#00D1FF]/5 scale-[1.02]"
                    : "border-border hover:border-[#00D1FF]/50 hover:bg-[#00D1FF]/5"
                }`}
              >
                <input
                  type="file"
                  multiple
                  accept=".xlsx,.xls,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
                  onChange={handleFileInput}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer block">
                  <div className="mb-4 inline-block p-4 rounded-full bg-gradient-blue/10 border border-[#00D1FF]/20">
                    <Upload className="w-8 h-8 text-[#00D1FF]" />
                  </div>
                  <p className="text-base font-medium mb-2">
                    {files.length === 0 ? "Drop your Excel files here" : `${files.length} file(s) selected`}
                  </p>
                  <p className="text-sm text-muted-foreground mb-1">
                    or click to browse from your computer
                  </p>
                  <p className="text-xs text-muted-foreground">
                    ✨ Supports: <span className="text-[#00D1FF] font-medium">.xlsx</span> and <span className="text-[#00D1FF] font-medium">.xls</span> files only
                  </p>
                  {files.length > 0 && (
                    <div className="mt-6 space-y-2 max-h-40 overflow-y-auto">
                      {files.map((file, idx) => (
                        <div key={idx} className="flex items-center gap-3 text-sm bg-[#00D1FF]/5 border border-[#00D1FF]/20 rounded-lg px-4 py-2.5 justify-center">
                          <FileText className="w-4 h-4 text-[#00D1FF]" />
                          <span className="font-medium">{file.name}</span>
                          <span className="text-xs text-muted-foreground">({(file.size / 1024).toFixed(1)} KB)</span>
                        </div>
                      ))}
                      {files.length >= 10 && (
                        <p className="text-xs text-amber-500 mt-3 font-medium">✓ Maximum 10 files reached</p>
                      )}
                    </div>
                  )}
                </label>
              </div>
              <div className="mt-3 p-3 rounded-lg bg-blue-500/5 border border-blue-500/20">
                <p className="text-xs text-muted-foreground">
                  <span className="font-medium text-foreground">💡 Required columns:</span> name, sector, stage, geography, ticket_size, summary
                  <br />
                  <span className="font-medium text-foreground">📝 Optional columns:</span> team, traction, product, website
                </p>
              </div>
            </div>

            {/* Investment Thesis */}
            <div className="mb-6">
              <Label htmlFor="thesis" className="text-sm font-medium mb-2 block">
                Investment Thesis
              </Label>
              <Textarea
                id="thesis"
                placeholder="Describe your investment focus and criteria..."
                value={thesis}
                onChange={(e) => setThesis(e.target.value)}
                rows={3}
              />
            </div>

            {/* Filters Grid */}
            <div className="grid grid-cols-2 gap-4 mb-8">
              <div>
                <Label htmlFor="sector" className="text-sm font-medium mb-2 block">
                  Sector
                </Label>
                <Input
                  id="sector"
                  placeholder="e.g., AI, FinTech"
                  value={sector}
                  onChange={(e) => setSector(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="stage" className="text-sm font-medium mb-2 block">
                  Stage
                </Label>
                <Input
                  id="stage"
                  placeholder="e.g., Seed, Series A"
                  value={stage}
                  onChange={(e) => setStage(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="geography" className="text-sm font-medium mb-2 block">
                  Geography
                </Label>
                <Input
                  id="geography"
                  placeholder="e.g., US, Europe"
                  value={geography}
                  onChange={(e) => setGeography(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="ticket-size" className="text-sm font-medium mb-2 block">
                  Ticket Size
                </Label>
                <Input
                  id="ticket-size"
                  placeholder="e.g., $1M-$5M"
                  value={ticketSize}
                  onChange={(e) => setTicketSize(e.target.value)}
                />
              </div>
            </div>

            {/* Start Button */}
            <Button
              onClick={handleStartScreening}
              disabled={files.length === 0}
              className="w-full bg-gradient-blue hover:opacity-90 text-white py-6 text-lg font-semibold group transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              <Sparkles className="w-5 h-5 mr-2 group-hover:rotate-12 transition-transform" />
              Start AI Analysis
              <span className="ml-2 group-hover:translate-x-1 transition-transform inline-block">→</span>
            </Button>
            {files.length === 0 && (
              <p className="text-xs text-center text-muted-foreground mt-3">
                Upload at least one Excel file to start
              </p>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  )
}
