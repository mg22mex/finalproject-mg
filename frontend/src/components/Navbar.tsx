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
    <nav style={{
      backgroundColor: 'var(--color-bg-card)',
      borderBottom: '1px solid var(--color-border-light)',
      padding: 'var(--space-4) 0',
      boxShadow: 'var(--shadow-sm)'
    }}>
      <div className="page-container">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 'var(--space-6)'
        }}>
          {/* Logo - Matching Autosell.mx exactly */}
          <div style={{display: 'flex', alignItems: 'center'}}>
            <Link to="/" style={{display: 'flex', alignItems: 'center', gap: 'var(--space-3)', textDecoration: 'none'}}>
              {/* Three vertical bars: black, blue, red - exact match */}
              <div style={{display: 'flex', gap: 'var(--space-1)'}}>
                <div style={{width: '0.25rem', height: '1.5rem', backgroundColor: 'var(--color-text)', transform: 'skewX(-12deg)'}}></div>
                <div style={{width: '0.25rem', height: '2rem', backgroundColor: '#2563eb', transform: 'skewX(-12deg)'}}></div>
                <div style={{width: '0.25rem', height: '2.5rem', backgroundColor: 'var(--color-danger)', transform: 'skewX(-12deg)'}}></div>
              </div>
              <div style={{display: 'flex', alignItems: 'baseline', gap: 'var(--space-1)'}}>
                <span style={{fontSize: 'var(--text-xl)', fontWeight: '700', color: 'var(--color-text)'}}>Autosell</span>
                <span style={{fontSize: 'var(--text-xs)', color: 'var(--color-text)'}}>®</span>
                <div style={{display: 'flex', alignItems: 'center'}}>
                  <div style={{width: '0.5rem', height: '0.5rem', backgroundColor: 'var(--color-danger)', borderRadius: '50%', marginRight: 'var(--space-1)'}}></div>
                  <span style={{fontSize: 'var(--text-lg)', color: 'var(--color-text)'}}>mx</span>
                </div>
              </div>
            </Link>
          </div>

          {/* Navigation Links - Horizontal Layout */}
          <div style={{display: 'flex', gap: 'var(--space-8)'}}>
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-2)',
                  padding: 'var(--space-3)',
                  fontSize: 'var(--text-sm)',
                  fontWeight: '600',
                  textDecoration: 'none',
                  color: isActive(item.path) ? 'var(--color-primary)' : 'var(--color-text-muted)',
                  transition: 'color 0.2s',
                  borderRadius: 'var(--radius-md)',
                  backgroundColor: isActive(item.path) ? 'var(--color-primary-light)' : 'transparent'
                }}
              >
                <span>{item.label}</span>
                <ChevronRight style={{width: '0.75rem', height: '0.75rem'}} />
              </Link>
            ))}
          </div>

          {/* Action Buttons */}
          <div style={{display: 'flex', alignItems: 'center', gap: 'var(--space-4)'}}>
            <Link
              to="/vehicles/new"
              className="btn-primary"
              style={{display: 'flex', alignItems: 'center', gap: 'var(--space-2)'}}
            >
              <Plus style={{width: '1rem', height: '1rem'}} />
              <span>Agregar Vehículo</span>
            </Link>
          </div>

          {/* Mobile Menu Button - Hidden for now since we want horizontal layout */}
          <div style={{display: 'none'}}>
            <button style={{color: '#6b7280', padding: '0.5rem'}}>
              <svg style={{width: '1.5rem', height: '1.5rem'}} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation - Hidden since we're using horizontal layout */}
        <div style={{display: 'none'}}>
          <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '0.75rem',
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  textDecoration: 'none',
                  color: isActive(item.path) ? '#2563eb' : '#374151',
                  transition: 'color 0.2s'
                }}
              >
                <span>{item.label}</span>
                <ChevronRight style={{width: '1rem', height: '1rem'}} />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
