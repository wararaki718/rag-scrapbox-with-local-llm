import { useState, useRef, useEffect, useCallback } from 'react';
import { 
  Send, Search, ExternalLink, Loader2, 
  Plus, User, Sparkles, MessageSquare, Menu, 
  Settings, Library, BookOpen, Clock, Command
} from 'lucide-react';
import { motion } from 'framer-motion';

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

const EXAMPLE_QUESTIONS = [
  "Scrapboxとは何ですか？",
  "このRAGシステムの仕組みを教えてください",
  "インデックスされている主なトピックは何ですか？",
];

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  const handleClear = () => {
    setMessages([]);
    setInput('');
  };

  const handleSubmit = async (e?: React.FormEvent, overrideInput?: string) => {
    e?.preventDefault();
    const query = overrideInput || input;
    if (!query.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
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
    <div className="drawer lg:drawer-open font-sans bg-base-100 text-base-content min-h-screen">
      <input id="my-drawer" type="checkbox" className="drawer-toggle" />
      
      {/* Main Content Area */}
      <div className="drawer-content flex flex-col h-screen overflow-hidden">
        {/* Top Navbar */}
        <div className="navbar bg-base-100/80 backdrop-blur border-b border-base-200 z-20 sticky top-0">
          <div className="flex-none lg:hidden">
            <label htmlFor="my-drawer" className="btn btn-square btn-ghost drawer-button">
              <Menu className="w-5 h-5" />
            </label>
          </div>
          <div className="flex-1 px-4">
            <div className="flex items-center gap-2">
              <div className="bg-primary p-1.5 rounded-lg text-primary-content shadow-sm">
                <Command className="w-5 h-5" />
              </div>
              <span className="text-xl font-black tracking-tight uppercase">Scrapbox <span className="text-primary">AI</span></span>
            </div>
          </div>
          <div className="flex-none">
            <div className="badge badge-outline badge-sm gap-1 hidden md:flex opacity-50 px-3 py-3">
              <Sparkles className="w-3 h-3" />
              <span>Gemma @ local-api</span>
            </div>
          </div>
        </div>

        {/* Messaging Area */}
        <div className="flex-1 overflow-y-auto bg-base-100 p-4 md:p-10 space-y-8 pb-32">
          <div className="max-w-4xl mx-auto w-full">
            {messages.length === 0 && (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="hero mt-12 mb-12"
              >
                <div className="hero-content text-center flex-col">
                  <div className="w-24 h-24 bg-primary/10 rounded-3xl flex items-center justify-center mb-6 rotate-3">
                    <BookOpen className="w-12 h-12 text-primary" />
                  </div>
                  <h1 className="text-5xl font-black tracking-tighter">知的生産を加速する</h1>
                  <p className="py-6 text-base-content/60 max-w-sm text-lg leading-relaxed">
                    Scrapboxの共有知から、必要な答えをAIが瞬時に導き出します。
                  </p>
                  
                  <div className="flex flex-wrap gap-2 justify-center mt-4">
                    {EXAMPLE_QUESTIONS.map((q, i) => (
                      <button
                        key={i}
                        onClick={() => handleSubmit(undefined, q)}
                        className="btn btn-neutral btn-outline btn-sm rounded-xl normal-case font-bold hover:btn-primary"
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            <div className="space-y-10">
              {messages.map((message, idx) => (
                <div key={idx} className={`chat ${message.role === 'user' ? 'chat-end' : 'chat-start'} animate-fade-in`}>
                  <div className="chat-image avatar">
                    <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shadow-md ${message.role === 'user' ? 'bg-primary text-primary-content' : 'bg-neutral text-neutral-content'}`}>
                      {message.role === 'user' ? <User className="w-5 h-5" /> : <Sparkles className="w-5 h-5" />}
                    </div>
                  </div>
                  <div className="chat-header opacity-40 text-[10px] font-black uppercase tracking-widest mb-2 px-1">
                    {message.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <div className={`chat-bubble text-base leading-relaxed py-4 px-6 shadow-sm max-w-[90%] md:max-w-[80%] ${message.role === 'user' ? 'chat-bubble-primary' : 'bg-base-200 text-base-content border border-base-300'}`}>
                    <div className="whitespace-pre-wrap">{message.content}</div>
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="chat-footer mt-4 w-full">
                      <SourceSection sources={message.sources} />
                    </div>
                  )}
                </div>
              ))}

              {isLoading && (
                <div className="chat chat-start">
                  <div className="chat-image avatar">
                    <div className="w-10 h-10 rounded-2xl bg-neutral text-neutral-content flex items-center justify-center shadow-md">
                      <Sparkles className="w-5 h-5" />
                    </div>
                  </div>
                  <div className="chat-bubble bg-base-200 text-base-content border border-base-300 flex items-center gap-4 py-4 px-6">
                    <span className="loading loading-spinner loading-md text-primary"></span>
                    <span className="text-sm font-bold opacity-40 uppercase tracking-widest">Generating Answer...</span>
                  </div>
                </div>
              )}
            </div>
            <div ref={messagesEndRef} className="h-4" />
          </div>
        </div>

        {/* Sticky Input Bar */}
        <div className="sticky bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-base-100 via-base-100/90 to-transparent">
          <div className="max-w-4xl mx-auto">
            <form onSubmit={handleSubmit} className="relative">
              <input
                type="text"
                placeholder="Ask your Scrapbox..."
                className="input input-bordered w-full pr-16 h-16 rounded-3xl shadow-xl shadow-neutral/5 focus:input-primary transition-all text-lg pl-8 bg-base-100"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="btn btn-primary btn-circle absolute right-3 top-2 shadow-lg hover:scale-105 active:scale-95 transition-transform"
              >
                {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Sidebar / Drawer Side */}
      <div className="drawer-side z-30">
        <label htmlFor="my-drawer" className="drawer-overlay"></label>
        <div className="menu p-6 w-80 min-h-full bg-base-200 text-base-content border-r border-base-300 flex flex-col gap-8">
          <div className="flex items-center gap-3 mb-6 px-2">
            <div className="bg-primary p-2 rounded-xl text-primary-content shadow-lg shadow-primary/20">
              <Search className="w-6 h-6" />
            </div>
            <h1 className="text-2xl font-black tracking-tighter">SCRAPBOX</h1>
          </div>

          <button 
            onClick={handleClear}
            className="btn btn-primary gap-2 normal-case w-full shadow-md hover:shadow-lg transition-all rounded-2xl"
          >
            <Plus className="w-5 h-5" />
            新しいチャット
          </button>

          <div className="flex-1 space-y-10 overflow-y-auto">
            <div className="space-y-4">
              <h2 className="text-[10px] font-black uppercase text-base-content/30 tracking-[0.3em] px-2">Knowledge Base</h2>
              <div className="space-y-1">
                {messages.length > 0 ? (
                  <button className="btn btn-ghost btn-sm w-full justify-start gap-4 normal-case font-bold py-3 h-auto rounded-xl bg-base-100/50">
                    <MessageSquare className="w-4 h-4 text-primary" />
                    <span className="truncate">{messages[0].content}</span>
                  </button>
                ) : (
                  <div className="px-6 py-10 border-2 border-dashed border-base-300 rounded-3xl flex flex-col items-center gap-3 text-base-content/20 italic text-xs">
                    <Clock className="w-8 h-8 opacity-20" />
                    <span>履歴はありません</span>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <h2 className="text-[10px] font-black uppercase text-base-content/30 tracking-[0.3em] px-2">System</h2>
              <button className="btn btn-ghost btn-sm w-full justify-start gap-4 normal-case rounded-xl">
                <Library className="w-4 h-4 opacity-50" /> Library
              </button>
              <button className="btn btn-ghost btn-sm w-full justify-start gap-4 normal-case rounded-xl font-medium">
                <Settings className="w-4 h-4 opacity-50" /> Settings
              </button>
            </div>
          </div>

          <div className="p-5 bg-primary/10 rounded-[2rem] border border-primary/10 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-primary/20 blur-3xl rounded-full -mr-12 -mt-12 transition-all group-hover:bg-primary/30" />
            <div className="relative">
              <div className="flex items-center gap-2 text-primary font-black text-xs uppercase tracking-widest mb-1">
                <Sparkles className="w-4 h-4" />
                <span>Gemma v2</span>
              </div>
              <p className="text-[11px] leading-relaxed font-bold opacity-60">
                100% Local RAG.<br/>No data leaves this server.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function SourceSection({ sources }: { sources: SearchResult[] }) {
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
}
