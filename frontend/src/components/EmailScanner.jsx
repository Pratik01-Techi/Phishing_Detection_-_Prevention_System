import { useState } from 'react'
import { analyzeEmail } from '../api'

const SAMPLE_EMAIL = `From: "PayPal Security" <security@paypa1-verify.tk>
Reply-To: support@suspicious-domain.ml
Subject: URGENT: Your account has been suspended — verify now
Authentication-Results: spf=fail; dkim=fail; dmarc=fail

Dear Customer,

Your PayPal account has been suspended due to unusual activity.
Please verify your account immediately by clicking here:
http://paypa1-secure-verify.tk/login/confirm

Act now — this link expires in 24 hours.

Attachments: invoice.exe`

export default function EmailScanner({ onResult, onLoading }) {
  const [emailText, setEmailText] = useState('')
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    const text = emailText.trim()
    if (!text) {
      setError('Please paste email headers or content')
      return
    }
    setError(null)
    onLoading?.(true)
    try {
      const result = await analyzeEmail(text)
      onResult?.(result)
    } catch (e) {
      setError(e.message)
      onResult?.(null)
    } finally {
      onLoading?.(false)
    }
  }

  return (
    <div>
      <textarea
        value={emailText}
        onChange={(e) => setEmailText(e.target.value)}
        placeholder="Paste raw email headers and body here..."
        rows={8}
        className="w-full bg-navy border border-gray-700 rounded-xl px-4 py-3 text-textPrimary placeholder-textSecondary focus:outline-none focus:border-info font-mono text-xs resize-y"
      />
      {error && <p className="text-danger text-sm mt-2">{error}</p>}
      <div className="flex gap-2 mt-3">
        <button
          type="button"
          onClick={() => setEmailText(SAMPLE_EMAIL)}
          className="text-xs text-info hover:underline"
        >
          Load sample phishing email
        </button>
      </div>
      <button
        type="button"
        onClick={handleAnalyze}
        className="w-full mt-4 bg-info hover:bg-blue-600 text-white font-semibold py-3 rounded-xl transition"
      >
        ANALYZE EMAIL →
      </button>
    </div>
  )
}
