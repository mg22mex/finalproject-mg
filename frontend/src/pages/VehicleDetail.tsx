import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { ArrowLeft, Car, Camera, Settings, Phone, MapPin, Calendar, DollarSign, Gauge, Palette, FileText, CheckCircle, Star } from 'lucide-react'
import { Link } from 'react-router-dom'
import DriveFolderManager from '../components/DriveFolderManager'

interface Vehicle {
  id: number
  external_id: string
  marca: string
  modelo: string
  año: number
  color: string
  precio: number
  kilometraje: string
  estatus: string
  ubicacion: string
  descripcion: string
  caracteristicas: string | null
  created_at: string
  updated_at: string
  photo_count: number
  is_available: boolean
  is_sold: boolean
  is_reserved: boolean
  is_temporarily_unavailable: boolean
  drive_folder_id?: string
  drive_folder_url?: string
}

const VehicleDetail: React.FC = () => {
  const { id } = useParams()
  const [vehicle, setVehicle] = useState<Vehicle | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      fetchVehicle(parseInt(id))
    }
  }, [id])

  const fetchVehicle = async (vehicleId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/vehicles/${vehicleId}`)
      if (response.ok) {
        const data = await response.json()
        setVehicle(data)
      }
    } catch (error) {
      console.error('Error fetching vehicle:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFolderCreated = (folderInfo: any) => {
    if (vehicle) {
      setVehicle({
        ...vehicle,
        drive_folder_id: folderInfo.folder_id,
        drive_folder_url: folderInfo.folder_url
      })
    }
  }

  if (loading) {
    return (
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '64vh'}}>
        <div style={{textAlign: 'center'}}>
          <div style={{
            width: '2rem', 
            height: '2rem', 
            border: '2px solid #e5e7eb', 
            borderTop: '2px solid #2563eb', 
            borderRadius: '50%', 
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }}></div>
          <p style={{color: '#6b7280'}}>Loading vehicle details...</p>
        </div>
      </div>
    )
  }

  if (!vehicle) {
    return (
      <div className="page-container">
        <div className="card">
          <h1 className="page-title">Vehicle Not Found</h1>
          <p className="page-subtitle">The requested vehicle could not be found.</p>
          <Link to="/vehicles" className="btn-primary">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Vehicles
          </Link>
        </div>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'DISPONIBLE': return '#10b981'
      case 'VENDIDO': return '#ef4444'
      case 'APARTADO': return '#f59e0b'
      case 'AUSENTE': return '#6b7280'
      default: return '#6b7280'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'DISPONIBLE': return 'Disponible'
      case 'VENDIDO': return 'Vendido'
      case 'APARTADO': return 'Apartado'
      case 'AUSENTE': return 'Ausente'
      default: return status
    }
  }

  return (
    <div style={{minHeight: '100vh', backgroundColor: '#f9fafb'}}>
      {/* Header */}
      <div style={{
        backgroundColor: 'white', 
        borderBottom: '1px solid #e5e7eb', 
        padding: '1rem 0'
      }}>
        <div className="container" style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
            <Link to="/vehicles" style={{
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.5rem', 
              padding: '0.5rem 1rem', 
              backgroundColor: '#f3f4f6', 
              color: '#374151', 
              textDecoration: 'none', 
              borderRadius: '0.375rem',
              border: '1px solid #d1d5db'
            }}>
              <ArrowLeft style={{width: '1rem', height: '1rem'}} />
              Back to Vehicles
            </Link>
          </div>
          <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <span style={{
              padding: '0.25rem 0.75rem', 
              backgroundColor: getStatusColor(vehicle.estatus), 
              color: 'white', 
              borderRadius: '9999px', 
              fontSize: '0.875rem', 
              fontWeight: '500'
            }}>
              {getStatusText(vehicle.estatus)}
            </span>
          </div>
        </div>
      </div>

      <div className="container" style={{padding: '2rem 0'}}>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem'}}>
          {/* Left Side - Vehicle Images */}
          <div>
            <div style={{
              backgroundColor: 'white', 
              borderRadius: '0.5rem', 
              padding: '1.5rem', 
              boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
              marginBottom: '1rem'
            }}>
              <div style={{
                width: '100%', 
                height: '400px', 
                backgroundColor: '#f3f4f6', 
                borderRadius: '0.375rem', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                marginBottom: '1rem'
              }}>
                <div style={{textAlign: 'center'}}>
                  <Camera style={{width: '4rem', height: '4rem', color: '#9ca3af', margin: '0 auto 1rem'}} />
                  <p style={{color: '#6b7280', fontSize: '1.125rem'}}>No photos available</p>
                  <p style={{color: '#9ca3af', fontSize: '0.875rem'}}>Upload photos to showcase this vehicle</p>
                </div>
              </div>
              
              {/* Thumbnail Images */}
              <div style={{display: 'flex', gap: '0.5rem'}}>
                {[1, 2, 3].map((i) => (
                  <div key={i} style={{
                    width: '80px', 
                    height: '80px', 
                    backgroundColor: '#f3f4f6', 
                    borderRadius: '0.375rem', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center'
                  }}>
                    <Camera style={{width: '1.5rem', height: '1.5rem', color: '#9ca3af'}} />
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Side - Vehicle Details */}
          <div>
            <div style={{
              backgroundColor: 'white', 
              borderRadius: '0.5rem', 
              padding: '1.5rem', 
              boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
            }}>
              {/* Vehicle Title */}
              <div style={{marginBottom: '1.5rem'}}>
                <h1 style={{
                  fontSize: '1.875rem', 
                  fontWeight: '700', 
                  color: '#1f2937', 
                  marginBottom: '0.5rem'
                }}>
                  {vehicle.marca} {vehicle.modelo} {vehicle.año}
                </h1>
                <p style={{color: '#6b7280', fontSize: '1rem'}}>
                  {vehicle.descripcion || `${vehicle.marca} ${vehicle.modelo} ${vehicle.año}`}
                </p>
              </div>

              {/* Vehicle Specifications */}
              <div style={{marginBottom: '2rem'}}>
                <h3 style={{
                  fontSize: '1.25rem', 
                  fontWeight: '600', 
                  color: '#1f2937', 
                  marginBottom: '1rem'
                }}>
                  Especificaciones
                </h3>
                
                <div style={{display: 'grid', gap: '0.75rem'}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.75rem'}}>
                    <Calendar style={{width: '1.25rem', height: '1.25rem', color: '#6b7280'}} />
                    <span style={{color: '#6b7280', fontSize: '0.875rem'}}>Año:</span>
                    <span style={{fontWeight: '500', color: '#1f2937'}}>{vehicle.año}</span>
                  </div>
                  
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.75rem'}}>
                    <Gauge style={{width: '1.25rem', height: '1.25rem', color: '#6b7280'}} />
                    <span style={{color: '#6b7280', fontSize: '0.875rem'}}>Kilometraje:</span>
                    <span style={{fontWeight: '500', color: '#1f2937'}}>
                      {vehicle.kilometraje || 'No especificado'}
                    </span>
                  </div>
                  
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.75rem'}}>
                    <Palette style={{width: '1.25rem', height: '1.25rem', color: '#6b7280'}} />
                    <span style={{color: '#6b7280', fontSize: '0.875rem'}}>Color:</span>
                    <span style={{fontWeight: '500', color: '#1f2937'}}>{vehicle.color}</span>
                  </div>
                  
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.75rem'}}>
                    <MapPin style={{width: '1.25rem', height: '1.25rem', color: '#6b7280'}} />
                    <span style={{color: '#6b7280', fontSize: '0.875rem'}}>Ubicación:</span>
                    <span style={{fontWeight: '500', color: '#1f2937'}}>{vehicle.ubicacion}</span>
                  </div>
                  
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.75rem'}}>
                    <FileText style={{width: '1.25rem', height: '1.25rem', color: '#6b7280'}} />
                    <span style={{color: '#6b7280', fontSize: '0.875rem'}}>ID:</span>
                    <span style={{fontWeight: '500', color: '#1f2937', fontFamily: 'monospace'}}>
                      {vehicle.external_id}
                    </span>
                  </div>
                </div>
              </div>

              {/* Price */}
              <div style={{
                backgroundColor: '#f9fafb', 
                padding: '1.5rem', 
                borderRadius: '0.5rem', 
                marginBottom: '2rem'
              }}>
                <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem'}}>
                  <DollarSign style={{width: '1.25rem', height: '1.25rem', color: '#059669'}} />
                  <span style={{color: '#6b7280', fontSize: '0.875rem'}}>Precio</span>
                </div>
                <div style={{
                  fontSize: '2rem', 
                  fontWeight: '700', 
                  color: '#059669'
                }}>
                  {vehicle.precio > 0 ? `$${vehicle.precio.toLocaleString()}` : 'Precio a consultar'}
                </div>
              </div>

              {/* Action Buttons */}
              <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '2rem'}}>
                <button style={{
                  backgroundColor: '#dc2626', 
                  color: 'white', 
                  padding: '0.75rem 1.5rem', 
                  borderRadius: '0.375rem', 
                  border: 'none', 
                  fontSize: '1rem', 
                  fontWeight: '600', 
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem'
                }}>
                  <Star style={{width: '1.25rem', height: '1.25rem'}} />
                  ME INTERESA ESTE VEHÍCULO
                </button>
                
                <button style={{
                  backgroundColor: '#f3f4f6', 
                  color: '#374151', 
                  padding: '0.75rem 1.5rem', 
                  borderRadius: '0.375rem', 
                  border: '1px solid #d1d5db', 
                  fontSize: '1rem', 
                  fontWeight: '500', 
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem'
                }}>
                  <Phone style={{width: '1.25rem', height: '1.25rem'}} />
                  LLÁMANOS (614) 227 4381
                </button>
              </div>

              {/* Trust Information */}
              <div style={{
                backgroundColor: '#f0f9ff', 
                padding: '1rem', 
                borderRadius: '0.5rem', 
                border: '1px solid #bae6fd'
              }}>
                <h4 style={{
                  fontSize: '1rem', 
                  fontWeight: '600', 
                  color: '#1e40af', 
                  marginBottom: '0.75rem'
                }}>
                  Garantías y Seguridad
                </h4>
                <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                    <CheckCircle style={{width: '1rem', height: '1rem', color: '#059669'}} />
                    <span style={{fontSize: '0.875rem', color: '#374151'}}>
                      No manejamos autos de aseguradora.
                    </span>
                  </div>
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                    <CheckCircle style={{width: '1rem', height: '1rem', color: '#059669'}} />
                    <span style={{fontSize: '0.875rem', color: '#374151'}}>
                      Compra segura: garantía de papelería en regla.
                    </span>
                  </div>
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                    <CheckCircle style={{width: '1rem', height: '1rem', color: '#059669'}} />
                    <span style={{fontSize: '0.875rem', color: '#374151'}}>
                      Seguridad y legalidad en proceso de compra.
                    </span>
                  </div>
                  <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                    <CheckCircle style={{width: '1rem', height: '1rem', color: '#059669'}} />
                    <span style={{fontSize: '0.875rem', color: '#374151'}}>
                      Garantía interna de 3 meses.
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Drive Integration */}
        <div style={{marginTop: '2rem'}}>
          <DriveFolderManager
            vehicleId={vehicle.id}
            vehicleInfo={{
              marca: vehicle.marca,
              modelo: vehicle.modelo,
              año: vehicle.año?.toString()
            }}
            onFolderCreated={handleFolderCreated}
          />
        </div>

        {/* Quick Actions */}
        <div style={{
          backgroundColor: 'white', 
          borderRadius: '0.5rem', 
          padding: '1.5rem', 
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
          marginTop: '2rem'
        }}>
          <h3 style={{
            fontSize: '1.25rem', 
            fontWeight: '600', 
            color: '#1f2937', 
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Settings style={{width: '1.25rem', height: '1.25rem', color: '#6b7280'}} />
            Acciones Rápidas
          </h3>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem'}}>
            <Link to={`/photos?vehicle=${vehicle.id}`} style={{
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              gap: '0.5rem', 
              padding: '0.75rem 1rem', 
              backgroundColor: '#f3f4f6', 
              color: '#374151', 
              textDecoration: 'none', 
              borderRadius: '0.375rem',
              border: '1px solid #d1d5db'
            }}>
              <Camera style={{width: '1rem', height: '1rem'}} />
              <span>Gestionar Fotos</span>
            </Link>
            <button style={{
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              gap: '0.5rem', 
              padding: '0.75rem 1rem', 
              backgroundColor: '#f3f4f6', 
              color: '#374151', 
              border: '1px solid #d1d5db', 
              borderRadius: '0.375rem',
              cursor: 'pointer'
            }}>
              <Settings style={{width: '1rem', height: '1rem'}} />
              <span>Editar Vehículo</span>
            </button>
            <button style={{
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              gap: '0.5rem', 
              padding: '0.75rem 1rem', 
              backgroundColor: '#fef2f2', 
              color: '#dc2626', 
              border: '1px solid #fecaca', 
              borderRadius: '0.375rem',
              cursor: 'pointer'
            }}>
              <span>Eliminar Vehículo</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VehicleDetail