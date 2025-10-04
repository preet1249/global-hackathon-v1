"use client"

import { useState } from "react"
import { UploadScreen } from "@/components/upload-screen"
import { ProgressView } from "@/components/progress-view"
import { ResultsDashboard } from "@/components/results-dashboard"
import { Navbar } from "@/components/navbar"

type AppState = "upload" | "processing" | "results"

export default function AppPage() {
  const [appState, setAppState] = useState<AppState>("upload")
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [filters, setFilters] = useState({
    thesis: "",
    sector: "",
    stage: "",
    geography: "",
    ticketSize: "",
  })

  const handleStartScreening = (files: File[], filterData: typeof filters) => {
    setUploadedFiles(files)
    setFilters(filterData)
    setAppState("processing")

    setTimeout(() => {
      setAppState("results")
    }, 30000)
  }

  const handleReset = () => {
    setAppState("upload")
    setUploadedFiles([])
    setFilters({
      thesis: "",
      sector: "",
      stage: "",
      geography: "",
      ticketSize: "",
    })
  }

  return (
    <div className="min-h-screen bg-gradient-dark">
      <Navbar />
      {appState === "upload" && <UploadScreen onStartScreening={handleStartScreening} />}
      {appState === "processing" && <ProgressView />}
      {appState === "results" && <ResultsDashboard onReset={handleReset} />}
    </div>
  )
}
