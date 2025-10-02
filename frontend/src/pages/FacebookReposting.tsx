import React, { useState, useEffect } from 'react'
import { Facebook, RefreshCw, Play, Settings, AlertCircle, Calendar, BarChart3, Zap, StopCircle, CheckCircle } from 'lucide-react'
import { toast } from 'react-hot-toast'

interface RepostingStatus {
  is_active: boolean
  last_posted?: string
  posts_last_week: number
  active_vehicles: number
  next_scheduled?: string
  total_posts: number
  workflow_name?: string
}

interface RepostingSchedule {
  is_active: boolean
  time_of_day: string
  days_of_week: number[]
  max_posts_per_day: number
  post_interval_hours: number
  include_marketplace: boolean
}

const FacebookReposting: React.FC = () => {
  const [status, setStatus] = useState<RepostingStatus | null>(null)
  const [schedule, setSchedule] = useState<RepostingSchedule>({
    is_active: false,
    time_of_day: "09:00",
    days_of_week: [1, 2, 3, 4, 5], // Monday to Friday
    max_posts_per_day: 5,
    post_interval_hours: 4,
    include_marketplace: true
  })
  const [loading, setLoading] = useState(true)
  const [testMessage, setTestMessage] = useState("")
  const [automating, setAutomating] = useState(false)

  useEffect(() => {
    fetchStatus()
    setLoading(false)
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/facebook/status')
      if (response.ok) {
        const data = await response.json()
        setStatus(data)
        
        // Update schedule if available
        if (data.schedule) {
          setSchedule(data.schedule)
        }
      } else {
        console.error('Failed to fetch Facebook status:', response.statusText)
        setStatus(null) // Indicate service unavailable
      }
    } catch (error) {
      console.error('Error fetching Facebook status:', error)
      setStatus(null) // Indicate service unavailable
    }
  }

  const handleScheduleChange = (field: keyof RepostingSchedule, value: any) => {
    setSchedule(prev => ({ ...prev, [field]: value }))
  }

  const handleDayToggle = (day: number) => {
    setSchedule(prev => {
      const newDays = prev.days_of_week.includes(day)
        ? prev.days_of_week.filter(d => d !== day)
        : [...prev.days_of_week, day]
      return { ...prev, days_of_week: newDays.sort((a, b) => a - b) }
    })
  }

  const saveSchedule = async () => {
    try {
      const response = await fetch('http://localhost:8000/facebook/schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(schedule)
      })
      
      if (response.ok) {
        toast.success('Configuración guardada')
        await fetchStatus()
      } else {
        toast.error('Error al guardar la configuración')
      }
    } catch (error) {
      console.error('Error saving schedule:', error)
      toast.error('Error al guardar la configuración')
    }
  }

  const startAutomation = async () => {
    try {
      setAutomating(true)
      const response = await fetch('http://localhost:8000/facebook/start-automation', {
        method: 'POST'
      })
      
      if (response.ok) {
        toast.success('Automatización iniciada')
        await fetchStatus()
      } else {
        toast.error('Error al iniciar la automatización')
      }
    } catch (error) {
      console.error('Error starting automation:', error)
      toast.error('Error al iniciar la automatización')
    } finally {
      setAutomating(false)
    }
  }

  const stopAutomation = async () => {
    try {
      setAutomating(true)
      const response = await fetch('http://localhost:8000/facebook/stop-automation', {
        method: 'POST'
      })
      
      if (response.ok) {
        toast.success('Automatización detenida')
        await fetchStatus()
      } else {
        toast.error('Error al detener la automatización')
      }
    } catch (error) {
      console.error('Error stopping automation:', error)
      toast.error('Error al detener la automatización')
    } finally {
      setAutomating(false)
    }
  }

  const testPost = async () => {
    if (!testMessage.trim()) {
      toast.error('Ingresa un mensaje para la prueba')
      return
    }

    try {
      setAutomating(true)
      const response = await fetch('http://localhost:8000/facebook/test-post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: testMessage })
      })
      
      if (response.ok) {
        await response.json()
        toast.success('Post de prueba creado exitosamente')
        setTestMessage("")
        await fetchStatus()
      } else {
        toast.error('Error al crear el post de prueba')
      }
    } catch (error) {
      console.error('Error testing post:', error)
      toast.error('Error al crear el post de prueba')
    } finally {
      setAutomating(false)
    }
  }

  const getDayName = (day: number) => {
    const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    return days[day]
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
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
              <Facebook className="h-8 w-8 text-white" />
            </div>
            <h1 className="page-title">Facebook Reposting</h1>
            <p className="page-subtitle">
              Sistema automatizado de reposting diario para máxima visibilidad
            </p>
          </div>
        </div>

        {/* Service Status */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <BarChart3 className="h-6 w-6 mr-3" style={{color: 'var(--color-primary)'}} />
              Estado del Servicio
            </h3>
          </div>
          <div className="card-content">
            {status ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{status.total_posts}</div>
                  <div className="text-sm text-gray-600">Total de Posts</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{status.posts_last_week}</div>
                  <div className="text-sm text-gray-600">Posts Esta Semana</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">{status.active_vehicles}</div>
                  <div className="text-sm text-gray-600">Vehículos Activos</div>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">
                    {status.is_active ? 'Activo' : 'Inactivo'}
                  </div>
                  <div className="text-sm text-gray-600">Estado</div>
                </div>
              </div>
            ) : (
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="h-5 w-5 text-yellow-600" />
                  <span className="font-semibold text-yellow-800">
                    Servicio no disponible
                  </span>
                </div>
                <p className="text-yellow-700 mt-2">
                  No se pudo conectar con el servicio de Facebook.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Automation Control */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <Zap className="h-6 w-6 mr-3" style={{color: 'var(--color-primary)'}} />
              Control de Automatización
            </h3>
          </div>
          <div className="card-content">
            <div className="flex flex-wrap gap-4 mb-6">
              <button
                onClick={startAutomation}
                disabled={automating || status?.is_active}
                className="btn-primary flex items-center space-x-2"
              >
                <Play className="h-4 w-4" />
                <span>Iniciar Automatización</span>
              </button>
              
              <button
                onClick={stopAutomation}
                disabled={automating || !status?.is_active}
                className="btn-danger flex items-center space-x-2"
              >
                <StopCircle className="h-4 w-4" />
                <span>Detener Automatización</span>
              </button>
              
              <button
                onClick={fetchStatus}
                disabled={automating}
                className="btn-secondary flex items-center space-x-2"
              >
                <RefreshCw className={`h-4 w-4 ${automating ? 'animate-spin' : ''}`} />
                <span>Actualizar Estado</span>
              </button>
            </div>

            {status?.next_scheduled && (
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5 text-blue-600" />
                  <span className="font-semibold text-blue-800">
                    Próximo Post Programado: {new Date(status.next_scheduled).toLocaleString('es-MX')}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Schedule Configuration */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <Settings className="h-6 w-6 mr-3" style={{color: 'var(--color-primary)'}} />
              Configuración de Programación
            </h3>
          </div>
          <div className="card-content">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Hora del Día
                </label>
                <input
                  type="time"
                  value={schedule.time_of_day}
                  onChange={(e) => handleScheduleChange('time_of_day', e.target.value)}
                  className="input-field"
                />
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Máximo Posts por Día
                </label>
                <input
                  type="number"
                  value={schedule.max_posts_per_day}
                  onChange={(e) => handleScheduleChange('max_posts_per_day', Number(e.target.value))}
                  className="input-field"
                />
              </div>
            </div>
            
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Días de la Semana
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                {['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'].map((dayName, index) => (
                  <label key={index} className="flex items-center space-x-2 text-sm text-gray-700">
                    <input
                      type="checkbox"
                      checked={schedule.days_of_week.includes(index)}
                      onChange={() => handleDayToggle(index)}
                      className="form-checkbox"
                    />
                    <span>{dayName}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="flex items-center space-x-2 mb-6">
              <input
                type="checkbox"
                checked={schedule.include_marketplace}
                onChange={(e) => handleScheduleChange('include_marketplace', e.target.checked)}
                className="form-checkbox"
              />
              <label className="text-sm font-semibold text-gray-700">
                Incluir Facebook Marketplace
              </label>
            </div>

            <button onClick={saveSchedule} className="btn-primary">
              Guardar Configuración
            </button>
          </div>
        </div>

        {/* Test Post */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <CheckCircle className="h-6 w-6 mr-3 text-green-600" />
              Post de Prueba
            </h3>
          </div>
          <div className="card-content">
            <textarea
              placeholder="Escribe tu mensaje de prueba aquí..."
              value={testMessage}
              onChange={(e) => setTestMessage(e.target.value)}
              className="input-field mb-4"
            ></textarea>
            <button
              onClick={testPost}
              disabled={automating || !testMessage.trim()}
              className="btn-primary flex items-center space-x-2"
            >
              <CheckCircle className="h-4 w-4" />
              <span>Crear Post de Prueba</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FacebookReposting