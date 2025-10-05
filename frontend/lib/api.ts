// API utility for connecting to backend
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Example API call helper
export async function apiCall(endpoint: string, options?: RequestInit) {
  const url = `${API_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('API call failed:', error)
    throw error
  }
}

// Health check
export async function checkBackendHealth() {
  try {
    const data = await apiCall('/health')
    return data
  } catch (error) {
    console.error('Backend health check failed:', error)
    return null
  }
}

// Create job example
export async function createJob(formData: FormData) {
  try {
    console.log('Creating job at:', `${API_URL}/api/jobs`)

    const response = await fetch(`${API_URL}/api/jobs`, {
      method: 'POST',
      body: formData, // Don't set Content-Type for FormData
    })

    console.log('Response status:', response.status)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Backend error:', errorText)
      throw new Error(`Failed to create job: ${response.status} - ${errorText}`)
    }

    const data = await response.json()
    console.log('Job created:', data)
    return data
  } catch (error) {
    console.error('Create job error:', error)
    throw error
  }
}

// Get job status
export async function getJobStatus(jobId: string) {
  return await apiCall(`/api/jobs/${jobId}`)
}

// Get job results
export async function getJobResults(jobId: string) {
  return await apiCall(`/api/jobs/${jobId}/results`)
}
