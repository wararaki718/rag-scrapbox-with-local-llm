import { Menu, Command, Sparkles } from 'lucide-react';

export const Navbar = () => {
  return (
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
  );
};
