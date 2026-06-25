import { useEffect, useState } from 'react'

export default function RiskGauge({ score = 0, size = 160 }) {
  const [animated, setAnimated] = useState(false)
  const clamped = Math.min(100, Math.max(0, score))

  useEffect(() => {
    const t = setTimeout(() => setAnimated(true), 50)
    return () => clearTimeout(t)
  }, [score])

  const color =
    clamped <= 30 ? '#10b981' : clamped <= 60 ? '#f59e0b' : '#ef4444'

  // Semicircle: 180deg arc, needle from -90 to +90 based on score
  const rotation = -90 + (clamped / 100) * 180
  const r = size / 2 - 12
  const cx = size / 2
  const cy = size / 2 + 8

  const arcPath = (startAngle, endAngle) => {
    const toRad = (deg) => (deg * Math.PI) / 180
    const x1 = cx + r * Math.cos(toRad(startAngle))
    const y1 = cy + r * Math.sin(toRad(startAngle))
    const x2 = cx + r * Math.cos(toRad(endAngle))
    const y2 = cy + r * Math.sin(toRad(endAngle))
    const large = endAngle - startAngle > 180 ? 1 : 0
    return `M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2}`
  }

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size / 2 + 24} viewBox={`0 0 ${size} ${size / 2 + 24}`}>
        {/* Background arc */}
        <path
          d={arcPath(180, 360)}
          fill="none"
          stroke="#1f2937"
          strokeWidth="10"
          strokeLinecap="round"
        />
        {/* Colored progress arc */}
        <path
          d={arcPath(180, 180 + (clamped / 100) * 180)}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeLinecap="round"
          style={{
            transition: 'stroke-dashoffset 1s ease-out',
            opacity: animated ? 1 : 0.3,
          }}
        />
        {/* Needle */}
        <g
          style={{
            transform: `rotate(${animated ? rotation : -90}deg)`,
            transformOrigin: `${cx}px ${cy}px`,
            transition: 'transform 1s ease-out',
          }}
        >
          <line
            x1={cx}
            y1={cy}
            x2={cx}
            y2={cy - r + 8}
            stroke={color}
            strokeWidth="3"
            strokeLinecap="round"
          />
          <circle cx={cx} cy={cy} r="5" fill={color} />
        </g>
        <text
          x={cx}
          y={cy + 28}
          textAnchor="middle"
          fill="#f1f5f9"
          fontSize="22"
          fontWeight="700"
          fontFamily="JetBrains Mono, monospace"
        >
          {clamped}
        </text>
      </svg>
      <span className="text-textSecondary text-xs mt-1">Risk Score</span>
    </div>
  )
}
