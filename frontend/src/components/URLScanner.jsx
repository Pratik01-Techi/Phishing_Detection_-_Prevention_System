import { useCallback, useEffect, useState } from 'react'
import { analyzeUrl } from '../api'

const QUICK_TESTS = {
  phishing: [
    'http://paypa1-secure-verify.tk/login/confirm',
    'http://192.168.1.1/amazon-account-suspended',
    'https://google-security-alert.000webhostapp.com',
  ],
  suspicious: [
    'http://free-iphone-winner.xyz/claim',
    'https://bit.ly/3xR9k2m',
  ],
  clean: [
    'https://github.com',
    'https://google.com',
    'https://stackoverflow.com',
  ],
}

export default function URLScanner({ onResult, onLoading, reanalyzeUrl }) {
  const [url, setUrl] = useState('')
  const [error, setError] = useState(null)

  const handleAnalyze = useCallback(async (testUrl) => {
    const target = (testUrl || url).trim()
    if (!target) {
      setError('Please enter a URL')
      return
    }
    setError(null)
    onLoading?.(true)
    try {
      const result = await analyzeUrl(target)
      onResult?.(result)
    } catch (e) {
      setError(e.message)
      onResult?.(null)
    } finally {
      onLoading?.(false)
    }
  }, [url, onResult, onLoading])

  useEffect(() => {
    if (reanalyzeUrl) {
      setUrl(reanalyzeUrl)
      handleAnalyze(reanalyzeUrl)
    }
  }, [reanalyzeUrl, handleAnalyze])

  useEffect(() => {
    const handler = (e) => {
      setUrl(e.detail)
      handleAnalyze(e.detail)
    }
    window.addEventListener('phishguard-reanalyze', handler)
    return () => window.removeEventListener('phishguard-reanalyze', handler)
  }, [handleAnalyze])

  return (
    <div>
      <div className="relative">
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-textSecondary">🔍</span>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
          placeholder="https://suspicious-site.com"
          className="w-full bg-navy border border-gray-700 rounded-xl pl-11 pr-4 py-4 text-textPrimary placeholder-textSecondary focus:outline-none focus:border-info font-mono text-sm"
        />
      </div>
      {error && <p className="text-danger text-sm mt-2">{error}</p>}
      <button
        type="button"
        onClick={() => handleAnalyze()}
        className="w-full mt-4 bg-danger hover:bg-red-600 text-white font-semibold py-3 rounded-xl transition flex items-center justify-center gap-2"
      >
        ANALYZE NOW →
      </button>

      <div className="mt-4">
        <p className="text-textSecondary text-xs mb-2">Quick Test</p>
        <div className="flex flex-wrap gap-2">
          {Object.entries(QUICK_TESTS).map(([category, urls]) =>
            urls.map((u) => (
              <button
                key={u}
                type="button"
                onClick={() => {
                  setUrl(u)
                  handleAnalyze(u)
                }}
                className={`text-xs px-3 py-1 rounded-full border font-mono transition hover:opacity-80 ${
                  category === 'phishing'
                    ? 'border-danger/50 text-danger'
                    : category === 'suspicious'
                    ? 'border-warning/50 text-warning'
                    : 'border-success/50 text-success'
                }`}
              >
                {u.replace(/^https?:\/\//, '').slice(0, 28)}…
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
