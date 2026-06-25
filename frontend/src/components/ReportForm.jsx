import { useState } from 'react'
import { submitReport } from '../api'

export default function ReportForm({ defaultUrl = '' }) {
  const [url, setUrl] = useState(defaultUrl)
  const [type, setType] = useState('phishing')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!url.trim()) return
    setLoading(true)
    setStatus(null)
    try {
      const res = await submitReport({ url, type, description })
      setStatus({ ok: true, id: res.report_id })
      setDescription('')
    } catch {
      setStatus({ ok: false })
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="text-textSecondary text-xs block mb-1">URL</label>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          className="w-full bg-navy border border-gray-700 rounded-lg px-3 py-2 text-textPrimary text-sm font-mono focus:outline-none focus:border-info"
        />
      </div>
      <div>
        <label className="text-textSecondary text-xs block mb-1">Report Type</label>
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="w-full bg-navy border border-gray-700 rounded-lg px-3 py-2 text-textPrimary text-sm focus:outline-none focus:border-info"
        >
          <option value="phishing">Phishing</option>
          <option value="spam">Spam</option>
          <option value="malware">Malware</option>
        </select>
      </div>
      <div>
        <label className="text-textSecondary text-xs block mb-1">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full bg-navy border border-gray-700 rounded-lg px-3 py-2 text-textPrimary text-sm focus:outline-none focus:border-info resize-none"
          placeholder="Describe what you observed..."
        />
      </div>
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-danger hover:bg-red-600 disabled:opacity-50 text-white font-semibold py-2.5 rounded-lg transition"
      >
        {loading ? 'Submitting...' : 'Submit Report'}
      </button>
      {status?.ok && (
        <p className="text-success text-sm">Report received! ID: {status.id}</p>
      )}
      {status && !status.ok && (
        <p className="text-danger text-sm">Failed to submit report. Try again.</p>
      )}
    </form>
  )
}
