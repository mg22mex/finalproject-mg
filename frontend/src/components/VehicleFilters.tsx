import React, { useState } from 'react'
import { Filter, X } from 'lucide-react'
import { VehicleStatus } from '../types/vehicle'

interface VehicleFiltersProps {
  filters: {
    marca: string
    modelo: string
    año: string
    estatus: string
    precio_min: string
    precio_max: string
    search: string
  }
  onFilterChange: (filters: Partial<VehicleFiltersProps['filters']>) => void
}

const VehicleFilters: React.FC<VehicleFiltersProps> = ({ filters, onFilterChange }) => {
  const [isExpanded, setIsExpanded] = useState(false)

  const statusOptions: VehicleStatus[] = ['Disponible', 'FOTOS', 'AUSENTE', 'Apartado', 'Vendido']

  const clearFilters = () => {
    onFilterChange({
      marca: '',
      modelo: '',
      año: '',
      estatus: '',
      precio_min: '',
      precio_max: '',
    })
  }

  const hasActiveFilters = Object.values(filters).some(value => value !== '')

  return (
    <div className="mt-4">
      {/* Filter Toggle */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors duration-200"
        >
          <Filter className="h-4 w-4" />
          <span className="text-sm font-medium">Advanced Filters</span>
        </button>

        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-red-600 hover:text-red-700 transition-colors duration-200"
          >
            Clear All
          </button>
        )}
      </div>

      {/* Expanded Filters */}
      {isExpanded && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Brand Filter */}
            <div className="form-group">
              <label className="form-label">Brand (Marca)</label>
              <input
                type="text"
                className="input-field"
                placeholder="e.g., Toyota, Honda"
                value={filters.marca}
                onChange={(e) => onFilterChange({ marca: e.target.value })}
              />
            </div>

            {/* Model Filter */}
            <div className="form-group">
              <label className="form-label">Model (Modelo)</label>
              <input
                type="text"
                className="input-field"
                placeholder="e.g., Camry, Civic"
                value={filters.modelo}
                onChange={(e) => onFilterChange({ modelo: e.target.value })}
              />
            </div>

            {/* Year Filter */}
            <div className="form-group">
              <label className="form-label">Year (Año)</label>
              <input
                type="number"
                className="input-field"
                placeholder="e.g., 2020"
                min="1900"
                max="2030"
                value={filters.año}
                onChange={(e) => onFilterChange({ año: e.target.value })}
              />
            </div>

            {/* Status Filter */}
            <div className="form-group">
              <label className="form-label">Status (Estatus)</label>
              <select
                className="input-field"
                value={filters.estatus}
                onChange={(e) => onFilterChange({ estatus: e.target.value })}
              >
                <option value="">All Statuses</option>
                {statusOptions.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>

            {/* Min Price Filter */}
            <div className="form-group">
              <label className="form-label">Min Price (Precio Mínimo)</label>
              <input
                type="number"
                className="input-field"
                placeholder="e.g., 10000"
                min="0"
                step="1000"
                value={filters.precio_min}
                onChange={(e) => onFilterChange({ precio_min: e.target.value })}
              />
            </div>

            {/* Max Price Filter */}
            <div className="form-group">
              <label className="form-label">Max Price (Precio Máximo)</label>
              <input
                type="number"
                className="input-field"
                placeholder="e.g., 50000"
                min="0"
                step="1000"
                value={filters.precio_max}
                onChange={(e) => onFilterChange({ precio_max: e.target.value })}
              />
            </div>
          </div>

          {/* Active Filters Display */}
          {hasActiveFilters && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex flex-wrap gap-2">
                {Object.entries(filters).map(([key, value]) => {
                  if (value && key !== 'search') {
                    return (
                      <span
                        key={key}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
                      >
                        {key}: {value}
                        <button
                          onClick={() => onFilterChange({ [key]: '' })}
                          className="ml-2 text-blue-600 hover:text-blue-800"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </span>
                    )
                  }
                  return null
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default VehicleFilters
