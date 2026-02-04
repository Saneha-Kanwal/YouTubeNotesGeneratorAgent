'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface VideoSummary {
  id: string;
  youtube_url: string;
  title: string | null;
  thumbnail_url: string | null;
  duration_seconds: number | null;
  created_at: string;
}

interface VideoListResponse {
  videos: VideoSummary[];
  total: number;
  page: number;
  limit: number;
}

export default function HistoryPage() {
  const router = useRouter();
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

  const [videos, setVideos] = useState<VideoSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [limit] = useState(20);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchVideos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/videos?page=${page}&limit=${limit}`);
      if (!response.ok) {
        throw new Error('Failed to fetch videos');
      }
      const data: VideoListResponse = await response.json();
      setVideos(data.videos);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [API_BASE, page, limit]);

  useEffect(() => {
    fetchVideos();
  }, [fetchVideos]);

  const handleDelete = async (videoId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this video and all its translations?')) {
      return;
    }

    setDeletingId(videoId);
    try {
      const response = await fetch(`${API_BASE}/videos/${videoId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete video');
      }

      // Refresh the list
      fetchVideos();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete video');
    } finally {
      setDeletingId(null);
    }
  };

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

  const totalPages = Math.ceil(total / limit);

  if (loading && videos.length === 0) {
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

  return (
    <div className="container mt-4 mb-5">
      <nav aria-label="breadcrumb" className="mb-4">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link href="/" className="text-decoration-none">
              <i className="bi bi-house-door me-1"></i>Home
            </Link>
          </li>
          <li className="breadcrumb-item active" aria-current="page">
            History
          </li>
        </ol>
      </nav>

      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="mb-0">
          <i className="bi bi-clock-history me-2 text-primary"></i>
          Processing History
        </h1>
        <Link href="/" className="btn btn-primary">
          <i className="bi bi-plus-circle me-2"></i>New Video
        </Link>
      </div>

      {error && (
        <div className="alert alert-danger d-flex align-items-center shadow-sm" role="alert">
          <i className="bi bi-exclamation-triangle-fill me-2 fs-5"></i>
          <div>{error}</div>
        </div>
      )}

      {videos.length === 0 ? (
        <div className="card shadow-sm border-0 text-center py-5">
          <div className="card-body">
            <i className="bi bi-inbox display-1 text-muted mb-3"></i>
            <h3 className="text-muted">No videos processed yet</h3>
            <p className="text-muted mb-4">Start by processing your first YouTube video</p>
            <Link href="/" className="btn btn-primary btn-lg">
              <i className="bi bi-play-circle me-2"></i>Process Your First Video
            </Link>
          </div>
        </div>
      ) : (
        <>
          <div className="row g-4">
            {videos.map((video) => (
              <div key={video.id} className="col-md-6 col-lg-4">
                <div
                  className="card h-100 shadow-sm border-0 hover-shadow transition"
                  style={{ cursor: 'pointer', transition: 'all 0.3s ease' }}
                  onClick={() => router.push(`/notes/${video.id}`)}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-5px)';
                    e.currentTarget.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '';
                  }}
                >
                  {video.thumbnail_url && (
                    <div className="position-relative">
                      <img
                        src={video.thumbnail_url}
                        className="card-img-top"
                        alt={video.title || 'Video thumbnail'}
                        style={{ height: '200px', objectFit: 'cover' }}
                      />
                      <div className="position-absolute top-0 end-0 m-2">
                        <span className="badge bg-dark bg-opacity-75">
                          <i className="bi bi-clock me-1"></i>
                          {formatDuration(video.duration_seconds)}
                        </span>
                      </div>
                    </div>
                  )}
                  <div className="card-body d-flex flex-column">
                    <h5 className="card-title mb-3 line-clamp-2" style={{
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden'
                    }}>
                      {video.title || 'Untitled Video'}
                    </h5>
                    <p className="card-text text-muted small mb-auto">
                      <i className="bi bi-calendar me-1"></i>
                      {new Date(video.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="card-footer bg-white border-top">
                    <div className="d-flex justify-content-between align-items-center gap-2">
                      <button
                        className="btn btn-primary btn-sm flex-fill"
                        onClick={(e) => {
                          e.stopPropagation();
                          router.push(`/notes/${video.id}`);
                        }}
                      >
                        <i className="bi bi-file-text me-1"></i>View Notes
                      </button>
                      <button
                        className="btn btn-outline-danger btn-sm"
                        onClick={(e) => handleDelete(video.id, e)}
                        disabled={deletingId === video.id}
                        title="Delete video"
                      >
                        {deletingId === video.id ? (
                          <span className="spinner-border spinner-border-sm" role="status">
                            <span className="visually-hidden">Deleting...</span>
                          </span>
                        ) : (
                          <i className="bi bi-trash"></i>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <nav aria-label="Page navigation" className="mt-5">
              <ul className="pagination justify-content-center">
                <li className={`page-item ${page === 1 ? 'disabled' : ''}`}>
                  <button
                    className="page-link"
                    onClick={() => setPage(page - 1)}
                    disabled={page === 1}
                  >
                    <i className="bi bi-chevron-left"></i> Previous
                  </button>
                </li>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                  <li key={p} className={`page-item ${page === p ? 'active' : ''}`}>
                    <button className="page-link" onClick={() => setPage(p)}>
                      {p}
                    </button>
                  </li>
                ))}
                <li className={`page-item ${page === totalPages ? 'disabled' : ''}`}>
                  <button
                    className="page-link"
                    onClick={() => setPage(page + 1)}
                    disabled={page === totalPages}
                  >
                    Next <i className="bi bi-chevron-right"></i>
                  </button>
                </li>
              </ul>
            </nav>
          )}

          <div className="text-center mt-4">
            <p className="text-muted mb-0">
              <i className="bi bi-info-circle me-1"></i>
              Showing {videos.length} of {total} video{total !== 1 ? 's' : ''}
            </p>
          </div>
        </>
      )}
    </div>
  );
}

