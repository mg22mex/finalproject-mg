export interface Vehicle {
  id: number
  external_id?: string
  marca: string
  modelo: string
  año: number
  color?: string
  precio?: number
  kilometraje?: string
  estatus: VehicleStatus
  ubicacion?: string
  descripcion?: string
  caracteristicas?: Record<string, any>
  created_at: string
  updated_at: string
  created_by?: string
  updated_by?: string
  photo_count: number
  is_available: boolean
  is_sold: boolean
  is_reserved: boolean
  is_temporarily_unavailable: boolean
}

export type VehicleStatus = 'Disponible' | 'FOTOS' | 'AUSENTE' | 'Apartado' | 'Vendido'

export interface VehicleCreate {
  external_id?: string
  marca: string
  modelo: string
  año: number
  color?: string
  precio?: number
  kilometraje?: string
  estatus: VehicleStatus
  ubicacion?: string
  descripcion?: string
  caracteristicas?: Record<string, any>
  created_by?: string
}

export interface VehicleUpdate {
  external_id?: string
  marca?: string
  modelo?: string
  año?: number
  color?: string
  precio?: number
  kilometraje?: string
  estatus?: VehicleStatus
  ubicacion?: string
  descripcion?: string
  caracteristicas?: Record<string, any>
}

export interface VehicleListResponse {
  vehicles: Vehicle[]
  total: number
  skip: number
  limit: number
}

export interface VehicleFilters {
  marca?: string
  modelo?: string
  año?: string
  estatus?: string
  precio_min?: string
  precio_max?: string
  search?: string
  skip?: number
  limit?: number
}

export interface DashboardStats {
  total_vehicles: number
  available_vehicles: number
  sold_vehicles: number
  reserved_vehicles: number
  temporarily_unavailable_vehicles: number
  average_price?: number
  total_value?: number
  vehicles_change: number
  available_change: number
  value_change: number
  total_photos: number
  photos_change: number
  vehicles_with_photos?: number
  primary_photos?: number
}
