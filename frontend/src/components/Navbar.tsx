import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Car, Camera, Settings, BarChart3, Plus, ChevronRight, Facebook } from 'lucide-react'

const Navbar: React.FC = () => {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3 },
    { path: '/vehicles', label: 'Vehículos', icon: Car },
    { path: '/photos', label: 'Fotos', icon: Camera },
    { path: '/facebook', label: 'Facebook', icon: Facebook },
    { path: '/settings', label: 'Configuración', icon: Settings },
  ]

  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo - Matching Autosell.mx exactly */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3">
              {/* Three vertical bars: black, blue, red - exact match */}
              <div className="flex space-x-1">
                <div className="w-1 h-6 bg-black transform -skew-x-12"></div>
                <div className="w-1 h-8 bg-blue-600 transform -skew-x-12"></div>
                <div className="w-1 h-10 bg-red-600 transform -skew-x-12"></div>
              </div>
              <div className="flex items-baseline space-x-1">
                <span className="text-2xl font-bold text-black">Autosell</span>
                <span className="text-xs text-black">®</span>
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-red-600 rounded-full mr-1"></div>
                  <span className="text-lg text-black">mx</span>
                </div>
              </div>
            </Link>
          </div>

                    {/* Navigation Links - Matching Autosell.mx style */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-2 px-3 py-2 text-sm font-semibold transition-colors duration-200 ${
                  isActive(item.path)
                    ? 'text-blue-600'
                    : 'text-gray-700 hover:text-blue-600'
                }`}
              >
                <span>{item.label}</span>
                <ChevronRight className="h-3 w-3" />
              </Link>
            ))}
          </div>

          {/* Action Buttons - Matching Autosell.mx red button */}
          <div className="flex items-center space-x-4">
            <Link
              to="/vehicles/new"
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors duration-200 flex items-center space-x-2"
            >
              <Plus className="h-4 w-4" />
              <span className="hidden sm:inline">Agregar Vehículo</span>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button className="text-gray-600 hover:text-gray-900 p-2">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation - Matching Autosell.mx style */}
        <div className="md:hidden border-t border-gray-200 py-4">
          <div className="flex flex-col space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center justify-between px-3 py-2 text-sm font-semibold transition-colors duration-200 ${
                  isActive(item.path)
                    ? 'text-blue-600'
                    : 'text-gray-700 hover:text-blue-600'
                }`}
              >
                <span>{item.label}</span>
                <ChevronRight className="h-4 w-4" />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
