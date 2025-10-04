import axios from 'axios'
import { Vehicle, VehicleCreate, VehicleUpdate, VehicleListResponse, VehicleFilters, DashboardStats } from '../types/vehicle'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Vehicle API endpoints
export const vehicleAPI = {
  // Get all vehicles with filters and pagination
  getVehicles: async (filters: VehicleFilters = {}): Promise<VehicleListResponse> => {
    try {
      const params = new URLSearchParams()
      
      // Sanitize and add filters to query params (omit empty values)
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '' && value !== 0) {
          params.append(key, value.toString())
        }
      })
      
      const queryString = params.toString()
      const url = queryString ? `/vehicles/?${queryString}` : '/vehicles/'
      
      console.log(`Fetching vehicles with URL: ${url}`)
      const response = await api.get(url)
      return response.data
    } catch (error: any) {
      console.error('Error fetching vehicles with filters:', error)
      
      // If the request failed with 422 or 500, try a simple GET request
      if (error.response?.status === 422 || error.response?.status === 500) {
        console.log('Falling back to simple GET /vehicles/')
        try {
          const response = await api.get('/vehicles/')
          return response.data
        } catch (fallbackError: any) {
          console.error('Fallback request also failed:', fallbackError)
          throw fallbackError
        }
      }
      
      throw error
    }
  },

  // Get a single vehicle by ID
  getVehicle: async (id: number): Promise<Vehicle> => {
    const response = await api.get(`/vehicles/${id}`)
    return response.data
  },

  // Create a new vehicle
  createVehicle: async (vehicle: VehicleCreate): Promise<Vehicle> => {
    const response = await api.post('/vehicles/', vehicle)
    return response.data
  },

  // Update an existing vehicle
  updateVehicle: async (id: number, vehicle: VehicleUpdate): Promise<Vehicle> => {
    const response = await api.put(`/vehicles/${id}`, vehicle)
    return response.data
  },

  // Delete a vehicle
  deleteVehicle: async (id: number): Promise<void> => {
    await api.delete(`/vehicles/${id}`)
  },

  // Update vehicle status
  updateVehicleStatus: async (id: number, status: string, changedBy: string, reason?: string, notes?: string): Promise<Vehicle> => {
    const response = await api.patch(`/vehicles/${id}/status`, {
      estatus: status,
      changed_by: changedBy,
      reason,
      notes,
    })
    return response.data
  },

  // Search vehicles
  searchVehicles: async (query: string, filters: Omit<VehicleFilters, 'search'> = {}): Promise<VehicleListResponse> => {
    const params = new URLSearchParams()
    params.append('search', query)
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString())
      }
    })
    
    const response = await api.get(`/vehicles/search/${query}?${params.toString()}`)
    return response.data
  },

  // Get vehicles by status
  getVehiclesByStatus: async (status: string, filters: Omit<VehicleFilters, 'estatus'> = {}): Promise<VehicleListResponse> => {
    const params = new URLSearchParams()
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString())
      }
    })
    
    const response = await api.get(`/vehicles/status/${status}?${params.toString()}`)
    return response.data
  },
}

// Dashboard API endpoints
export const dashboardAPI = {
  // Get dashboard statistics
  getDashboardStats: async (): Promise<DashboardStats> => {
    const response = await api.get('/dashboard/stats')
    const data = response.data
    
    // Map backend response to frontend DashboardStats interface
    const stats: DashboardStats = {
      total_vehicles: data.total_vehicles || 0,
      available_vehicles: data.available_vehicles || 0,
      sold_vehicles: data.sold_vehicles || 0,
      reserved_vehicles: data.reserved_vehicles || 0,
      temporarily_unavailable_vehicles: data.unavailable_vehicles || 0,
      average_price: data.average_price || 0,
      total_value: data.total_value || 0,
      vehicles_change: data.vehicles_change || 0,
      available_change: data.available_change || 0,
      value_change: data.value_change || 0,
      total_photos: data.total_photos || 0,
      photos_change: data.photos_change || 0,
      vehicles_with_photos: data.vehicles_with_photos || 0,
      primary_photos: data.primary_photos || 0,
    }
    
    return stats
  },
}

// Photo API endpoints
export const photoAPI = {
  // Get all photos with filters
  getPhotos: async (filters: any = {}) => {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString())
      }
    })
    const response = await api.get(`/photos/?${params.toString()}`)
    return response.data
  },

  // Get photos for a specific vehicle
  getVehiclePhotos: async (vehicleId: number) => {
    const response = await api.get(`/photos/vehicle/${vehicleId}`)
    return response.data
  },

  // Get a specific photo
  getPhoto: async (photoId: number) => {
    const response = await api.get(`/photos/${photoId}`)
    return response.data
  },

  // Upload a photo
  uploadPhoto: async (vehicleId: number, file: File, description?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    if (description) {
      formData.append('description', description)
    }
    
    const response = await api.post(`/photos/upload/${vehicleId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Update photo information
  updatePhoto: async (photoId: number, updates: any) => {
    const response = await api.put(`/photos/${photoId}`, updates)
    return response.data
  },

  // Delete a photo
  deletePhoto: async (photoId: number) => {
    await api.delete(`/photos/${photoId}`)
  },

  // Set photo as primary
  setPrimaryPhoto: async (vehicleId: number, photoId: number) => {
    const response = await api.post(`/photos/vehicle/${vehicleId}/photos/${photoId}/set-primary`)
    return response.data
  },

  // Get photo statistics
  getPhotoStats: async () => {
    const response = await api.get('/photos/stats/overview')
    return response.data
  },

  // Sync Google Drive photos
  syncGoogleDrivePhotos: async () => {
    const response = await api.post('/photos/sync/google-drive')
    return response.data
  },

  // Search photos
  searchPhotos: async (query: string, filters: any = {}) => {
    const params = new URLSearchParams()
    params.append('query', query)
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString())
      }
    })
    const response = await api.get(`/photos/search?${params.toString()}`)
    return response.data
  },
}

// Google Drive API
export const driveAPI = {
  // Test Drive connection
  testConnection: async () => {
    const response = await api.post('/drive/test-connection')
    return response.data
  },

  // Create Drive folder for vehicle
  createFolder: async (vehicleId: number) => {
    const response = await api.post(`/drive/create-folder/${vehicleId}`)
    return response.data
  },

  // Sync photos from Drive folder
  syncPhotos: async (vehicleId: number) => {
    const response = await api.post(`/drive/sync-photos/${vehicleId}`)
    return response.data
  },

  // Get vehicle folder info
  getFolderInfo: async (vehicleId: number) => {
    const response = await api.get(`/drive/vehicle/${vehicleId}/folder-info`)
    return response.data
  },

  // List files in Drive folder
  listFolderFiles: async (folderId: string) => {
    const response = await api.get(`/drive/folder/${folderId}/files`)
    return response.data
  }
}

// Health check API
export const healthAPI = {
  // Basic health check
  getHealth: async () => {
    const response = await api.get('/health')
    return response.data
  },

  // Detailed health check
  getDetailedHealth: async () => {
    const response = await api.get('/health/detailed')
    return response.data
  },
}

// Convenience functions for React Query
export const getVehicles = (filters: VehicleFilters = {}) => vehicleAPI.getVehicles(filters)
export const getVehicle = (id: number) => vehicleAPI.getVehicle(id)
export const createVehicle = (vehicle: VehicleCreate) => vehicleAPI.createVehicle(vehicle)
export const updateVehicle = (id: number, vehicle: VehicleUpdate) => vehicleAPI.updateVehicle(id, vehicle)
export const deleteVehicle = (id: number) => vehicleAPI.deleteVehicle(id)
export const getDashboardStats = () => dashboardAPI.getDashboardStats()

// Photo convenience functions
export const getPhotos = (filters: any = {}) => photoAPI.getPhotos(filters)
export const getVehiclePhotos = (vehicleId: number) => photoAPI.getVehiclePhotos(vehicleId)
export const uploadPhoto = (vehicleId: number, file: File, description?: string) => photoAPI.uploadPhoto(vehicleId, file, description)
export const updatePhoto = (photoId: number, updates: any) => photoAPI.updatePhoto(photoId, updates)
export const deletePhoto = (photoId: number) => photoAPI.deletePhoto(photoId)
export const setPrimaryPhoto = (vehicleId: number, photoId: number) => photoAPI.setPrimaryPhoto(vehicleId, photoId)
export const getPhotoStats = () => photoAPI.getPhotoStats()
export const syncGoogleDrivePhotos = () => photoAPI.syncGoogleDrivePhotos()
export const searchPhotos = (query: string, filters: any = {}) => photoAPI.searchPhotos(query, filters)

export default api
