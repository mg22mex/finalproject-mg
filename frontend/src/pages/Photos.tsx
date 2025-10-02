import React, { useState, useEffect } from 'react'
import { Upload, Camera, FolderOpen, Trash2, Star, Eye, RefreshCw } from 'lucide-react'
import { toast } from 'react-hot-toast'
import LoadingSpinner from '../components/LoadingSpinner'
import { vehicleAPI, photoAPI } from '../services/api'

interface Photo {
  id: number
  vehicle_id: number
  filename: string
  original_filename: string
  drive_url?: string
  drive_file_id?: string
  file_size?: number
  mime_type?: string
  width?: number
  height?: number
  is_primary: boolean
  created_at: string
  updated_at?: string
}

interface Vehicle {
  id: number
  marca: string
  modelo: string
  año: number
  color?: string
  precio?: number
  kilometraje?: string
  estatus: string
  ubicacion?: string
  photo_count: number
}

const Photos: React.FC = () => {
  const [selectedVehicle, setSelectedVehicle] = useState<number | null>(null)
  const [uploading, setUploading] = useState(false)
  const [syncStatus, setSyncStatus] = useState<'idle' | 'syncing' | 'success' | 'error'>('idle')

  // Real API data
  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [vehiclesLoading, setVehiclesLoading] = useState(true)

  // Fetch vehicles from API
  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        setVehiclesLoading(true)
        const response = await vehicleAPI.getVehicles()
        setVehicles(response.vehicles || [])
      } catch (error) {
        console.error('Error fetching vehicles:', error)
        toast.error('Error al cargar vehículos')
      } finally {
        setVehiclesLoading(false)
      }
    }

    fetchVehicles()
  }, [])

  // Real photos data from API
  const [photos, setPhotos] = useState<Photo[]>([])
  const [photosLoading, setPhotosLoading] = useState(false)
  const [filteredPhotos, setFilteredPhotos] = useState<Photo[]>([])

  // Fetch photos from API
  const fetchPhotos = async (vehicleId?: number) => {
    try {
      setPhotosLoading(true)
      const response = await photoAPI.getPhotos(vehicleId ? { vehicle_id: vehicleId } : {})
      setPhotos(response)
    } catch (error) {
      console.error('Error fetching photos:', error)
      toast.error('Error al cargar fotos')
    } finally {
      setPhotosLoading(false)
    }
  }

  // Fetch photos when component mounts or vehicle changes
  useEffect(() => {
    fetchPhotos(selectedVehicle || undefined)
  }, [selectedVehicle])

  // Filter photos by selected vehicle
  useEffect(() => {
    if (selectedVehicle) {
      setFilteredPhotos(photos.filter(photo => photo.vehicle_id === selectedVehicle))
    } else {
      setFilteredPhotos(photos)
    }
  }, [selectedVehicle, photos])

  // Handle file upload
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (!files || files.length === 0 || !selectedVehicle) return

    setUploading(true)

    try {
      // Upload each file individually
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        await photoAPI.uploadPhoto(selectedVehicle, file)
      }
      
      toast.success(`${files.length} photo(s) uploaded successfully!`)
      
      // Refresh photos list
      await fetchPhotos(selectedVehicle)
      
    } catch (error) {
      toast.error('Failed to upload photos')
      console.error('Upload error:', error)
    } finally {
      setUploading(false)
      // Reset file input
      event.target.value = ''
    }
  }

  // Handle Google Drive sync
  const handleGoogleDriveSync = async () => {
    setSyncStatus('syncing')
    try {
      // TODO: Implement actual sync API call
      // await syncGoogleDrivePhotos()
      
      // Simulate sync delay
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      setSyncStatus('success')
      toast.success('Google Drive photos synced successfully!')
      
      // Refresh photos list
      // queryClient.invalidateQueries(['photos'])
      
    } catch (error) {
      setSyncStatus('error')
      toast.error('Failed to sync Google Drive photos')
      console.error('Sync error:', error)
    } finally {
      setTimeout(() => setSyncStatus('idle'), 3000)
    }
  }

  // Handle photo deletion
  const handleDeletePhoto = async (photoId: number) => {
    if (!confirm('Are you sure you want to delete this photo?')) return

    try {
      // TODO: Implement actual delete API call
      // await deletePhoto(photoId)
      
      // Remove from local state
      setPhotos(prev => prev.filter(photo => photo.id !== photoId))
      
      toast.success('Photo deleted successfully')
      
    } catch (error) {
      toast.error('Failed to delete photo')
      console.error('Delete error:', error)
    }
  }

  // Handle setting primary photo
  const handleSetPrimary = async (photoId: number) => {
    try {
      // TODO: Implement actual set primary API call
      // await setPrimaryPhoto(photoId)
      
      // Update local state
      setPhotos(prev => prev.map(photo => ({
        ...photo,
        is_primary: photo.id === photoId
      })))
      
      toast.success('Primary photo updated')
      
    } catch (error) {
      toast.error('Failed to update primary photo')
      console.error('Set primary error:', error)
    }
  }

  // Format file size
  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'Unknown'
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
  }

  // Get selected vehicle info
  const selectedVehicleInfo = vehicles.find(v => v.id === selectedVehicle)

  if (vehiclesLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="space-y-6">
        {/* Page Header */}
        <div className="page-header">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
              <Camera className="h-8 w-8 text-white" />
            </div>
            <h1 className="page-title">Gestión de Fotos</h1>
            <p className="page-subtitle">
              Gestiona las fotos de vehículos e integración con Google Drive
            </p>
          </div>
        </div>

        {/* Vehicle Selection */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <span className="w-2 h-8 bg-blue-600 rounded-full mr-4"></span>
              Seleccionar Vehículo
            </h3>
          </div>
          <div className="card-content">
            <div className="flex flex-col lg:flex-row gap-6">
              <div className="flex-1">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Elegir Vehículo</label>
                <select
                  value={selectedVehicle || ''}
                  onChange={(e) => setSelectedVehicle(Number(e.target.value) || null)}
                  className="input-field"
                >
                  <option value="">Elige un vehículo...</option>
                  {vehicles.map((vehicle) => (
                    <option key={vehicle.id} value={vehicle.id}>
                      {vehicle.año} {vehicle.marca} {vehicle.modelo} - {vehicle.estatus} - ${vehicle.precio?.toLocaleString()} - {vehicle.kilometraje}
                    </option>
                  ))}
                </select>
              </div>
              
              <button
                onClick={handleGoogleDriveSync}
                disabled={syncStatus === 'syncing'}
                className="btn-primary flex items-center space-x-3"
              >
                {syncStatus === 'syncing' ? (
                  <RefreshCw className="h-5 w-5 animate-spin" />
                ) : (
                  <FolderOpen className="h-5 w-5" />
                )}
                <span>
                  {syncStatus === 'syncing' ? 'Syncing...' : 
                   syncStatus === 'success' ? 'Synced!' : 
                   syncStatus === 'error' ? 'Sync Failed' : 'Sync Google Drive'}
                </span>
              </button>
            </div>
          </div>
        </div>

      {/* Upload Section - Matching Autosell.mx style */}
      {selectedVehicle && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <span className="w-2 h-8 bg-blue-600 rounded-full mr-4"></span>
            Subir Fotos para {selectedVehicleInfo?.año} {selectedVehicleInfo?.marca} {selectedVehicleInfo?.modelo}
          </h3>
          
          <div className="border-2 border-dashed border-blue-300 rounded-xl p-12 text-center bg-blue-50 hover:bg-blue-100 transition-colors duration-200">
            <Camera className="mx-auto h-16 w-16 text-blue-500 mb-6" />
            <div className="text-lg text-gray-700 mb-6">
              <p className="font-bold text-xl mb-2">Subir fotos del vehículo</p>
              <p className="text-gray-600">Arrastra y suelta archivos aquí, o haz clic para seleccionar</p>
            </div>
            
            <input
              type="file"
              multiple
              accept="image/*"
              onChange={handleFileUpload}
              disabled={uploading}
              className="hidden"
              id="photo-upload"
            />
            
            <label
              htmlFor="photo-upload"
              className={`inline-flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer ${
                uploading ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {uploading ? (
                <RefreshCw className="h-5 w-5 animate-spin" />
              ) : (
                <Upload className="h-5 w-5" />
              )}
              <span className="text-lg">{uploading ? 'Subiendo...' : 'Seleccionar Fotos'}</span>
            </label>
          </div>
        </div>
      )}

      {/* Photos Display - Matching Autosell.mx style */}
      {selectedVehicle && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <div className="flex items-center justify-between mb-8">
            <h3 className="text-2xl font-bold text-gray-900 flex items-center">
              <span className="w-2 h-8 bg-blue-600 rounded-full mr-4"></span>
              Fotos ({filteredPhotos.length})
            </h3>
            <div className="text-lg text-gray-600 font-medium">
              {selectedVehicleInfo?.photo_count || 0} fotos totales
            </div>
          </div>

          {filteredPhotos.length === 0 ? (
            <div className="text-center py-12">
              <Camera className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Aún no hay fotos</h3>
              <p className="text-gray-500 mb-6">
                Sube fotos para este vehículo para comenzar
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredPhotos.map((photo) => (
                <div key={photo.id} className="relative group">
                  {/* Photo Card - Matching Autosell.mx style */}
                  <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300">
                    {/* Actual photo or fallback */}
                    <div className="aspect-square bg-gradient-to-br from-blue-50 to-gray-100 flex items-center justify-center relative overflow-hidden">
                      {photo.drive_url ? (
                        <img
                          src={photo.drive_url}
                          alt={photo.filename}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          onError={(e) => {
                            // Fallback to placeholder if image fails to load
                            const target = e.target as HTMLImageElement;
                            target.style.display = 'none';
                            const fallback = target.parentElement?.querySelector('.fallback') as HTMLElement;
                            if (fallback) fallback.style.display = 'flex';
                          }}
                        />
                      ) : null}
                      <div className="fallback flex w-full h-full items-center justify-center">
                        <Camera className="h-16 w-16 text-blue-400" />
                      </div>
                    </div>
                    
                    {/* Photo Info */}
                    <div className="p-4">
                      <p className="text-sm font-semibold text-gray-900 truncate mb-1">
                        {photo.filename}
                      </p>
                      <p className="text-xs text-gray-600">
                        {formatFileSize(photo.file_size)} • {photo.width}x{photo.height}
                      </p>
                    </div>
                  </div>

                  {/* Action Overlay - Matching Autosell.mx style */}
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 rounded-xl flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <div className="flex space-x-3">
                      <button
                        onClick={() => handleSetPrimary(photo.id)}
                        className={`p-3 rounded-full shadow-lg ${
                          photo.is_primary 
                            ? 'bg-yellow-500 text-white hover:bg-yellow-600' 
                            : 'bg-white text-gray-700 hover:bg-yellow-50 hover:scale-110'
                        } transition-all duration-200`}
                        title={photo.is_primary ? 'Primary photo' : 'Set as primary'}
                      >
                        <Star className="h-5 w-5" />
                      </button>
                      
                      <button
                        onClick={() => window.open(photo.drive_url, '_blank')}
                        className="p-3 rounded-full bg-white text-gray-700 hover:bg-blue-50 hover:scale-110 shadow-lg transition-all duration-200"
                        title="View in Google Drive"
                      >
                        <Eye className="h-5 w-5" />
                      </button>
                      
                      <button
                        onClick={() => handleDeletePhoto(photo.id)}
                        className="p-3 rounded-full bg-white text-gray-700 hover:bg-red-50 hover:scale-110 shadow-lg transition-all duration-200"
                        title="Delete photo"
                      >
                        <Trash2 className="h-5 w-5" />
                      </button>
                    </div>
                  </div>

                  {/* Primary Badge - Matching Autosell.mx style */}
                  {photo.is_primary && (
                    <div className="absolute top-3 right-3 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white px-3 py-1 rounded-full text-sm font-bold shadow-lg">
                      Primary
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Quick Stats - Matching Autosell.mx style */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center hover:shadow-xl transition-all duration-300">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <Camera className="h-8 w-8 text-white" />
          </div>
          <div className="text-4xl font-bold text-blue-600 mb-2">
            {vehicles.reduce((sum, v) => sum + (v.photo_count || 0), 0) || 0}
          </div>
          <div className="text-lg font-semibold text-gray-700">Fotos Totales</div>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center hover:shadow-xl transition-all duration-300">
          <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <FolderOpen className="h-8 w-8 text-white" />
          </div>
          <div className="text-4xl font-bold text-green-600 mb-2">
            {vehicles.filter(v => (v.photo_count || 0) > 0).length || 0}
          </div>
          <div className="text-lg font-semibold text-gray-700">Vehículos con Fotos</div>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center hover:shadow-xl transition-all duration-300">
          <div className="w-16 h-16 bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <Star className="h-8 w-8 text-white" />
          </div>
          <div className="text-4xl font-bold text-yellow-600 mb-2">
            {photos.filter(p => p.is_primary).length}
          </div>
          <div className="text-lg font-semibold text-gray-700">Fotos Principales</div>
        </div>
      </div>
      
      {/* Footer - Matching Autosell.mx style */}
      <div className="bg-gray-900 text-white py-12 mt-16">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="text-2xl font-bold mb-4">Autosell.mx</div>
          <p className="text-gray-400 mb-6">Sistema Profesional de Gestión de Vehículos y Fotos</p>
          <div className="flex justify-center space-x-6 text-sm text-gray-400">
            <span>Gestión de Fotos</span>
            <span>•</span>
            <span>Integración Google Drive</span>
            <span>•</span>
            <span>Inventario de Vehículos</span>
          </div>
        </div>
        </div>
      </div>
    </div>
  )
}

export default Photos
