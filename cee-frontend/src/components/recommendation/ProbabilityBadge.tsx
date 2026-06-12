function ProbabilityBadge({ probability }: { probability: number }) {
  let colorClass = 'bg-emerald-500'
  let label = '保底'
  let textColor = 'text-emerald-700'
  let bgColor = 'bg-emerald-50'

  if (probability < 50) {
    colorClass = 'bg-amber-500'
    label = '冲刺'
    textColor = 'text-amber-700'
    bgColor = 'bg-amber-50'
  } else if (probability < 80) {
    colorClass = 'bg-sky-500'
    label = '稳妥'
    textColor = 'text-sky-700'
    bgColor = 'bg-sky-50'
  }

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full ${colorClass} rounded-full transition-all duration-500`}
          style={{ width: `${probability}%` }}
        />
      </div>
      <span className={`text-xs px-2.5 py-1 rounded-lg font-medium ${bgColor} ${textColor}`}>
        {label} · {probability}%
      </span>
    </div>
  )
}

export default ProbabilityBadge
