import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import { Plus, Search, Grid, List, Car } from 'lucide-react'
import { getVehicles } from '../services/api'
import VehicleCard from '../components/VehicleCard'
import VehicleTable from '../components/VehicleTable'
import VehicleFilters from '../components/VehicleFilters'
import LoadingSpinner from '../components/LoadingSpinner'


const Vehicles: React.FC = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [filters, setFilters] = useState({
    marca: '',
    modelo: '',
    año: '',
    estatus: '',
    precio_min: '',
    precio_max: '',
    search: '',
  })
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 12,
  })

  // Fetch vehicles with filters and pagination
  const { data: vehiclesData, isLoading, error } = useQuery(
    ['vehicles', filters, pagination],
    () => getVehicles({
      ...filters,
      skip: (pagination.page - 1) * pagination.limit,
      limit: pagination.limit,
    }),
    { keepPreviousData: true }
  )

  const handleFilterChange = (newFilters: Partial<typeof filters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }))
    setPagination(prev => ({ ...prev, page: 1 })) // Reset to first page
  }

  const handleSearch = (searchTerm: string) => {
    setFilters(prev => ({ ...prev, search: searchTerm }))
    setPagination(prev => ({ ...prev, page: 1 }))
  }

  const handlePageChange = (newPage: number) => {
    setPagination(prev => ({ ...prev, page: newPage }))
  }

  if (error) {
    const errorMessage = error instanceof Error ? error.message : 'Error desconocido'
    const isNetworkError = errorMessage.includes('Network Error') || errorMessage.includes('fetch')
    const isServerError = errorMessage.includes('500') || errorMessage.includes('Internal Server Error')
    
    return (
      <div className="page-container">
        <div className="page-header">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="page-title">Vehículos</h1>
              <p className="page-subtitle">
                Gestiona tu inventario de vehículos y listados
              </p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="text-center py-12">
            <div className="mx-auto h-12 w-12 text-red-600 mb-4">
              <Car className="h-12 w-12" />
            </div>
            <h3 className="text-lg font-semibold text-red-600 mb-2">Error al cargar vehículos</h3>
            <p className="text-gray-600 mb-4">
              {isNetworkError 
                ? 'No se pudo conectar con el servidor. Verifica tu conexión a internet.'
                : isServerError
                ? 'El servidor está experimentando problemas. Intenta nuevamente en unos momentos.'
                : 'Ocurrió un error inesperado al cargar los vehículos.'
              }
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <button 
                onClick={() => window.location.reload()} 
                className="btn-danger"
              >
                Recargar Página
              </button>
              <button 
                onClick={() => {
                  // Reset filters and try again
                  setFilters({
                    marca: '',
                    modelo: '',
                    año: '',
                    estatus: '',
                    precio_min: '',
                    precio_max: '',
                    search: '',
                  })
                  setPagination({ page: 1, limit: 12 })
                }}
                className="btn-secondary"
              >
                Limpiar Filtros
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="space-y-6">
        {/* Page Header */}
        <div className="page-header">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="page-title">Vehículos</h1>
              <p className="page-subtitle">
                Gestiona tu inventario de vehículos y listados
              </p>
            </div>
          </div>
        </div>

      {/* Search and Filters */}
      <div className="card">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search Bar */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar vehículos por marca, modelo o descripción..."
                className="input-field pl-10"
                value={filters.search}
                onChange={(e) => handleSearch(e.target.value)}
              />
            </div>
          </div>

          {/* View Mode Toggle */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg transition-colors duration-200 ${
                viewMode === 'grid'
                  ? 'bg-blue-100 text-blue-600'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <Grid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg transition-colors duration-200 ${
                viewMode === 'list'
                  ? 'bg-blue-100 text-blue-600'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <List className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Advanced Filters */}
        <VehicleFilters
          filters={filters}
          onFilterChange={handleFilterChange}
        />
      </div>

      {/* Results Summary */}
      {vehiclesData && (
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>
            Mostrando {vehiclesData.vehicles.length} de {vehiclesData.total} vehículos
          </span>
          {vehiclesData.total > 0 && (
            <span>
              Página {pagination.page} de {Math.ceil(vehiclesData.total / pagination.limit)}
            </span>
          )}
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner />
        </div>
      )}

      {/* Vehicles Display */}
      {!isLoading && vehiclesData && (
        <>
          {viewMode === 'grid' ? (
            <div className="vehicle-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {vehiclesData.vehicles.map((vehicle) => (
                <VehicleCard key={vehicle.id} vehicle={vehicle} />
              ))}
            </div>
          ) : (
            <VehicleTable vehicles={vehiclesData.vehicles} />
          )}

          {/* Empty State */}
          {vehiclesData.vehicles.length === 0 && (
            <div className="empty-state">
              <div className="text-center py-12">
                <div className="mx-auto h-12 w-12 text-gray-400 mb-4">
                  <Car className="h-12 w-12" />
                </div>
                <h3 className="empty-state-title">No vehicles found</h3>
                <p className="empty-state-description">
                  {filters.search || Object.values(filters).some(f => f)
                    ? 'Try adjusting your search or filters'
                    : 'Start by adding your first vehicle to the system'
                  }
                </p>
                {!filters.search && !Object.values(filters).some(f => f) && (
                  <Link to="/vehicles/new" className="btn-primary mt-4">
                    Add First Vehicle
                  </Link>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {/* Pagination */}
      {vehiclesData && vehiclesData.total > pagination.limit && (
        <div className="flex items-center justify-center space-x-2">
          <button
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page === 1}
            className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          {Array.from({ length: Math.ceil(vehiclesData.total / pagination.limit) }, (_, i) => i + 1)
            .filter(page => 
              page === 1 || 
              page === Math.ceil(vehiclesData.total / pagination.limit) ||
              Math.abs(page - pagination.page) <= 2
            )
            .map((page, index, array) => (
              <React.Fragment key={page}>
                {index > 0 && array[index - 1] !== page - 1 && (
                  <span className="px-2 text-gray-400">...</span>
                )}
                <button
                  onClick={() => handlePageChange(page)}
                  className={`px-3 py-2 text-sm font-medium rounded-md ${
                    page === pagination.page
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-500 bg-white border border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {page}
                </button>
              </React.Fragment>
            ))}
          
          <button
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page === Math.ceil(vehiclesData.total / pagination.limit)}
            className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
      </div>
    </div>
  )
}

export default Vehicles
