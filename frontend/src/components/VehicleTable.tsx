import React from 'react'
import { Link } from 'react-router-dom'
import { Eye, Edit, Trash2, Camera } from 'lucide-react'
import { Vehicle } from '../types/vehicle'

interface VehicleTableProps {
  vehicles: Vehicle[]
  onEdit?: (vehicle: Vehicle) => void
  onDelete?: (vehicle: Vehicle) => void
}

const VehicleTable: React.FC<VehicleTableProps> = ({ vehicles, onEdit, onDelete }) => {
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
    <div className="table-container">
      <table className="data-table">
        <thead className="table-header">
          <tr>
            <th className="table-header-cell">Vehicle</th>
            <th className="table-header-cell">Price</th>
            <th className="table-header-cell">Status</th>
            <th className="table-header-cell">Location</th>
            <th className="table-header-cell">Photos</th>
            <th className="table-header-cell">Actions</th>
          </tr>
        </thead>
        <tbody className="table-body">
          {vehicles.map((vehicle) => (
            <tr key={vehicle.id} className="table-row">
              <td className="table-cell">
                <div>
                  <div className="font-medium text-gray-900">
                    {vehicle.año} {vehicle.marca} {vehicle.modelo}
                  </div>
                  <div className="text-sm text-gray-500">
                    ID: {vehicle.external_id || vehicle.id}
                  </div>
                  {vehicle.color && (
                    <div className="text-sm text-gray-500">
                      Color: {vehicle.color}
                    </div>
                  )}
                </div>
              </td>
              <td className="table-cell">
                <div className="font-medium text-gray-900">
                  {formatPrice(vehicle.precio)}
                </div>
              </td>
              <td className="table-cell">
                <span className={`status-badge ${getStatusColor(vehicle.estatus)}`}>
                  {vehicle.estatus}
                </span>
              </td>
              <td className="table-cell">
                <div className="text-sm text-gray-900">
                  {vehicle.ubicacion || 'No especificada'}
                </div>
              </td>
              <td className="table-cell">
                <div className="flex items-center space-x-2">
                  <Camera className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-900">
                    {vehicle.photo_count} foto{vehicle.photo_count !== 1 ? 's' : ''}
                  </span>
                </div>
              </td>
              <td className="table-cell">
                <div className="flex items-center space-x-3">
                  <Link
                    to={`/vehicles/${vehicle.id}`}
                    className="text-blue-600 hover:text-blue-700 transition-colors duration-200"
                  >
                    <Eye className="h-4 w-4" />
                  </Link>
                  
                  {onEdit && (
                    <button
                      onClick={() => onEdit(vehicle)}
                      className="text-gray-600 hover:text-gray-800 transition-colors duration-200"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                  )}
                  
                  {onDelete && (
                    <button
                      onClick={() => onDelete(vehicle)}
                      className="text-red-600 hover:text-red-700 transition-colors duration-200"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default VehicleTable
