import React, { useState } from 'react'
import { FolderPlus, ExternalLink, RefreshCw, Upload, CheckCircle, AlertCircle } from 'lucide-react'
import { toast } from 'react-hot-toast'

interface DriveFolderManagerProps {
  vehicleId: number
  vehicleInfo: {
    marca?: string
    modelo?: string
    año?: string
  }
  onFolderCreated?: (folderInfo: any) => void
}

interface DriveFolderInfo {
  folder_id: string
  folder_name: string
  folder_url: string
  files: any[]
  file_count: number
}

const DriveFolderManager: React.FC<DriveFolderManagerProps> = ({
  vehicleId,
  vehicleInfo,
  onFolderCreated
}) => {
  const [loading, setLoading] = useState(false)
  const [syncing, setSyncing] = useState(false)
  const [folderInfo, setFolderInfo] = useState<DriveFolderInfo | null>(null)
  const [checking, setChecking] = useState(false)

  const createDriveFolder = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/drive/create-folder/${vehicleId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('Failed to create Drive folder')
      }

      const data = await response.json()
      setFolderInfo({
        folder_id: data.folder_id,
        folder_name: data.folder_name,
        folder_url: data.folder_url,
        files: [],
        file_count: 0
      })
      
      toast.success('Drive folder created successfully!')
      onFolderCreated?.(data)
      
    } catch (error) {
      console.error('Error creating Drive folder:', error)
      toast.error('Failed to create Drive folder')
    } finally {
      setLoading(false)
    }
  }

  const checkFolderInfo = async () => {
    try {
      setChecking(true)
      const response = await fetch(`http://localhost:8000/drive/vehicle/${vehicleId}/folder-info`)
      
      if (response.ok) {
        const data = await response.json()
        if (data.has_folder) {
          setFolderInfo({
            folder_id: data.folder_id,
            folder_name: data.folder_id, // Use folder_id as name for now
            folder_url: data.folder_url,
            files: data.files || [],
            file_count: data.file_count || 0
          })
        }
      }
    } catch (error) {
      console.error('Error checking folder info:', error)
    } finally {
      setChecking(false)
    }
  }

  const syncPhotos = async () => {
    try {
      setSyncing(true)
      const response = await fetch(`http://localhost:8000/drive/sync-photos/${vehicleId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('Failed to sync photos')
      }

      const data = await response.json()
      toast.success(`Synced ${data.synced_photos} photos successfully!`)
      
      // Refresh folder info
      await checkFolderInfo()
      
    } catch (error) {
      console.error('Error syncing photos:', error)
      toast.error('Failed to sync photos')
    } finally {
      setSyncing(false)
    }
  }

  const testConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/drive/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          toast.success('Google Drive connection successful!')
        } else {
          toast.error('Google Drive connection failed')
        }
      } else {
        toast.error('Google Drive connection failed')
      }
    } catch (error) {
      console.error('Error testing connection:', error)
      toast.error('Failed to test Drive connection')
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title flex items-center">
          <FolderPlus className="h-6 w-6 mr-3 text-blue-600" />
          Google Drive Integration
        </h3>
      </div>
      <div className="card-content">
        <div className="space-y-4">
          {/* Connection Test */}
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h4 className="font-semibold text-gray-800">Drive Connection</h4>
              <p className="text-sm text-gray-600">Test Google Drive API connection</p>
            </div>
            <button
              onClick={testConnection}
              className="btn-secondary flex items-center space-x-2"
            >
              <CheckCircle className="h-4 w-4" />
              <span>Test Connection</span>
            </button>
          </div>

          {/* Folder Creation */}
          {!folderInfo && (
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <div>
                <h4 className="font-semibold text-blue-800">Create Drive Folder</h4>
                <p className="text-sm text-blue-600">
                  Create a Google Drive folder for this vehicle's photos
                </p>
              </div>
              <button
                onClick={createDriveFolder}
                disabled={loading}
                className="btn-primary flex items-center space-x-2"
              >
                {loading ? (
                  <RefreshCw className="h-4 w-4 animate-spin" />
                ) : (
                  <FolderPlus className="h-4 w-4" />
                )}
                <span>{loading ? 'Creating...' : 'Create Folder'}</span>
              </button>
            </div>
          )}

          {/* Folder Info */}
          {folderInfo && (
            <div className="space-y-4">
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <h4 className="font-semibold text-green-800">Drive Folder Created</h4>
                </div>
                <p className="text-sm text-green-700 mb-3">
                  Folder: {folderInfo.folder_name}
                </p>
                <div className="flex items-center space-x-2">
                  <a
                    href={folderInfo.folder_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <ExternalLink className="h-4 w-4" />
                    <span>Open Folder</span>
                  </a>
                  <button
                    onClick={checkFolderInfo}
                    disabled={checking}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    {checking ? (
                      <RefreshCw className="h-4 w-4 animate-spin" />
                    ) : (
                      <RefreshCw className="h-4 w-4" />
                    )}
                    <span>Refresh</span>
                  </button>
                </div>
              </div>

              {/* File Count */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-semibold text-gray-800">Photos in Folder</h4>
                  <p className="text-sm text-gray-600">
                    {folderInfo.file_count} photos found
                  </p>
                </div>
                <button
                  onClick={syncPhotos}
                  disabled={syncing}
                  className="btn-primary flex items-center space-x-2"
                >
                  {syncing ? (
                    <RefreshCw className="h-4 w-4 animate-spin" />
                  ) : (
                    <Upload className="h-4 w-4" />
                  )}
                  <span>{syncing ? 'Syncing...' : 'Sync Photos'}</span>
                </button>
              </div>

              {/* Instructions */}
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-800 mb-2">How to Use</h4>
                <ol className="text-sm text-blue-700 space-y-1">
                  <li>1. Click "Open Folder" to access the Drive folder</li>
                  <li>2. Upload your vehicle photos to the folder</li>
                  <li>3. Click "Sync Photos" to import them to the system</li>
                  <li>4. Photos will appear in the vehicle's photo gallery</li>
                </ol>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DriveFolderManager
