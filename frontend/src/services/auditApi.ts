import axios from 'axios'

export interface AuditResult {
  url: string
  status_code: number
  response_time_ms: number
  title: string | null
  meta_description: string | null
  h1_count: number
  images_missing_alt: number
  word_count: number
}

interface ApiErrorResponse {
  detail?: string
}

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
})

export async function auditUrl(url: string): Promise<AuditResult> {
  try {
    const response = await apiClient.post<AuditResult>('/api/audit', { url })
    return response.data
  } catch (error) {
    if (axios.isAxiosError<ApiErrorResponse>(error)) {
      if (typeof error.response?.data.detail === 'string') {
        throw new Error(error.response.data.detail)
      }
      if (error.request) {
        throw new Error('Unable to reach the Page Pulse API.')
      }
    }
    throw new Error('Unable to analyse this webpage. Please try again.')
  }
}
