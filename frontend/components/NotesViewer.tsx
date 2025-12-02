'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface NotesViewerProps {
  notes: string;
  className?: string;
}

export default function NotesViewer({ notes, className = '' }: NotesViewerProps) {
  return (
    <div className={`notes-viewer ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Custom code block rendering with syntax highlighting
          code: ({ node, inline, className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <pre className="bg-light p-3 rounded border">
                <code className={className} {...props}>
                  {children}
                </code>
              </pre>
            ) : (
              <code className="bg-light px-2 py-1 rounded" {...props}>
                {children}
              </code>
            );
          },
          // Custom heading styles
          h1: ({ children }: any) => (
            <h1 className="mt-4 mb-3 border-bottom pb-2">{children}</h1>
          ),
          h2: ({ children }: any) => (
            <h2 className="mt-4 mb-3">{children}</h2>
          ),
          h3: ({ children }: any) => (
            <h3 className="mt-3 mb-2">{children}</h3>
          ),
          // Custom blockquote for quotes
          blockquote: ({ children }: any) => (
            <blockquote className="blockquote border-start border-primary border-3 ps-3 my-3">
              {children}
            </blockquote>
          ),
          // Custom list styling
          ul: ({ children }: any) => (
            <ul className="list-group list-group-flush mb-3">{children}</ul>
          ),
          ol: ({ children }: any) => (
            <ol className="mb-3">{children}</ol>
          ),
          li: ({ children }: any) => (
            <li className="mb-2">{children}</li>
          ),
        }}
      >
        {notes}
      </ReactMarkdown>
    </div>
  );
}

