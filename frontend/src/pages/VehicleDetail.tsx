import React from 'react'
import { useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

const VehicleDetail: React.FC = () => {
  const { id } = useParams()

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link to="/vehicles" className="btn-secondary">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Vehicles
        </Link>
      </div>
      
      <div className="card">
        <h1 className="page-title">Vehicle Details</h1>
        <p className="page-subtitle">Vehicle ID: {id}</p>
        <p>This page will show detailed vehicle information, photos, and management options.</p>
      </div>
    </div>
  )
}

export default VehicleDetail
