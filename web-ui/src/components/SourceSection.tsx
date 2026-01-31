import { useState } from 'react';
import { ExternalLink, Library } from 'lucide-react';
import { SearchResult } from '../types';

interface SourceSectionProps {
  sources: SearchResult[];
}

export const SourceSection = ({ sources }: SourceSectionProps) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={`collapse collapse-arrow bg-base-200/50 border border-base-300 rounded-3xl transition-all duration-300 ${isOpen ? 'collapse-open' : 'collapse-close'}`}>
      <div 
        className="collapse-title text-xs font-black flex items-center gap-3 py-4 min-h-0 cursor-pointer hover:bg-base-300/30"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Library className="w-4 h-4 text-primary" />
        <span className="uppercase tracking-widest">Cited Sources ({sources.length})</span>
      </div>
      <div className="collapse-content px-4 transition-all">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 pb-4">
          {sources.map((source, idx) => (
            <div key={idx} className="card bg-base-100 shadow-sm border border-base-200 transition-all hover:border-primary/40 hover:shadow-md rounded-2xl">
              <div className="card-body p-5 gap-3">
                <div className="flex justify-between items-start gap-4">
                  <a 
                    href={source.url} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="text-xs font-black hover:text-primary transition-colors flex items-center gap-2 leading-snug"
                  >
                    <ExternalLink className="w-3.5 h-3.5 shrink-0" />
                    {source.title}
                  </a>
                  <div className="badge badge-primary badge-outline badge-xs font-mono font-bold scale-90">
                    {(source.score * 10).toFixed(1)}
                  </div>
                </div>
                <p className="text-[11px] leading-relaxed text-base-content/50 line-clamp-2">
                  {source.text}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
