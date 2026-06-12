import type { Recommendation } from '@/types/recommendation'
import ProbabilityBadge from './ProbabilityBadge'
import { MapPin, TrendingUp, ChevronRight } from 'lucide-react'

function RecommendationCard({ rec }: { rec: Recommendation }) {
  return (
    <div className="bg-white rounded-2xl border p-6 hover:shadow-lg hover:shadow-primary/5 hover:border-primary/20 transition-all duration-300 group">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex items-center gap-3 mb-2">
            <h3 className="font-bold text-lg text-foreground">{rec.college.name}</h3>
            <div className="flex gap-1.5">
              {rec.college.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-[10px] px-2 py-0.5 bg-primary/5 text-primary rounded-md font-medium border border-primary/10"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Location & Major */}
          <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
            <span className="flex items-center gap-1">
              <MapPin className="h-3.5 w-3.5" />
              {rec.college.location}
            </span>
            <span className="flex items-center gap-1">
              <TrendingUp className="h-3.5 w-3.5" />
              {rec.major}
            </span>
          </div>

          {/* Probability */}
          <ProbabilityBadge probability={rec.probability} />

          {/* Previous Scores */}
          <div className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
            <span>近年录取分:</span>
            <div className="flex gap-1.5">
              {rec.previousScores.map((score, i) => (
                <span key={i} className="px-2 py-0.5 bg-muted rounded-md font-mono">
                  {score}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Action */}
        <button className="flex-shrink-0 p-2 text-muted-foreground hover:text-primary hover:bg-primary/5 rounded-lg transition-colors opacity-0 group-hover:opacity-100">
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>
    </div>
  )
}

export default RecommendationCard
