import {
  Atom,
  LayoutDashboard,
  Plus,
  History,
  BookOpen,
  Settings,
  PanelLeftClose,
  Sparkles,
} from "lucide-react";

const navigation = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    active: true,
  },
  {
    label: "Research History",
    icon: History,
    active: false,
  },
  {
    label: "Research Sources",
    icon: BookOpen,
    active: false,
  },
];

export default function Sidebar() {
  return (
    <aside className="flex min-h-screen w-64 shrink-0 flex-col border-r border-white/[0.07] bg-[#0b0e17] p-5">
      {/* Logo */}
      <div className="mb-10 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/15 text-indigo-400">
            <Atom size={24} />
          </div>

          <div>
            <h1 className="text-sm font-bold tracking-wide text-white">
              Forschung ai
            </h1>

            <p className="mt-1 text-[10px] tracking-[0.18em] text-gray-500">
              AI RESEARCH PLATFORM
            </p>
          </div>
        </div>

        <button
          type="button"
          aria-label="Sidebar options"
          className="text-gray-500 transition hover:text-white"
        >
          <PanelLeftClose size={17} />
        </button>
      </div>

      {/* New Research */}
      <button
        type="button"
        className="mb-8 flex items-center justify-center gap-2 rounded-xl bg-indigo-500 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/10 transition hover:bg-indigo-400"
      >
        <Plus size={18} />
        New Research
      </button>

      {/* Navigation */}
      <p className="mb-3 px-2 text-[10px] font-semibold tracking-[0.2em] text-gray-600">
        WORKSPACE
      </p>

      <nav className="space-y-2">
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              type="button"
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm transition ${
                item.active
                  ? "border border-indigo-400/10 bg-indigo-500/10 text-indigo-300"
                  : "text-gray-400 hover:bg-white/[0.04] hover:text-white"
              }`}
            >
              <Icon size={18} />
              <span>{item.label}</span>

              {item.active && (
                <span className="ml-auto h-1.5 w-1.5 rounded-full bg-indigo-400" />
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom section */}
      <div className="mt-auto">
        <div className="mb-5 rounded-2xl border border-indigo-400/10 bg-indigo-500/[0.07] p-4">
          <Sparkles size={20} className="mb-3 text-indigo-400" />

          <h3 className="text-sm font-semibold text-white">
            Research smarter
          </h3>

          <p className="mt-2 text-xs leading-5 text-gray-400">
            Discover insights across academic papers with AI-powered research.
          </p>
        </div>

        <button
          type="button"
          className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm text-gray-400 transition hover:bg-white/[0.04] hover:text-white"
        >
          <Settings size={18} />
          Settings
        </button>

        <div className="mt-4 border-t border-white/[0.07] pt-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-indigo-400 to-violet-600 text-sm font-bold text-white">
              R
            </div>

            <div>
              <p className="text-sm font-medium text-white">
                Researcher
              </p>

              <p className="mt-1 text-xs text-gray-500">
                AI Workspace
              </p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}