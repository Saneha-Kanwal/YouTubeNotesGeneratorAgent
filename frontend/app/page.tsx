'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [youtubeUrl, setYoutubeUrl] = useState('');

  const [status, setStatus] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progressPercent, setProgressPercent] = useState(0);

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setStatus('Submitting video for processing...');
    setProgressPercent(5);

    try {
      const response = await fetch(`${API_BASE}/process-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ youtube_url: youtubeUrl }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to process video');
      }

      const data = await response.json();
      setStatus('Processing started. Checking status...');
      setProgressPercent(10);

      // Poll for status
      pollStatus(data.video_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setLoading(false);
      setStatus('');
      setProgressPercent(0);
    }
  };

  const pollStatus = async (id: string) => {
    const maxAttempts = 600; // 50 minutes max (5 second intervals)
    let attempts = 0;
    let progressTracker = 10; // Start at 10% after submission

    const checkStatus = async () => {
      try {
        const response = await fetch(`${API_BASE}/videos/${id}/status`);
        if (!response.ok) {
          throw new Error('Failed to fetch status');
        }

        const data = await response.json();
        const currentStatus = data.status || '';
        const progress = data.progress || '';
        
        // Update status with progress
        setStatus(progress || `Status: ${currentStatus}`);
        
        // Estimate progress based on status
        if (currentStatus === 'downloading') {
          progressTracker = Math.min(progressTracker + 0.5, 40); // 10-40% for download
        } else if (currentStatus === 'transcribing') {
          progressTracker = Math.min(progressTracker + 0.3, 80); // 40-80% for transcription
        } else if (currentStatus === 'generating_notes') {
          progressTracker = Math.min(progressTracker + 0.2, 95); // 80-95% for notes
        }
        
        setProgressPercent(Math.round(progressTracker));

        if (currentStatus === 'completed') {
          setLoading(false);
          setStatus('Processing completed!');
          setProgressPercent(100);
          // Small delay for visual feedback
          setTimeout(() => {
            window.location.href = `/notes/${id}`;
          }, 500);
        } else if (currentStatus === 'failed') {
          setLoading(false);
          setError(data.error || 'Processing failed');
          setStatus('');
          setProgressPercent(0);
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(checkStatus, 3000); // Poll every 3 seconds (faster updates)
        } else {
          setLoading(false);
          setError('Processing timeout. Please check back later.');
          setStatus('');
          setProgressPercent(0);
        }
      } catch (err) {
        setLoading(false);
        setError(err instanceof Error ? err.message : 'Failed to check status');
        setStatus('');
        setProgressPercent(0);
      }
    };

    checkStatus();
  };

  return (
    <div className="container mt-5 mb-5">
      <div className="row justify-content-center">
        <div className="col-lg-8 col-xl-7">
          {/* Hero Section - Enhanced */}
          <div className="text-center mb-5 animate-fade-in-up">
            <div className="mb-4 float-animation">
              <div className="d-inline-block p-4 rounded-circle" style={{
                background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)',
                border: '4px solid',
                borderImage: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) 1',
                boxShadow: '0 20px 60px rgba(99, 102, 241, 0.3), 0 0 40px rgba(139, 92, 246, 0.2)',
                animation: 'pulse 2s ease-in-out infinite'
              }}>
                <i className="bi bi-youtube gradient-text" style={{ fontSize: '4.5rem' }}></i>
              </div>
            </div>
            <h1 className="display-3 fw-bold mb-3 gradient-text" style={{
              fontSize: '4rem',
              letterSpacing: '-0.03em',
              lineHeight: '1.1',
              textShadow: '0 4px 20px rgba(99, 102, 241, 0.2)'
            }}>
              YouTube Notes AI Agent
            </h1>
            <p className="lead animate-fade-in" style={{ 
              color: '#6b7280', 
              fontSize: '1.4rem', 
              fontWeight: '500',
              maxWidth: '600px',
              margin: '0 auto'
            }}>
              Transform YouTube videos into structured, comprehensive study notes with AI-powered intelligence
            </p>
          </div>

          {/* Main Card - Premium Design */}
          <div className="card shadow-xl border-0 card-hover-effect animate-fade-in-up" style={{ 
            borderRadius: '2rem', 
            overflow: 'hidden',
            background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
            border: '2px solid rgba(99, 102, 241, 0.1)',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(99, 102, 241, 0.05)'
          }}>
            <div className="card-body p-4 p-md-5">
              <form onSubmit={handleSubmit}>
                <div className="mb-4">
                  <label htmlFor="youtubeUrl" className="form-label fw-bold mb-3" style={{ 
                    color: '#374151', 
                    fontSize: '1.15rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    <i className="bi bi-link-45deg" style={{ color: '#6366f1', fontSize: '1.3rem' }}></i>
                    YouTube Video URL
                  </label>
                  <div className="input-group input-group-lg">
                    <span className="input-group-text" style={{
                      background: 'linear-gradient(135deg, #f0f4ff 0%, #faf5ff 100%)',
                      border: '2px solid #e0e7ff',
                      borderRight: 'none',
                      borderRadius: '0.75rem 0 0 0.75rem'
                    }}>
                      <i className="bi bi-youtube" style={{ color: '#ef4444', fontSize: '1.8rem' }}></i>
                    </span>
                    <input
                      type="url"
                      className="form-control"
                      id="youtubeUrl"
                      value={youtubeUrl}
                      onChange={(e) => setYoutubeUrl(e.target.value)}
                      placeholder="https://www.youtube.com/watch?v=..."
                      required
                      disabled={loading}
                      style={{
                        border: '2px solid #e0e7ff',
                        borderLeft: 'none',
                        borderRadius: '0 0.75rem 0.75rem 0',
                        fontSize: '1.1rem',
                        padding: '1rem 1.25rem',
                        transition: 'all 0.3s ease'
                      }}
                    />
                  </div>
                </div>

                {/* Progress Bar - Enhanced */}
                {loading && (
                  <div className="mb-4" style={{ marginTop: '1rem' }}>
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <small className="text-muted fw-semibold">Processing...</small>
                      <small className="text-muted fw-bold">{progressPercent}%</small>
                    </div>
                    <div className="progress" style={{ 
                      height: '10px', 
                      borderRadius: '1rem',
                      backgroundColor: '#e5e7eb',
                      overflow: 'hidden',
                      boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.1)'
                    }}>
                      <div 
                        className="progress-bar progress-bar-striped progress-bar-animated" 
                        role="progressbar" 
                        style={{ 
                          width: `${progressPercent}%`,
                          background: 'linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
                          backgroundSize: '200% 100%',
                          animation: 'gradientShift 3s ease infinite',
                          transition: 'width 0.5s ease'
                        }}
                      ></div>
                    </div>
                  </div>
                )}

                {error && (
                  <div className="alert alert-danger d-flex align-items-center shadow-sm mb-4" role="alert" style={{
                    borderRadius: '1rem',
                    border: 'none',
                    padding: '1rem 1.25rem'
                  }}>
                    <i className="bi bi-exclamation-triangle-fill me-2 fs-5"></i>
                    <div className="fw-semibold">{error}</div>
                  </div>
                )}

                {status && (
                  <div className="alert alert-info d-flex align-items-center shadow-sm mb-4" role="alert" style={{
                    borderRadius: '1rem',
                    border: 'none',
                    padding: '1rem 1.25rem',
                    background: 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)'
                  }}>
                    {loading && (
                      <div className="spinner-border spinner-border-sm me-3" role="status" style={{
                        borderWidth: '2.5px',
                        width: '1.2rem',
                        height: '1.2rem'
                      }}>
                        <span className="visually-hidden">Loading...</span>
                      </div>
                    )}
                    <div className="fw-semibold">{status}</div>
                  </div>
                )}

                <button
                  type="submit"
                  className="btn btn-gradient btn-lg w-100 py-4 fw-bold shadow-lg ripple"
                  disabled={loading || !youtubeUrl}
                  style={{
                    fontSize: '1.2rem',
                    letterSpacing: '0.5px',
                    borderRadius: '1rem',
                    border: 'none',
                    position: 'relative',
                    overflow: 'hidden',
                    transform: loading ? 'scale(0.98)' : 'scale(1)',
                    transition: 'all 0.3s ease'
                  }}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" style={{
                        borderWidth: '2.5px',
                        width: '1.2rem',
                        height: '1.2rem'
                      }}></span>
                      Processing...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-magic me-2"></i>
                      ✨ Generate Notes
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Features - Enhanced Cards */}
          <div className="row mt-5 g-4">
            <div className="col-md-4">
              <div className="text-center p-5 rounded-4 feature-card" style={{
                background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)',
                border: '2px solid rgba(99, 102, 241, 0.15)',
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                cursor: 'pointer',
                height: '100%'
              }}>
                <div className="rounded-circle d-inline-flex align-items-center justify-content-center mb-4" style={{
                  width: '80px',
                  height: '80px',
                  background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                  boxShadow: '0 8px 25px rgba(99, 102, 241, 0.4)',
                  transition: 'all 0.3s ease'
                }}>
                  <i className="bi bi-file-text text-white fs-2"></i>
                </div>
                <h5 className="fw-bold mb-3" style={{ color: '#1f2937', fontSize: '1.3rem' }}>Structured Notes</h5>
                <p style={{ color: '#6b7280', fontSize: '1rem', lineHeight: '1.6' }}>
                  Organized with headings, bullet points, and key insights
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="text-center p-5 rounded-4 feature-card" style={{
                background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.08) 100%)',
                border: '2px solid rgba(16, 185, 129, 0.15)',
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                cursor: 'pointer',
                height: '100%'
              }}>
                <div className="rounded-circle d-inline-flex align-items-center justify-content-center mb-4" style={{
                  width: '80px',
                  height: '80px',
                  background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
                  boxShadow: '0 8px 25px rgba(16, 185, 129, 0.4)',
                  transition: 'all 0.3s ease'
                }}>
                  <i className="bi bi-translate text-white fs-2"></i>
                </div>
                <h5 className="fw-bold mb-3" style={{ color: '#1f2937', fontSize: '1.3rem' }}>50+ Languages</h5>
                <p style={{ color: '#6b7280', fontSize: '1rem', lineHeight: '1.6' }}>
                  Translate notes into any language instantly
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="text-center p-5 rounded-4 feature-card" style={{
                background: 'linear-gradient(135deg, rgba(236, 72, 153, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)',
                border: '2px solid rgba(236, 72, 153, 0.15)',
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                cursor: 'pointer',
                height: '100%'
              }}>
                <div className="rounded-circle d-inline-flex align-items-center justify-content-center mb-4" style={{
                  width: '80px',
                  height: '80px',
                  background: 'linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)',
                  boxShadow: '0 8px 25px rgba(236, 72, 153, 0.4)',
                  transition: 'all 0.3s ease'
                }}>
                  <i className="bi bi-clock-history text-white fs-2"></i>
                </div>
                <h5 className="fw-bold mb-3" style={{ color: '#1f2937', fontSize: '1.3rem' }}>Full History</h5>
                <p style={{ color: '#6b7280', fontSize: '1rem', lineHeight: '1.6' }}>
                  Access all your processed videos anytime
                </p>
              </div>
            </div>
          </div>

          <div className="mt-5 text-center">
            <Link href="/history" className="btn btn-outline-primary btn-lg px-5 py-3" style={{
              borderWidth: '2px',
              fontWeight: '600',
              borderRadius: '1rem',
              fontSize: '1.1rem'
            }}>
              <i className="bi bi-clock-history me-2"></i>
              View Processing History
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
