import { useEffect, useState } from 'react'
import { getHistory } from '../api'

function timeAgo(iso) {
  if (!iso) return ''
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins} min${mins > 1 ? 's' : ''} ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs} hr${hrs > 1 ? 's' : ''} ago`
  const days = Math.floor(hrs / 24)
  return `${days} day${days > 1 ? 's' : ''} ago`
}

const DOT = {
  PHISHING: 'bg-danger',
  SUSPICIOUS: 'bg-warning',
  CLEAN: 'bg-success',
}

export default function ScanHistory({ onReanalyze, refreshKey = 0 }) {
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getHistory(20)
      .then(setScans)
      .catch(() => setScans([]))
      .finally(() => setLoading(false))
  }, [refreshKey])

  if (loading) {
    return (
      <div className="bg-surface rounded-xl border border-gray-800 p-4">
        <h3 className="text-textSecondary text-xs uppercase mb-3">Recent Scans</h3>
        {[1, 2, 3].map((i) => (
          <div key={i} className="skeleton h-10 rounded-lg mb-2" />
        ))}
      </div>
    )
  }

  return (
    <div className="bg-surface rounded-xl border border-gray-800 p-4">
      <h3 className="text-textSecondary text-xs uppercase tracking-wider mb-3">
        Recent Scans
      </h3>
      <div className="max-h-64 overflow-y-auto space-y-1">
        {scans.length === 0 ? (
          <p className="text-textSecondary text-sm">No scans yet</p>
        ) : (
          scans.map((scan) => (
            <button
              key={scan.id}
              type="button"
              onClick={() =>
                scan.scan_type === 'url' && onReanalyze?.(scan.input_value)
              }
              className="w-full flex items-center gap-3 py-2 px-2 rounded-lg hover:bg-gray-800/50 transition text-left"
            >
              <span className={`w-2 h-2 rounded-full flex-shrink-0 ${DOT[scan.verdict] || 'bg-gray-500'}`} />
              <span className="font-mono text-xs text-textPrimary truncate flex-1">
                {scan.input_value?.slice(0, 40)}
              </span>
              <span
                className={`text-xs font-semibold flex-shrink-0 ${
                  scan.verdict === 'PHISHING'
                    ? 'text-danger'
                    : scan.verdict === 'SUSPICIOUS'
                    ? 'text-warning'
                    : 'text-success'
                }`}
              >
                {scan.verdict}
              </span>
              <span className="text-textSecondary text-xs flex-shrink-0 hidden sm:block">
                {timeAgo(scan.created_at)}
              </span>
            </button>
          ))
        )}
      </div>
    </div>
  )
}
