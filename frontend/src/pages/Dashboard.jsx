import { useCallback, useEffect, useState } from 'react'
import { getStats, getHealth } from '../api'
import URLScanner from '../components/URLScanner'
import EmailScanner from '../components/EmailScanner'
import ResultCard from '../components/ResultCard'
import FeatureBreakdown from '../components/FeatureBreakdown'
import ScanHistory from '../components/ScanHistory'

export default function Dashboard() {
  const [tab, setTab] = useState('url')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [health, setHealth] = useState(null)
  const [historyKey, setHistoryKey] = useState(0)
  const [reanalyzeUrl, setReanalyzeUrl] = useState('')

  useEffect(() => {
    getStats().then(setStats).catch(() => {})
    getHealth().then(setHealth).catch(() => {})
  }, [historyKey])

  const handleResult = useCallback((r) => {
    setResult(r)
    if (r) setHistoryKey((k) => k + 1)
  }, [])

  const handleReanalyze = (url) => {
    setTab('url')
    setResult(null)
    setReanalyzeUrl(url)
    window.dispatchEvent(new CustomEvent('phishguard-reanalyze', { detail: url }))
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-textPrimary flex items-center gap-2">
            🛡️ PhishGuard
          </h1>
          <p className="text-textSecondary text-sm">AI-Powered Phishing Detection</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
          <span className="text-success text-xs font-semibold uppercase tracking-wider">
            Live Protection: ON
          </span>
          {health && (
            <span className="text-textSecondary text-xs ml-2">
              Model: {health.model_loaded ? '✓' : '✗'} | VT: {health.vt_api}
            </span>
          )}
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        {[
          { label: 'Total Scans', value: stats?.total_scans ?? '—', color: 'text-info' },
          { label: 'Detected', value: stats?.phishing_detected ?? '—', color: 'text-danger' },
          { label: 'Detection Rate', value: stats?.detection_rate ?? '—', color: 'text-success' },
        ].map(({ label, value, color }) => (
          <div
            key={label}
            className="bg-surface rounded-xl border border-gray-800 p-5 text-center"
          >
            <p className="text-textSecondary text-xs uppercase tracking-wider">{label}</p>
            <p className={`text-3xl font-bold font-mono mt-1 ${color}`}>{value}</p>
          </div>
        ))}
      </div>

      {/* Scanner tabs */}
      <div className="bg-surface rounded-xl border border-gray-800 p-5 mb-6">
        <div className="flex gap-2 mb-5 border-b border-gray-800 pb-3">
          {['url', 'email'].map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => { setTab(t); setResult(null) }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                tab === t
                  ? 'bg-info/20 text-info border border-info/30'
                  : 'text-textSecondary hover:text-textPrimary'
              }`}
            >
              {t === 'url' ? '🔗 URL Scanner' : '📧 Email Scanner'}
            </button>
          ))}
        </div>

        {tab === 'url' ? (
          <URLScanner onResult={handleResult} onLoading={setLoading} reanalyzeUrl={reanalyzeUrl} />
        ) : (
          <EmailScanner onResult={handleResult} onLoading={setLoading} />
        )}
      </div>

      {/* Loading skeleton */}
      {loading && (
        <div className="bg-surface rounded-xl border border-gray-800 p-6 mb-6">
          <div className="skeleton h-8 w-48 rounded mb-4" />
          <div className="skeleton h-32 rounded" />
        </div>
      )}

      {/* Results */}
      {!loading && result && (
        <div className="mb-6">
          <p className="text-textSecondary text-xs uppercase tracking-wider mb-3">Result</p>
          <ResultCard result={result} type={tab} />
          {tab === 'url' && result.features && (
            <FeatureBreakdown
              features={result.features}
              importances={result.feature_importances}
            />
          )}
        </div>
      )}

      {/* History */}
      <ScanHistory onReanalyze={handleReanalyze} refreshKey={historyKey} />
    </div>
  )
}
