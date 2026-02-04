'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import LanguageDropdown from '@/components/LanguageDropdown';
import NotesViewer from '@/components/NotesViewer';

interface Video {
  id: string;
  youtube_url: string;
  title: string | null;
  transcript: string | null;
  original_notes: string | null;
  duration_seconds: number | null;
  thumbnail_url: string | null;
  created_at: string;
}

export default function NotesPage() {
  const params = useParams();
  const videoId = params.id as string;
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

  const [video, setVideo] = useState<Video | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTranscript, setShowTranscript] = useState(false);
  const [displayNotes, setDisplayNotes] = useState<string | null>(null);
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const fetchVideo = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/videos/${videoId}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Video not found');
        }
        throw new Error('Failed to fetch video');
      }
      const data = await response.json();
      setVideo(data);
      setDisplayNotes(data.original_notes);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [API_BASE, videoId]);

  useEffect(() => {
    fetchVideo();
  }, [fetchVideo]);

  const handleTranslationChange = (translatedNotes: string, language: string) => {
    setDisplayNotes(translatedNotes);
    setCurrentLanguage(language);
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
        <Link href="/" className="btn btn-primary">
          Back to Home
        </Link>
      </div>
    );
  }

  if (!video) {
    return null;
  }

  const formatDuration = (seconds: number | null) => {
    if (!seconds) return 'Unknown';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="container mt-4 mb-5">
      <div className="row">
        <div className="col-md-12">
          <nav aria-label="breadcrumb" className="mb-4">
            <ol className="breadcrumb">
              <li className="breadcrumb-item">
                <Link href="/" className="text-decoration-none">
                  <i className="bi bi-house-door me-1"></i>Home
                </Link>
              </li>
              <li className="breadcrumb-item">
                <Link href="/history" className="text-decoration-none">History</Link>
              </li>
              <li className="breadcrumb-item active" aria-current="page">
                Notes
              </li>
            </ol>
          </nav>

          {/* Video Metadata */}
          <div className="card mb-4 shadow-lg border-0" style={{ borderRadius: '1.25rem', overflow: 'hidden' }}>
            <div className="card-body p-4 p-md-5">
              <div className="row align-items-center">
                {video.thumbnail_url && (
                  <div className="col-md-3 mb-3 mb-md-0">
                    <div className="position-relative" style={{ borderRadius: '1rem', overflow: 'hidden', boxShadow: '0 10px 25px rgba(0,0,0,0.15)' }}>
                      <img
                        src={video.thumbnail_url}
                        alt={video.title || 'Video thumbnail'}
                        className="img-fluid"
                        style={{ maxHeight: '200px', objectFit: 'cover', width: '100%', display: 'block' }}
                      />
                      <div className="position-absolute top-50 start-50 translate-middle">
                        <div className="rounded-circle bg-white bg-opacity-90 d-flex align-items-center justify-content-center" style={{ width: '60px', height: '60px' }}>
                          <i className="bi bi-play-fill text-primary" style={{ fontSize: '1.5rem', marginLeft: '3px' }}></i>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div className={video.thumbnail_url ? 'col-md-9' : 'col-md-12'}>
                  <h2 className="card-title mb-4" style={{
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    fontSize: '2rem',
                    fontWeight: '700'
                  }}>
                    <i className="bi bi-play-circle me-2"></i>
                    {video.title || 'Untitled Video'}
                  </h2>
                  <div className="row g-3">
                    <div className="col-md-6">
                      <div className="d-flex align-items-center p-3 rounded-3" style={{ background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%)' }}>
                        <div className="rounded-circle d-flex align-items-center justify-content-center me-3" style={{
                          width: '40px',
                          height: '40px',
                          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
                        }}>
                          <i className="bi bi-clock text-white"></i>
                        </div>
                        <div>
                          <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Duration</div>
                          <div style={{ color: '#1f2937', fontWeight: '600' }}>{formatDuration(video.duration_seconds)}</div>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className="d-flex align-items-center p-3 rounded-3" style={{ background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(6, 182, 212, 0.05) 100%)' }}>
                        <div className="rounded-circle d-flex align-items-center justify-content-center me-3" style={{
                          width: '40px',
                          height: '40px',
                          background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)'
                        }}>
                          <i className="bi bi-calendar text-white"></i>
                        </div>
                        <div>
                          <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Processed</div>
                          <div style={{ color: '#1f2937', fontWeight: '600' }}>{new Date(video.created_at).toLocaleString()}</div>
                        </div>
                      </div>
                    </div>
                    <div className="col-12">
                      <div className="d-flex align-items-center p-3 rounded-3" style={{ background: 'linear-gradient(135deg, rgba(236, 72, 153, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%)' }}>
                        <div className="rounded-circle d-flex align-items-center justify-content-center me-3" style={{
                          width: '40px',
                          height: '40px',
                          background: 'linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)'
                        }}>
                          <i className="bi bi-link-45deg text-white"></i>
                        </div>
                        <div className="flex-grow-1">
                          <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Video URL</div>
                          <a 
                            href={video.youtube_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-decoration-none fw-semibold"
                            style={{ color: '#6366f1' }}
                          >
                            {video.youtube_url}
                            <i className="bi bi-box-arrow-up-right ms-1"></i>
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Notes */}
          {video.original_notes ? (
            <div className="card mb-4 shadow-lg border-0" style={{ borderRadius: '1.25rem', overflow: 'hidden' }}>
              <div className="card-header d-flex justify-content-between align-items-center" style={{
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
                color: 'white',
                border: 'none',
                padding: '1.5rem 2rem'
              }}>
                <h3 className="mb-0 fw-bold" style={{ fontSize: '1.5rem' }}>
                  <i className="bi bi-file-text me-2"></i>Generated Notes
                </h3>
                <div className="d-flex gap-2">
                  <button
                    className="btn btn-sm"
                    onClick={() => window.print()}
                    title="Print or Save as PDF"
                    style={{
                      background: 'rgba(255, 255, 255, 0.2)',
                      border: '1px solid rgba(255, 255, 255, 0.3)',
                      color: 'white',
                      fontWeight: '600'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                    }}
                  >
                    <i className="bi bi-printer me-1"></i> Print/Export
                  </button>
                </div>
              </div>
              <div className="card-body p-4 p-md-5">
                <LanguageDropdown
                  videoId={videoId}
                  onTranslationChange={handleTranslationChange}
                  currentLanguage={currentLanguage}
                />
                {displayNotes ? (
                  <NotesViewer notes={displayNotes} />
                ) : (
                  <div className="text-center py-5">
                    <div className="spinner-border" role="status" style={{ color: '#6366f1', width: '3rem', height: '3rem' }}>
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="alert shadow-lg border-0" role="alert" style={{
              background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(251, 191, 36, 0.1) 100%)',
              border: '2px solid rgba(245, 158, 11, 0.3)',
              borderRadius: '1rem',
              color: '#92400e',
              fontWeight: '600'
            }}>
              <i className="bi bi-hourglass-split me-2"></i>
              Notes are not available yet. Processing may still be in progress.
            </div>
          )}

          {/* Transcript */}
          {video.transcript && (
            <div className="card shadow-lg border-0" style={{ borderRadius: '1.25rem', overflow: 'hidden' }}>
              <div className="card-header" style={{
                background: 'linear-gradient(135deg, #6b7280 0%, #4b5563 100%)',
                color: 'white',
                border: 'none',
                padding: '1.5rem 2rem'
              }}>
                <button
                  className="btn btn-link text-white text-decoration-none p-0 w-100 text-start"
                  type="button"
                  onClick={() => setShowTranscript(!showTranscript)}
                  aria-expanded={showTranscript}
                  style={{ fontWeight: '600' }}
                >
                  <h3 className="mb-0" style={{ fontSize: '1.5rem' }}>
                    <i className="bi bi-file-earmark-text me-2"></i>
                    Full Transcript{' '}
                    <span className="badge ms-2" style={{
                      background: 'rgba(255, 255, 255, 0.2)',
                      color: 'white',
                      fontWeight: '600',
                      padding: '0.375rem 0.75rem'
                    }}>
                      {showTranscript ? 'Hide' : 'Show'}
                    </span>
                  </h3>
                </button>
              </div>
              {showTranscript && (
                <div className="card-body p-4 p-md-5">
                  <div className="transcript-content" style={{ whiteSpace: 'pre-wrap' }}>
                    {video.transcript}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

