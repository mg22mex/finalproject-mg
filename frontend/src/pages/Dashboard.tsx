import React from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { Car, DollarSign, Camera, Plus, Settings } from 'lucide-react'
import { getVehicles, getDashboardStats } from '../services/api'
import VehicleCard from '../components/VehicleCard'
import StatsCard from '../components/StatsCard'
import LoadingSpinner from '../components/LoadingSpinner'

const Dashboard: React.FC = () => {
  // Fetch vehicles for recent listings
  const { data: vehicles, isLoading: vehiclesLoading } = useQuery(
    'recent-vehicles',
    () => getVehicles({ limit: 6 }),
    { refetchInterval: 30000 } // Refresh every 30 seconds
  )

  // Fetch dashboard statistics
  const { data: stats, isLoading: statsLoading } = useQuery(
    'dashboard-stats',
    getDashboardStats,
    { refetchInterval: 60000 } // Refresh every minute
  )

  const isLoading = vehiclesLoading || statsLoading

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">
          Bienvenido a Autosell.mx - Tu Sistema de Gestión de Vehículos
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total de Vehículos"
          value={stats?.total_vehicles || 0}
          icon={Car}
          color="blue"
          change={stats?.vehicles_change || 0}
        />
        <StatsCard
          title="Vehículos Disponibles"
          value={stats?.available_vehicles || 0}
          icon={Car}
          color="green"
          change={stats?.available_change || 0}
        />
        <StatsCard
          title="Valor Total"
          value={`$${(stats?.total_value || 0).toLocaleString()}`}
          icon={DollarSign}
          color="purple"
          change={stats?.value_change || 0}
        />
        <StatsCard
          title="Fotos Subidas"
          value={stats?.total_photos || 0}
          icon={Camera}
          color="orange"
          change={stats?.photos_change || 0}
        />
      </div>

      {/* Recent Vehicles Section */}
      <div className="card">
        <div className="section-header">
          <h2 className="section-title">Vehículos Recientes</h2>
          <Link to="/vehicles" className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200">
            Ver Todos los Vehículos
          </Link>
        </div>

        {vehicles && vehicles.vehicles.length > 0 ? (
          <div className="vehicle-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {vehicles.vehicles.map((vehicle) => (
              <VehicleCard key={vehicle.id} vehicle={vehicle} />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <Car className="empty-state-icon" />
            <h3 className="empty-state-title">No hay vehículos aún</h3>
            <p className="empty-state-description">
              Comienza agregando tu primer vehículo al sistema.
            </p>
            <Link to="/vehicles/new" className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200">
              Agregar Primer Vehículo
            </Link>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
          <div className="space-y-3">
            <Link
              to="/vehicles/new"
              className="flex items-center space-x-3 p-3 rounded-lg border border-gray-200 hover:border-red-300 hover:bg-red-50 transition-colors duration-200"
            >
              <Plus className="h-5 w-5 text-red-600" />
              <span className="text-gray-700">Agregar Nuevo Vehículo</span>
            </Link>
            <Link
              to="/photos"
              className="flex items-center space-x-3 p-3 rounded-lg border border-gray-200 hover:border-red-300 hover:bg-red-50 transition-colors duration-200"
            >
              <Camera className="h-5 w-5 text-red-600" />
              <span className="text-gray-700">Gestionar Fotos</span>
            </Link>
            <Link
              to="/settings"
              className="flex items-center space-x-3 p-3 rounded-lg border border-gray-200 hover:border-red-300 hover:bg-red-50 transition-colors duration-200"
            >
              <Settings className="h-5 w-5 text-red-600" />
              <span className="text-gray-700">Configuración del Sistema</span>
            </Link>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">API Status</span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Healthy
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Database</span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Connected
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Photo Storage</span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Ready
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
