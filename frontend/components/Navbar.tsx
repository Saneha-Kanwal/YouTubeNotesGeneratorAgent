'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="navbar navbar-expand-lg" style={{
      background: 'rgba(15, 12, 41, 0.85)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(139, 92, 246, 0.3)',
      padding: '1rem 2rem',
      boxShadow: '0 4px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(139, 92, 246, 0.2)',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
      transition: 'all 0.3s ease',
      animation: 'fadeInDown 0.5s ease-out'
    }}>
      <div className="container-fluid">
        <Link href="/" className="navbar-brand d-flex align-items-center" style={{
          fontSize: '1.5rem',
          fontWeight: '800',
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          textDecoration: 'none',
          letterSpacing: '-0.02em'
        }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginRight: '0.75rem',
            boxShadow: '0 0 30px rgba(139, 92, 246, 0.6), inset 0 0 20px rgba(99, 102, 241, 0.3)',
            position: 'relative',
            animation: 'rotate360 8s linear infinite, pulse 2s ease-in-out infinite',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'scale(1.1)';
            e.currentTarget.style.boxShadow = '0 0 40px rgba(139, 92, 246, 0.8), inset 0 0 30px rgba(99, 102, 241, 0.5)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = '0 0 30px rgba(139, 92, 246, 0.6), inset 0 0 20px rgba(99, 102, 241, 0.3)';
          }}
          >
            {/* Outer rotating ring */}
            <div style={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              borderRadius: '50%',
              border: '2px solid transparent',
              borderTopColor: 'rgba(255, 255, 255, 0.6)',
              borderRightColor: 'rgba(255, 255, 255, 0.3)',
              animation: 'rotate360 3s linear infinite',
              top: '0',
              left: '0'
            }}></div>
            {/* Inner rotating ring */}
            <div style={{
              position: 'absolute',
              width: '80%',
              height: '80%',
              borderRadius: '50%',
              border: '2px solid transparent',
              borderBottomColor: 'rgba(255, 255, 255, 0.5)',
              borderLeftColor: 'rgba(255, 255, 255, 0.2)',
              animation: 'rotate360 2s linear infinite reverse',
              top: '10%',
              left: '10%'
            }}></div>
            {/* AI Brain/Robot Icon */}
            <i className="bi bi-cpu-fill" style={{ 
              fontSize: '1.75rem', 
              color: '#ffffff',
              zIndex: 1,
              position: 'relative',
              animation: 'bounce 3s ease-in-out infinite',
              filter: 'drop-shadow(0 0 8px rgba(255, 255, 255, 0.5))'
            }}></i>
          </div>
          YouTube Notes AI
        </Link>
        
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
          style={{
            border: '1px solid rgba(139, 92, 246, 0.3)',
            borderRadius: '0.5rem',
            padding: '0.5rem',
            background: 'rgba(26, 21, 56, 0.6)'
          }}
        >
          <span className="navbar-toggler-icon" style={{
            backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(255, 255, 255, 0.85)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e")`
          }}></span>
        </button>
        
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto" style={{ gap: '1rem' }}>
            <li className="nav-item">
              <Link
                href="/"
                className={`nav-link ${pathname === '/' ? 'active' : ''}`}
                style={{
                  color: pathname === '/' ? '#8b5cf6' : 'rgba(255, 255, 255, 0.8)',
                  fontWeight: pathname === '/' ? '700' : '500',
                  fontSize: '1rem',
                  padding: '0.5rem 1rem',
                  borderRadius: '0.5rem',
                  transition: 'all 0.3s ease',
                  position: 'relative'
                }}
                onMouseEnter={(e) => {
                  if (pathname !== '/') {
                    e.currentTarget.style.color = '#ffffff';
                    e.currentTarget.style.background = 'rgba(139, 92, 246, 0.15)';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(139, 92, 246, 0.3)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (pathname !== '/') {
                    e.currentTarget.style.color = 'rgba(255, 255, 255, 0.8)';
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                  }
                }}
              >
                <i className="bi bi-house-door me-2"></i>Home
                {pathname === '/' && (
                  <span style={{
                    position: 'absolute',
                    bottom: '0',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    width: '60%',
                    height: '2px',
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
                    borderRadius: '2px',
                    boxShadow: '0 0 10px rgba(139, 92, 246, 0.8)'
                  }}></span>
                )}
              </Link>
            </li>
            <li className="nav-item">
              <Link
                href="/history"
                className={`nav-link ${pathname === '/history' ? 'active' : ''}`}
                style={{
                  color: pathname === '/history' ? '#8b5cf6' : 'rgba(255, 255, 255, 0.8)',
                  fontWeight: pathname === '/history' ? '700' : '500',
                  fontSize: '1rem',
                  padding: '0.5rem 1rem',
                  borderRadius: '0.5rem',
                  transition: 'all 0.3s ease',
                  position: 'relative'
                }}
                onMouseEnter={(e) => {
                  if (pathname !== '/history') {
                    e.currentTarget.style.color = '#ffffff';
                    e.currentTarget.style.background = 'rgba(139, 92, 246, 0.15)';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(139, 92, 246, 0.3)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (pathname !== '/history') {
                    e.currentTarget.style.color = 'rgba(255, 255, 255, 0.8)';
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                  }
                }}
              >
                <i className="bi bi-clock-history me-2"></i>History
                {pathname === '/history' && (
                  <span style={{
                    position: 'absolute',
                    bottom: '0',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    width: '60%',
                    height: '2px',
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
                    borderRadius: '2px',
                    boxShadow: '0 0 10px rgba(139, 92, 246, 0.8)'
                  }}></span>
                )}
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

