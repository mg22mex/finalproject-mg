import React from 'react'
import { Link } from 'react-router-dom'
import { Eye, Edit, Trash2, Camera, MapPin, Calendar, Gauge } from 'lucide-react'
import { Vehicle } from '../types/vehicle'

interface VehicleCardProps {
  vehicle: Vehicle
  onEdit?: (vehicle: Vehicle) => void
  onDelete?: (vehicle: Vehicle) => void
}

const VehicleCard: React.FC<VehicleCardProps> = ({ vehicle, onEdit, onDelete }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Disponible':
        return 'status-disponible'
      case 'FOTOS':
        return 'status-fotos'
      case 'AUSENTE':
        return 'status-ausente'
      case 'Apartado':
        return 'status-apartado'
      case 'Vendido':
        return 'status-vendido'
      default:
        return 'status-disponible'
    }
  }

  const formatPrice = (price: number | null | undefined) => {
    if (!price) return 'Precio a consultar'
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
      minimumFractionDigits: 0,
    }).format(price)
  }

  return (
    <div className="vehicle-card bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Vehicle Image */}
      <div className="relative">
        {vehicle.photo_count > 0 ? (
          <img
            src={`/api/vehicles/${vehicle.id}/primary-photo`}
            alt={`${vehicle.marca} ${vehicle.modelo}`}
            className="vehicle-image w-full h-48 object-cover"
            onError={(e) => {
              const target = e.target as HTMLImageElement
              target.src = '/placeholder-vehicle.jpg'
            }}
          />
        ) : (
          <div className="vehicle-image w-full h-48 bg-gray-200 flex items-center justify-center">
            <Camera className="h-12 w-12 text-gray-400" />
          </div>
        )}
        
        {/* Status Badge */}
        <div className="absolute top-3 right-3">
          <span className={`status-badge ${getStatusColor(vehicle.estatus)}`}>
            {vehicle.estatus}
          </span>
        </div>

        {/* Photo Count Badge */}
        {vehicle.photo_count > 0 && (
          <div className="absolute bottom-3 left-3 bg-black bg-opacity-75 text-white px-2 py-1 rounded-md text-xs">
            {vehicle.photo_count} foto{vehicle.photo_count !== 1 ? 's' : ''}
          </div>
        )}
      </div>

      {/* Vehicle Information */}
      <div className="vehicle-info p-4">
        <h3 className="vehicle-title text-lg font-semibold text-gray-900 mb-2">
          {vehicle.año} {vehicle.marca} {vehicle.modelo}
        </h3>
        
        <div className="vehicle-price text-2xl font-bold text-blue-600 mb-3">
          {formatPrice(vehicle.precio)}
        </div>

        <div className="vehicle-details space-y-2 mb-4">
          {vehicle.color && (
            <div className="flex items-center text-sm text-gray-600">
              <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: vehicle.color }}></div>
              <span>{vehicle.color}</span>
            </div>
          )}
          
          {vehicle.kilometraje && (
            <div className="flex items-center text-sm text-gray-600">
              <Gauge className="h-4 w-4 mr-2 text-gray-400" />
              <span>{vehicle.kilometraje}</span>
            </div>
          )}
          
          {vehicle.ubicacion && (
            <div className="flex items-center text-sm text-gray-600">
              <MapPin className="h-4 w-4 mr-2 text-gray-400" />
              <span>{vehicle.ubicacion}</span>
            </div>
          )}
          
          <div className="flex items-center text-sm text-gray-600">
            <Calendar className="h-4 w-4 mr-2 text-gray-400" />
            <span>ID: {vehicle.external_id || vehicle.id}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-100">
          <Link
            to={`/vehicles/${vehicle.id}`}
            className="flex items-center space-x-1 text-blue-600 hover:text-blue-700 text-sm font-medium transition-colors duration-200"
          >
            <Eye className="h-4 w-4" />
            <span>Ver</span>
          </Link>

          <div className="flex items-center space-x-2">
            {onEdit && (
              <button
                onClick={() => onEdit(vehicle)}
                className="flex items-center space-x-1 text-gray-600 hover:text-gray-800 text-sm font-medium transition-colors duration-200"
              >
                <Edit className="h-4 w-4" />
                <span>Editar</span>
              </button>
            )}
            
            {onDelete && (
              <button
                onClick={() => onDelete(vehicle)}
                className="flex items-center space-x-1 text-red-600 hover:text-red-700 text-sm font-medium transition-colors duration-200"
              >
                <Trash2 className="h-4 w-4" />
                <span>Eliminar</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default VehicleCard
