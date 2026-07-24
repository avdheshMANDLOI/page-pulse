import type { AuditResult } from '../services/auditApi'

interface ResultsCardProps {
  result: AuditResult
}

interface MetricProps {
  label: string
  value: string | number
}

function Metric({ label, value }: MetricProps) {
  return (
    <div className="rounded-lg bg-slate-50 p-4">
      <dt className="text-sm font-medium text-slate-500">{label}</dt>
      <dd className="mt-1 text-xl font-semibold text-slate-900">{value}</dd>
    </div>
  )
}

export function ResultsCard({ result }: ResultsCardProps) {
  return (
    <section aria-live="polite" className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-slate-500">Audit result</p>
      <h2 className="mt-1 break-words text-xl font-semibold text-slate-900">{result.url}</h2>
      <dl className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Metric label="HTTP Status" value={result.status_code} />
        <Metric label="Response Time" value={`${result.response_time_ms} ms`} />
        <Metric label="H1 Count" value={result.h1_count} />
        <Metric label="Images Missing Alt" value={result.images_missing_alt} />
        <Metric label="Word Count" value={result.word_count.toLocaleString()} />
      </dl>
      <div className="mt-6 space-y-4 border-t border-slate-100 pt-5">
        <div>
          <h3 className="text-sm font-medium text-slate-500">Page Title</h3>
          <p className="mt-1 break-words text-slate-900">{result.title || 'Not found'}</p>
        </div>
        <div>
          <h3 className="text-sm font-medium text-slate-500">Meta Description</h3>
          <p className="mt-1 break-words text-slate-900">
            {result.meta_description || 'Not found'}
          </p>
        </div>
      </div>
    </section>
  )
}
