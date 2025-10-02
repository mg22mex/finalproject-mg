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
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '16rem'}}>
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="dashboard">
      {/* Page Header */}
      <div>
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="welcome-message">
          Bienvenido a Autosell.mx - Tu Sistema de Gestión de Vehículos
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <StatsCard
          title="Total de Vehículos"
          value={stats?.total_vehicles || 0}
          icon={Car}
          color="blue"
          change={stats?.vehicles_change || 0}
          subtitle={`${stats?.available_vehicles || 0} disponibles`}
        />
        <StatsCard
          title="Vehículos Disponibles"
          value={stats?.available_vehicles || 0}
          icon={Car}
          color="green"
          change={stats?.available_change || 0}
          subtitle={`${stats?.sold_vehicles || 0} vendidos`}
        />
        <StatsCard
          title="Valor Total"
          value={`$${(stats?.total_value || 0).toLocaleString()}`}
          icon={DollarSign}
          color="purple"
          change={stats?.value_change || 0}
          subtitle={`Promedio: $${(stats?.average_price || 0).toLocaleString()}`}
        />
        <StatsCard
          title="Fotos Subidas"
          value={stats?.total_photos || 0}
          icon={Camera}
          color="orange"
          change={stats?.photos_change || 0}
          subtitle={`${stats?.vehicles_with_photos || 0} vehículos con fotos`}
        />
      </div>

      {/* Recent Vehicles Section */}
      <div className="card">
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem'}}>
          <h2 className="card-title">Vehículos Recientes</h2>
          <Link to="/vehicles" className="btn btn-primary">
            Ver Todos los Vehículos
          </Link>
        </div>

        {vehicles && vehicles.vehicles.length > 0 ? (
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem'}}>
            {vehicles.vehicles.map((vehicle) => (
              <VehicleCard key={vehicle.id} vehicle={vehicle} />
            ))}
          </div>
        ) : (
          <div style={{textAlign: 'center', padding: '2rem'}}>
            <Car style={{width: '4rem', height: '4rem', margin: '0 auto 1rem', color: '#6b7280'}} />
            <h3 style={{fontSize: '1.25rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.5rem'}}>No hay vehículos aún</h3>
            <p style={{color: '#6b7280', marginBottom: '1.5rem'}}>
              Comienza agregando tu primer vehículo al sistema.
            </p>
            <Link to="/vehicles/new" className="btn btn-primary">
              Agregar Primer Vehículo
            </Link>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem'}}>
        <div className="card">
          <h3 className="card-title">Acciones Rápidas</h3>
          <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
            <Link
              to="/photos"
              style={{display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e5e7eb', textDecoration: 'none', color: '#374151', transition: 'all 0.2s'}}
            >
              <Camera style={{width: '1.25rem', height: '1.25rem', color: '#dc2626'}} />
              <span>Gestionar Fotos</span>
            </Link>
            <Link
              to="/settings"
              style={{display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e5e7eb', textDecoration: 'none', color: '#374151', transition: 'all 0.2s'}}
            >
              <Settings style={{width: '1.25rem', height: '1.25rem', color: '#dc2626'}} />
              <span>Configuración del Sistema</span>
            </Link>
          </div>
        </div>

        <div className="card">
          <h3 className="card-title">System Status</h3>
          <div className="system-status">
            <div className="status-item">
              <span style={{color: '#6b7280'}}>API Status</span>
              <span className="status">Healthy</span>
            </div>
            <div className="status-item">
              <span style={{color: '#6b7280'}}>Database</span>
              <span className="status">Connected</span>
            </div>
            <div className="status-item">
              <span style={{color: '#6b7280'}}>Photo Storage</span>
              <span className="status">Ready</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
