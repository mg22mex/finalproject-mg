import React from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface StatsCardProps {
  title: string
  value: string | number
  icon: React.ComponentType<{ className?: string }>
  color: 'blue' | 'green' | 'purple' | 'orange' | 'red'
  change?: number
  className?: string
}

const StatsCard: React.FC<StatsCardProps> = ({ 
  title, 
  value, 
  icon: Icon, 
  color, 
  change, 
  className = '' 
}) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600',
    red: 'bg-red-50 text-red-600',
  }

  const borderClasses = {
    blue: 'border-blue-200',
    green: 'border-green-200',
    purple: 'border-purple-200',
    orange: 'border-orange-200',
    red: 'border-red-200',
  }

  return (
    <div className={`card ${borderClasses[color]} ${className}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          
          {change !== undefined && (
            <div className="flex items-center mt-2">
              {change > 0 ? (
                <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
              ) : change < 0 ? (
                <TrendingDown className="h-4 w-4 text-red-500 mr-1" />
              ) : null}
              
              <span className={`text-sm font-medium ${
                change > 0 ? 'text-green-600' : 
                change < 0 ? 'text-red-600' : 
                'text-gray-600'
              }`}>
                {change > 0 ? '+' : ''}{change}%
              </span>
            </div>
          )}
        </div>
        
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  )
}

export default StatsCard
