import {
  Bell,
  Search,
  ChevronDown,
  Command,
} from "lucide-react";

export default function Header() {
  return (
    <header className="flex h-[76px] items-center justify-between border-b border-white/[0.07] px-5 sm:px-8">
      <div>
        <p className="text-xs text-gray-500">
          Workspace / Dashboard
        </p>

        <h2 className="mt-1 text-sm font-semibold text-white">
          Research Overview
        </h2>
      </div>

      <div className="flex items-center gap-3 sm:gap-5">
        {/* Search */}
        <div className="hidden items-center gap-3 rounded-xl border border-white/[0.08] bg-white/[0.02] px-3 py-2.5 md:flex">
          <Search size={16} className="text-gray-500" />

          <input
            type="text"
            placeholder="Search research..."
            aria-label="Search research"
            className="w-36 bg-transparent text-xs text-white outline-none placeholder:text-gray-600"
          />

          <span className="flex items-center gap-1 rounded border border-white/10 px-1.5 py-1 text-[10px] text-gray-500">
            <Command size={10} /> K
          </span>
        </div>

        {/* Notifications */}
        <button
          type="button"
          aria-label="Notifications"
          className="relative rounded-xl border border-white/[0.08] p-2.5 text-gray-400 transition hover:bg-white/[0.05] hover:text-white"
        >
          <Bell size={17} />

          <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-indigo-400" />
        </button>

        {/* Profile */}
        <button
          type="button"
          className="flex items-center gap-2 text-gray-400 transition hover:text-white"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-full border border-indigo-400/20 bg-indigo-500/10 text-sm font-semibold text-indigo-300">
            R
          </div>

          <ChevronDown size={14} className="hidden sm:block" />
        </button>
      </div>
    </header>
  );
}