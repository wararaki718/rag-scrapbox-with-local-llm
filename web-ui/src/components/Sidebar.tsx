import { Search, Plus, MessageSquare, Clock, Library, Settings, Sparkles } from 'lucide-react';
import { Message } from '../types';

interface SidebarProps {
  messages: Message[];
  onClear: () => void;
}

export const Sidebar = ({ messages, onClear }: SidebarProps) => {
  return (
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
          onClick={onClear}
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
  );
};
