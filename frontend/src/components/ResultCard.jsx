import RiskGauge from './RiskGauge'

const VERDICT_STYLES = {
  PHISHING: {
    bg: 'bg-danger/10',
    border: 'border-danger animate-pulseBorder',
    text: 'text-danger',
    icon: '⚠️',
  },
  SUSPICIOUS: {
    bg: 'bg-warning/10',
    border: 'border-warning',
    text: 'text-warning',
    icon: '🟡',
  },
  CLEAN: {
    bg: 'bg-success/10',
    border: 'border-success',
    text: 'text-success',
    icon: '✅',
  },
}

const RULE_LABELS = {
  ip_address_domain: 'IP address used as domain',
  suspicious_keyword: 'Contains suspicious keyword',
  suspicious_keywords: 'Multiple suspicious keywords',
  high_risk_tld: 'High-risk TLD detected',
  new_domain: 'Domain registered recently',
  brand_lookalike: 'Mimics known brand name',
  at_symbol_redirect: '@ symbol redirect trick',
  double_slash_trick: 'Double-slash obfuscation',
  no_https: 'No HTTPS encryption',
  deep_subdomain: 'Unusually deep subdomain chain',
  excessive_url_length: 'Excessively long URL',
  spf_fail: 'SPF authentication failed',
  dkim_missing: 'DKIM signature missing',
  dmarc_fail: 'DMARC policy failed',
  reply_to_mismatch: 'Reply-To domain mismatch',
  display_name_spoofing: 'Display name spoofing detected',
  urgency_language: 'Urgent language detected',
  high_urgency_language: 'High urgency language',
  html_obfuscation: 'HTML obfuscation detected',
  risky_attachment: 'Risky attachment detected',
}

export default function ResultCard({ result, type = 'url' }) {
  if (!result) return null

  const verdict = result.verdict || 'CLEAN'
  const style = VERDICT_STYLES[verdict] || VERDICT_STYLES.CLEAN
  const rules = result.triggered_rules || []

  return (
    <div className={`rounded-xl border-2 p-6 ${style.bg} ${style.border} transition-all`}>
      <div className="flex flex-col md:flex-row gap-6 items-start md:items-center justify-between">
        <div>
          <p className={`text-2xl font-bold ${style.text} flex items-center gap-2`}>
            <span>{style.icon}</span>
            {verdict === 'PHISHING' && 'PHISHING DETECTED'}
            {verdict === 'SUSPICIOUS' && 'SUSPICIOUS — USE CAUTION'}
            {verdict === 'CLEAN' && 'CLEAN — LOOKS SAFE'}
          </p>
          {result.confidence != null && (
            <p className="text-textSecondary mt-1 text-sm">
              Confidence: <span className="text-textPrimary font-mono">{result.confidence}%</span>
            </p>
          )}
          {type === 'url' && result.vt_detections && (
            <p className="text-textSecondary mt-1 text-sm">
              VT Engines: <span className="text-textPrimary font-mono">{result.vt_detections}</span>
            </p>
          )}
          {result.domain_age && (
            <p className="text-textSecondary mt-1 text-sm">
              Domain Age: <span className="text-textPrimary">{result.domain_age}</span>
            </p>
          )}
          {type === 'email' && (
            <div className="flex gap-3 mt-2 text-xs font-mono">
              <span className={result.spf === 'PASS' ? 'text-success' : 'text-danger'}>
                SPF: {result.spf}
              </span>
              <span className={result.dkim === 'PASS' ? 'text-success' : 'text-danger'}>
                DKIM: {result.dkim}
              </span>
              <span className={result.dmarc === 'PASS' ? 'text-success' : 'text-danger'}>
                DMARC: {result.dmarc}
              </span>
            </div>
          )}
        </div>
        <RiskGauge score={result.risk_score ?? 0} />
      </div>

      {rules.length > 0 && (
        <div className="mt-5 border-t border-gray-700 pt-4">
          <h4 className="text-textSecondary text-xs uppercase tracking-wider mb-2">
            Why it was flagged
          </h4>
          <ul className="space-y-1.5">
            {rules.map((rule) => (
              <li key={rule} className="flex items-center gap-2 text-sm text-textPrimary">
                <span className="text-danger">✗</span>
                {RULE_LABELS[rule] || rule.replace(/_/g, ' ')}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
