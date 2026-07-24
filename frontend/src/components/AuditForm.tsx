import type { FormEvent } from 'react'

interface AuditFormProps {
  url: string
  isLoading: boolean
  onUrlChange: (url: string) => void
  onSubmit: () => void
}

export function AuditForm({ url, isLoading, onUrlChange, onSubmit }: AuditFormProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    onSubmit()
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 sm:flex-row">
      <label className="sr-only" htmlFor="url">
        Webpage URL
      </label>
      <input
        id="url"
        type="url"
        value={url}
        onChange={(event) => onUrlChange(event.target.value)}
        placeholder="https://example.com"
        required
        disabled={isLoading}
        className="min-w-0 flex-1 rounded-lg border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-blue-600 focus:ring-4 focus:ring-blue-100 disabled:bg-slate-100"
      />
      <button
        type="submit"
        disabled={isLoading}
        className="inline-flex min-h-12 items-center justify-center rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-200 disabled:cursor-not-allowed disabled:bg-blue-400"
      >
        {isLoading ? 'Analyzing…' : 'Analyze'}
      </button>
    </form>
  )
}
