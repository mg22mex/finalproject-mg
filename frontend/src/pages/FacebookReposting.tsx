import React, { useState, useEffect } from 'react'
import { Facebook, RefreshCw, Play, Settings, AlertCircle, Clock, Calendar, BarChart3, Zap, StopCircle, CheckCircle, XCircle } from 'lucide-react'
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
        if (data.config) {
          setSchedule(data.config)
        }
      }
    } catch (error) {
      console.error('Error fetching status:', error)
      toast.error('Error al cargar el estado del servicio')
    }
  }

  const handleScheduleChange = (field: keyof RepostingSchedule, value: any) => {
    setSchedule(prev => ({ ...prev, [field]: value }))
  }

  const saveSchedule = async () => {
    try {
      setAutomating(true)
      const response = await fetch('http://localhost:8000/facebook/schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(schedule)
      })
      
      if (response.ok) {
        toast.success('Programación guardada exitosamente')
        await fetchStatus()
      } else {
        toast.error('Error al guardar la programación')
      }
    } catch (error) {
      console.error('Error saving schedule:', error)
      toast.error('Error al guardar la programación')
    } finally {
      setAutomating(false)
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
        const result = await response.json()
        toast.success('Post de prueba creado exitosamente')
        setTestMessage("")
        await fetchStatus()
      } else {
        toast.error('Error al crear el post de prueba')
      }
    } catch (error) {
      console.error('Error creating test post:', error)
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
    <div className="space-y-8 bg-gray-50 min-h-screen">
      {/* Page Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white py-12 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center space-x-4 mb-4">
            <Facebook className="h-10 w-10" />
            <h1 className="text-4xl font-bold">Facebook Reposting</h1>
          </div>
          <p className="text-xl text-blue-100">
            Sistema automatizado de reposting diario para máxima visibilidad
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 space-y-8">
        {/* Service Status */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <BarChart3 className="h-6 w-6 mr-3 text-blue-600" />
            Estado del Servicio
          </h3>
          
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

        {/* Automation Control */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <Zap className="h-6 w-6 mr-3 text-blue-600" />
            Control de Automatización
          </h3>
          
          <div className="flex flex-wrap gap-4 mb-6">
            <button
              onClick={startAutomation}
              disabled={automating || status?.is_active}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center space-x-2"
            >
              <Play className="h-4 w-4" />
              <span>Iniciar Automatización</span>
            </button>
            
            <button
              onClick={stopAutomation}
              disabled={automating || !status?.is_active}
              className="px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center space-x-2"
            >
              <StopCircle className="h-4 w-4" />
              <span>Detener Automatización</span>
            </button>
            
            <button
              onClick={fetchStatus}
              disabled={automating}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center space-x-2"
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

        {/* Schedule Configuration */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <Settings className="h-6 w-6 mr-3 text-blue-600" />
            Configuración de Programación
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Hora del Día
              </label>
              <input
                type="time"
                value={schedule.time_of_day}
                onChange={(e) => handleScheduleChange('time_of_day', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Máximo Posts por Día
              </label>
              <input
                type="number"
                min="1"
                max="20"
                value={schedule.max_posts_per_day}
                onChange={(e) => handleScheduleChange('max_posts_per_day', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              />
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Días de la Semana
            </label>
            <div className="flex flex-wrap gap-2">
              {[0, 1, 2, 3, 4, 5, 6].map((day) => (
                <label key={day} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={schedule.days_of_week.includes(day)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        handleScheduleChange('days_of_week', [...schedule.days_of_week, day])
                      } else {
                        handleScheduleChange('days_of_week', schedule.days_of_week.filter(d => d !== day))
                      }
                    }}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700">{getDayName(day)}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="mb-6">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={schedule.include_marketplace}
                onChange={(e) => handleScheduleChange('include_marketplace', e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm font-semibold text-gray-700">
                Incluir Facebook Marketplace
              </span>
            </label>
          </div>

          <button
            onClick={saveSchedule}
            disabled={automating}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center space-x-2"
          >
            <Settings className="h-4 w-4" />
            <span>Guardar Configuración</span>
          </button>
        </div>

        {/* Test Post */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <Facebook className="h-6 w-6 mr-3 text-blue-600" />
            Post de Prueba
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Mensaje de Prueba
              </label>
              <textarea
                value={testMessage}
                onChange={(e) => setTestMessage(e.target.value)}
                placeholder="Escribe tu mensaje de prueba aquí..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 h-24"
              />
            </div>
            
            <button
              onClick={testPost}
              disabled={automating || !testMessage.trim()}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center space-x-2"
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
