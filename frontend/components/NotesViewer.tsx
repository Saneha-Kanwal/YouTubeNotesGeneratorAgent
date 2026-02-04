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
          code: (props: any) => {
            const { inline, className, children, ...rest } = props;
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <pre className="bg-light p-3 rounded border">
                <code className={className} {...rest}>
                  {children}
                </code>
              </pre>
            ) : (
              <code className="bg-light px-2 py-1 rounded" {...rest}>
                {children}
              </code>
            );
          },
          // Custom heading styles
          h1: (props: any) => (
            <h1 className="mt-4 mb-3 border-bottom pb-2">{props.children}</h1>
          ),
          h2: (props: any) => (
            <h2 className="mt-4 mb-3">{props.children}</h2>
          ),
          h3: (props: any) => (
            <h3 className="mt-3 mb-2">{props.children}</h3>
          ),
          // Custom blockquote for quotes
          blockquote: (props: any) => (
            <blockquote className="blockquote border-start border-primary border-3 ps-3 my-3">
              {props.children}
            </blockquote>
          ),
          // Custom list styling
          ul: (props: any) => (
            <ul className="list-group list-group-flush mb-3">{props.children}</ul>
          ),
          ol: (props: any) => (
            <ol className="mb-3">{props.children}</ol>
          ),
          li: (props: any) => (
            <li className="mb-2">{props.children}</li>
          ),
        }}
      >
        {notes}
      </ReactMarkdown>
    </div>
  );
}

