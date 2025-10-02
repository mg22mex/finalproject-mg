import React, { useState } from 'react'
import { Settings as SettingsIcon, Database, Key, Globe, Shield, Save } from 'lucide-react'

const Settings: React.FC = () => {
  const [settings, setSettings] = useState({
    apiUrl: 'http://localhost:8000',
    databaseUrl: 'postgresql://postgres:password@localhost:5434/autosell_db',
    googleDriveEnabled: true,
    facebookIntegration: true,
    n8nWebhookUrl: 'http://localhost:5678',
    maxFileSize: '10MB',
    allowedFileTypes: 'jpg,jpeg,png,gif',
    autoSync: true,
    backupEnabled: true
  })

  const handleSave = () => {
    // TODO: Implement actual save functionality
    console.log('Saving settings:', settings)
    alert('Configuración guardada exitosamente')
  }

  return (
    <div className="page-container">
      <div className="space-y-6">
        <div className="page-header">
          <h1 className="page-title">Configuración</h1>
          <p className="page-subtitle">
            Configura los ajustes del sistema e integraciones
          </p>
        </div>
        
        {/* API Configuration */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <Key className="h-6 w-6 mr-3" style={{color: 'var(--color-primary)'}} />
              Configuración de API
            </h3>
          </div>
          <div className="card-content">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  URL de API
                </label>
                <input
                  type="text"
                  value={settings.apiUrl}
                  onChange={(e) => setSettings({...settings, apiUrl: e.target.value})}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  URL de Base de Datos
                </label>
                <input
                  type="text"
                  value={settings.databaseUrl}
                  onChange={(e) => setSettings({...settings, databaseUrl: e.target.value})}
                  className="input-field"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Integrations */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <Globe className="h-6 w-6 mr-3" style={{color: 'var(--color-primary)'}} />
              Integraciones
            </h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-gray-900">Google Drive</h4>
                  <p className="text-sm text-gray-600">Sincronización automática de fotos</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.googleDriveEnabled}
                    onChange={(e) => setSettings({...settings, googleDriveEnabled: e.target.checked})}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-gray-900">Facebook</h4>
                  <p className="text-sm text-gray-600">Publicación automática en Facebook</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.facebookIntegration}
                    onChange={(e) => setSettings({...settings, facebookIntegration: e.target.checked})}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* File Settings */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title flex items-center">
              <Shield className="h-6 w-6 mr-3" style={{color: 'var(--color-primary)'}} />
              Configuración de Archivos
            </h3>
          </div>
          <div className="card-content">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Tamaño Máximo de Archivo
                </label>
                <select
                  value={settings.maxFileSize}
                  onChange={(e) => setSettings({...settings, maxFileSize: e.target.value})}
                  className="input-field"
                >
                  <option value="5MB">5MB</option>
                  <option value="10MB">10MB</option>
                  <option value="25MB">25MB</option>
                  <option value="50MB">50MB</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Tipos de Archivo Permitidos
                </label>
                <input
                  type="text"
                  value={settings.allowedFileTypes}
                  onChange={(e) => setSettings({...settings, allowedFileTypes: e.target.value})}
                  className="input-field"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            onClick={handleSave}
            className="btn-primary flex items-center space-x-2"
          >
            <Save className="h-4 w-4" />
            <span>Guardar Configuración</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default Settings
