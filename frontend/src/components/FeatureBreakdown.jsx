import { useState } from 'react'

const FEATURE_LABELS = {
  url_length: 'URL Length',
  domain_length: 'Domain Length',
  num_dots: 'Dot Count',
  num_hyphens: 'Hyphen Count',
  num_underscores: 'Underscore Count',
  num_slashes: 'Slash Count',
  num_at_symbol: '@ Symbol Present',
  num_double_slash: 'Double Slash Trick',
  has_ip_address: 'IP as Domain',
  is_https: 'HTTPS Enabled',
  subdomain_depth: 'Subdomain Depth',
  suspicious_keywords: 'Suspicious Keywords',
  domain_age_days: 'Domain Age (days)',
  tld_risk_score: 'High-Risk TLD',
  url_entropy: 'URL Entropy',
  digit_ratio: 'Digit Ratio',
  special_char_count: 'Special Characters',
  lookalike_score: 'Brand Lookalike Score',
}

function isRisky(name, value) {
  const risky = {
    has_ip_address: v => v === 1,
    num_at_symbol: v => v === 1,
    num_double_slash: v => v === 1,
    tld_risk_score: v => v === 1,
    is_https: v => v === 0,
    suspicious_keywords: v => v >= 1,
    domain_age_days: v => v >= 0 && v < 30,
    lookalike_score: v => v >= 0.75,
    subdomain_depth: v => v >= 3,
    url_length: v => v > 100,
    special_char_count: v => v >= 3,
  }
  return risky[name] ? risky[name](value) : false
}

export default function FeatureBreakdown({ features = {}, importances = {} }) {
  const [expanded, setExpanded] = useState(false)

  if (!features || Object.keys(features).length === 0) return null

  const entries = Object.entries(features).map(([name, value]) => ({
    name,
    label: FEATURE_LABELS[name] || name,
    value,
    risky: isRisky(name, value),
    importance: importances[name] || 0,
  }))

  const topSuspicious = [...entries]
    .filter(e => e.risky || e.importance > 0.05)
    .sort((a, b) => b.importance - a.importance)
    .slice(0, 5)
    .map(e => e.name)

  const display = expanded ? entries : entries.slice(0, 8)

  return (
    <div className="bg-surface rounded-xl border border-gray-800 p-4 mt-4">
      <h3 className="text-textPrimary font-semibold mb-3 text-sm uppercase tracking-wider">
        Feature Analysis
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-textSecondary text-left border-b border-gray-800">
              <th className="pb-2 pr-4">Feature</th>
              <th className="pb-2 pr-4">Value</th>
              <th className="pb-2">Risk</th>
            </tr>
          </thead>
          <tbody>
            {display.map(({ name, label, value, risky }) => (
              <tr
                key={name}
                className={`border-b border-gray-800/50 ${
                  topSuspicious.includes(name) ? 'text-danger' : 'text-textPrimary'
                }`}
              >
                <td className="py-2 pr-4 font-mono text-xs">{label}</td>
                <td className="py-2 pr-4 font-mono">{String(value)}</td>
                <td className="py-2">
                  <span
                    className={`inline-block w-2.5 h-2.5 rounded-full ${
                      risky ? 'bg-danger' : 'bg-success'
                    }`}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="mt-3 text-info text-xs hover:underline"
      >
        {expanded ? 'Hide technical details' : 'Show technical details'}
      </button>
    </div>
  )
}
