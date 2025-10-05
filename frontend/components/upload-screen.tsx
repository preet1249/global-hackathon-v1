"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { motion } from "framer-motion"
import { Upload, FileText, LinkIcon, Sparkles } from "lucide-react"
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
  const [sheetsUrl, setSheetsUrl] = useState("")
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
        file.type === "application/pdf" ||
        file.type === "text/csv" ||
        file.name.endsWith('.csv') ||
        file.name.endsWith('.xlsx') ||
        file.name.endsWith('.xls')
    )
    setFiles((prev) => {
      const combined = [...prev, ...droppedFiles]
      return combined.slice(0, 50) // Max 50 files
    })
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files).filter(
        (file) =>
          file.type === "application/pdf" ||
          file.type === "text/csv" ||
          file.name.endsWith('.csv') ||
          file.name.endsWith('.xlsx') ||
          file.name.endsWith('.xls')
      )
      setFiles((prev) => {
        const combined = [...prev, ...selectedFiles]
        return combined.slice(0, 50) // Max 50 files
      })
    }
  }

  const handleStartScreening = () => {
    if (files.length > 0 || sheetsUrl) {
      onStartScreening(files, { thesis, sector, stage, geography, ticketSize }, sheetsUrl)
    }
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated background - FIXED z-index and opacity */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none -z-10">
        <motion.div
          className="absolute top-20 left-10 w-96 h-96 rounded-full blur-3xl opacity-10"
          style={{
            background: "radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%)",
          }}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.05, 0.1, 0.05],
          }}
          transition={{
            duration: 8,
            repeat: Number.POSITIVE_INFINITY,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12">
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
              Upload pitch decks and let our multi-agent AI system analyze, validate, and deliver investment-grade
              reports.
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
            <h2 className="text-2xl font-semibold mb-6">Upload & Configure</h2>

            {/* File Upload */}
            <div className="mb-6">
              <Label className="text-sm font-medium mb-2 block">
                Upload Files (PDF, CSV, Google Sheets) - Max 50 PDFs
              </Label>
              <div
                onDrop={handleDrop}
                onDragOver={(e) => {
                  e.preventDefault()
                  setIsDragging(true)
                }}
                onDragLeave={() => setIsDragging(false)}
                className={`border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer ${
                  isDragging ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"
                }`}
              >
                <input
                  type="file"
                  multiple
                  accept=".pdf,.csv,.xlsx,.xls"
                  onChange={handleFileInput}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-sm text-muted-foreground mb-2">
                    Drag & drop files or click to browse
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Supports: PDF, CSV, Excel (.xlsx, .xls) • Up to 50 files
                  </p>
                  {files.length > 0 && (
                    <div className="mt-4 space-y-2 max-h-32 overflow-y-auto">
                      {files.map((file, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-sm text-primary justify-center">
                          <FileText className="w-4 h-4" />
                          {file.name}
                        </div>
                      ))}
                      {files.length >= 50 && (
                        <p className="text-xs text-amber-500 mt-2">Maximum 50 files reached</p>
                      )}
                    </div>
                  )}
                </label>
              </div>
            </div>

            {/* Google Sheets URL */}
            <div className="mb-6">
              <Label htmlFor="sheets-url" className="text-sm font-medium mb-2 block">
                Or Paste Public Google Sheets Link
              </Label>
              <div className="relative">
                <LinkIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="sheets-url"
                  placeholder="https://docs.google.com/spreadsheets/d/..."
                  value={sheetsUrl}
                  onChange={(e) => setSheetsUrl(e.target.value)}
                  className="pl-10"
                />
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Sheet must be public with columns: name, sector, stage, geography, ticket_size, summary, pdf_link
              </p>
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
              disabled={files.length === 0 && !sheetsUrl}
              className="w-full bg-gradient-blue hover:opacity-90 text-white py-6 text-lg group"
            >
              🚀 Start Screening
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
