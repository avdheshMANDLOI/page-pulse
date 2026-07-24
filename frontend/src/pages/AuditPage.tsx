import { useState } from 'react'

import { AuditForm } from '../components/AuditForm'
import { ResultsCard } from '../components/ResultsCard'
import { auditUrl, type AuditResult } from '../services/auditApi'

export function AuditPage() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState<AuditResult | null>(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  async function handleAudit() {
    setError('')
    setResult(null)
    setIsLoading(true)

    try {
      setResult(await auditUrl(url))
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : 'Unable to analyse this webpage. Please try again.',
      )
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col">
      <main className="mx-auto flex w-full max-w-4xl flex-1 flex-col px-4 py-12 sm:px-6 sm:py-20">
        <section className="mx-auto w-full max-w-3xl">
          <div className="mb-8 text-center">
            <p className="mb-3 text-sm font-semibold uppercase tracking-widest text-blue-600">Webpage auditor</p>
            <h1 className="text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl">Page Pulse</h1>
            <p className="mx-auto mt-4 max-w-xl text-base leading-7 text-slate-600">
              Get a quick, clear snapshot of any webpage's key content and performance signals.
            </p>
          </div>

          <AuditForm
            url={url}
            isLoading={isLoading}
            onUrlChange={setUrl}
            onSubmit={handleAudit}
          />

          {isLoading && (
            <p role="status" className="mt-5 text-center text-sm text-slate-600">
              Fetching and analysing the webpage…
            </p>
          )}

          {error && (
            <p role="alert" className="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </p>
          )}

          {result && <div className="mt-8"><ResultsCard result={result} /></div>}
        </section>
      </main>
      <footer className="px-4 py-6 text-center text-sm text-slate-500">
        Built for{' '}
        <a
          href="https://digitalheroesco.com"
          target="_blank"
          rel="noreferrer"
          className="font-medium text-slate-700 underline underline-offset-2 hover:text-blue-700"
        >
          Digital Heroes Training Task
        </a>
      </footer>
    </div>
  )
}
