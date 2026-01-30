import { useState, useRef, useEffect } from 'react';
import { Send, Search, ExternalLink, ChevronDown, ChevronUp, Loader2 } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface SearchResult {
  text: string;
  title: string;
  url: string;
  score: number;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: SearchResult[];
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Vite proxy is configured to redirect /api to the backend in dev
      // In production, Nginx or similar will handle /api
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'エラーが発生しました。バックエンドサーバーの起動状況を確認してください。' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 py-4 px-6 flex items-center gap-2 flex-shrink-0">
        <Search className="w-6 h-6 text-blue-600" />
        <h1 className="text-xl font-bold text-gray-800">Scrapbox RAG Search</h1>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-gray-500 space-y-4">
            <Search className="w-16 h-16 opacity-20" />
            <p className="text-lg font-medium">Scrapbox の知識ベースに質問してみましょう</p>
          </div>
        )}

        {messages.map((message, idx) => (
          <div
            key={idx}
            className={cn(
              "flex flex-col max-w-3xl mx-auto space-y-2",
              message.role === 'user' ? "items-end" : "items-start"
            )}
          >
            <div
              className={cn(
                "px-4 py-2 rounded-2xl shadow-sm",
                message.role === 'user'
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-white border border-gray-200 text-gray-800 rounded-bl-none"
              )}
            >
              <div className="whitespace-pre-wrap">{message.content}</div>
            </div>

            {message.sources && message.sources.length > 0 && (
              <SourceList sources={message.sources} />
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start max-w-3xl mx-auto">
            <div className="bg-white border border-gray-200 px-4 py-2 rounded-2xl rounded-bl-none shadow-sm flex items-center gap-2 text-gray-500">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>回答を生成中...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4 flex-shrink-0">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-2">
          <input
            className="flex-1 bg-gray-100 border-none rounded-full px-4 py-2 focus:ring-2 focus:ring-blue-500 transition-all outline-none"
            placeholder="質問を入力してください..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-blue-600 text-white rounded-full p-2 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
}

function SourceList({ sources }: { sources: SearchResult[] }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="w-full max-w-md">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1 text-xs font-medium text-gray-500 hover:text-gray-700 transition-colors px-1"
      >
        {isOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
        <span>出典 ({sources.length})</span>
      </button>

      {isOpen && (
        <div className="mt-2 space-y-2">
          {sources.map((source, idx) => (
            <div key={idx} className="bg-white border border-gray-200 rounded-lg p-3 text-sm shadow-sm hover:border-blue-300 transition-colors">
              <div className="flex justify-between items-start mb-1">
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-semibold text-blue-600 hover:underline flex items-center gap-1"
                >
                  {source.title}
                  <ExternalLink className="w-3 h-3" />
                </a>
                <span className="text-[10px] text-gray-400 bg-gray-100 px-1.5 rounded-full">
                  Score: {source.score.toFixed(4)}
                </span>
              </div>
              <p className="text-gray-600 line-clamp-2 italic">{source.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
