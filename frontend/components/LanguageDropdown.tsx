'use client';

import { useState } from 'react';
import { SUPPORTED_LANGUAGES, Language } from '@/lib/languages';

interface LanguageDropdownProps {
  videoId: string;
  onTranslationChange?: (translatedNotes: string, language: string) => void;
  currentLanguage?: string;
}

export default function LanguageDropdown({
  videoId,
  onTranslationChange,
  currentLanguage = 'en',
}: LanguageDropdownProps) {
  const [selectedLanguage, setSelectedLanguage] = useState(currentLanguage);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [wasCached, setWasCached] = useState(false);

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

  const handleLanguageChange = async (languageCode: string) => {
    if (languageCode === selectedLanguage) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_id: videoId,
          target_language: languageCode,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Translation failed');
      }

      const data = await response.json();
      setSelectedLanguage(languageCode);
      setWasCached(data.was_cached);

      if (onTranslationChange) {
        onTranslationChange(data.translated_notes, languageCode);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Translation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="language-dropdown mb-4" style={{
      background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%)',
      padding: '1.5rem',
      borderRadius: '1rem',
      border: '2px solid rgba(99, 102, 241, 0.1)'
    }}>
      <label htmlFor="languageSelect" className="form-label mb-3" style={{
        fontSize: '1.1rem',
        fontWeight: '700',
        color: '#1f2937',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
      }}>
        <div style={{
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 15px rgba(99, 102, 241, 0.3)'
        }}>
          <i className="bi bi-translate text-white"></i>
        </div>
        Translate Notes to 50+ Languages
      </label>
      <div className="input-group input-group-lg">
        <span className="input-group-text" style={{
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
          color: 'white',
          border: 'none',
          fontWeight: '600'
        }}>
          <i className="bi bi-globe me-2"></i>Language
        </span>
        <select
          id="languageSelect"
          className="form-select"
          value={selectedLanguage}
          onChange={(e) => handleLanguageChange(e.target.value)}
          disabled={loading}
          style={{
            border: '2px solid #e0e7ff',
            fontSize: '1rem',
            fontWeight: '500',
            padding: '0.75rem 1rem'
          }}
        >
          {SUPPORTED_LANGUAGES.map((lang: Language) => (
            <option key={lang.code} value={lang.code}>
              {lang.name} ({lang.code.toUpperCase()})
            </option>
          ))}
        </select>
        {loading && (
          <span className="input-group-text" style={{
            background: 'linear-gradient(135deg, #f0f4ff 0%, #faf5ff 100%)',
            border: '2px solid #e0e7ff',
            borderLeft: 'none'
          }}>
            <div className="spinner-border spinner-border-sm" role="status" style={{ color: '#6366f1' }}>
              <span className="visually-hidden">Loading...</span>
            </div>
          </span>
        )}
      </div>
      {error && (
        <div className="alert alert-danger mt-3 shadow-sm" role="alert" style={{
          borderRadius: '0.75rem',
          border: 'none',
          fontWeight: '600'
        }}>
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          {error}
        </div>
      )}
      {!loading && !error && wasCached && (
        <div className="mt-3 d-flex align-items-center" style={{ color: '#10b981', fontWeight: '600' }}>
          <i className="bi bi-check-circle-fill me-2"></i>
          Translation retrieved from cache
        </div>
      )}
      {!loading && !error && !wasCached && selectedLanguage !== 'en' && (
        <div className="mt-3 d-flex align-items-center" style={{ color: '#6366f1', fontWeight: '600' }}>
          <i className="bi bi-info-circle-fill me-2"></i>
          Translation completed successfully
        </div>
      )}
    </div>
  );
}

