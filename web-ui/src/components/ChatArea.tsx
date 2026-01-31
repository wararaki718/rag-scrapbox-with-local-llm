import { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, User, Sparkles } from 'lucide-react';
import { Message } from '../types';
import { SourceSection } from './SourceSection';

interface ChatAreaProps {
  messages: Message[];
  isLoading: boolean;
  onExampleClick: (query: string) => void;
}

const EXAMPLE_QUESTIONS = [
  "Scrapboxとは何ですか？",
  "このRAGシステムの仕組みを教えてください",
  "インデックスされている主なトピックは何ですか？",
];

export const ChatArea = ({ messages, isLoading, onExampleClick }: ChatAreaProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
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
                    onClick={() => onExampleClick(q)}
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
  );
};
