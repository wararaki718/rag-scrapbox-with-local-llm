import { Send, Loader2 } from 'lucide-react';

interface ChatInputProps {
  input: string;
  isLoading: boolean;
  onInputChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export const ChatInput = ({ input, isLoading, onInputChange, onSubmit }: ChatInputProps) => {
  return (
    <div className="sticky bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-base-100 via-base-100/90 to-transparent">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={onSubmit} className="relative">
          <input
            type="text"
            placeholder="Ask your Scrapbox..."
            className="input input-bordered w-full pr-16 h-16 rounded-3xl shadow-xl shadow-neutral/5 focus:input-primary transition-all text-lg pl-8 bg-base-100"
            value={input}
            onChange={(e) => onInputChange(e.target.value)}
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
  );
};
