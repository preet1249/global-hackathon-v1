"use client"

import { useState } from "react"
import { UploadScreen } from "@/components/upload-screen"
import { ProgressView } from "@/components/progress-view"
import { ResultsDashboard } from "@/components/results-dashboard"
import { Navbar } from "@/components/navbar"
import { createJob } from "@/lib/api"

type AppState = "upload" | "processing" | "results"

export default function AppPage() {
  const [appState, setAppState] = useState<AppState>("upload")
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [jobId, setJobId] = useState<string>("")
  const [filters, setFilters] = useState({
    thesis: "",
    sector: "",
    stage: "",
    geography: "",
    ticketSize: "",
  })

  const handleStartScreening = async (files: File[], filterData: typeof filters, sheetsUrl: string) => {
    try {
      setUploadedFiles(files)
      setFilters(filterData)

      // Create FormData for API call
      const formData = new FormData()

      // Add files
      files.forEach((file) => {
        formData.append("files", file)
      })

      // Add Google Sheet link if provided
      if (sheetsUrl) {
        formData.append("google_sheet_link", sheetsUrl)
      }

      // Add filters as JSON
      const filterPayload = {
        context_text: filterData.thesis,
        sector: filterData.sector,
        stage: filterData.stage,
        geography: filterData.geography,
        ticket_min: filterData.ticketSize ? parseFloat(filterData.ticketSize.split("-")[0].replace(/[^0-9.]/g, "")) : null,
        ticket_max: filterData.ticketSize && filterData.ticketSize.includes("-")
          ? parseFloat(filterData.ticketSize.split("-")[1].replace(/[^0-9.]/g, ""))
          : null
      }

      formData.append("filters", JSON.stringify(filterPayload))

      // Create job via API - NO MOCK DATA
      const response = await createJob(formData)

      if (response.job_id) {
        setJobId(response.job_id)
        setAppState("processing")
      }

    } catch (error) {
      console.error("Failed to start screening:", error)
      alert("Failed to start screening. Please try again.")
    }
  }

  const handleReset = () => {
    setAppState("upload")
    setUploadedFiles([])
    setJobId("")
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
      {appState === "processing" && <ProgressView jobId={jobId} onComplete={() => setAppState("results")} />}
      {appState === "results" && <ResultsDashboard jobId={jobId} onReset={handleReset} />}
    </div>
  )
}
