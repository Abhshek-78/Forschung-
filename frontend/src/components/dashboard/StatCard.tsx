import type { LucideIcon } from "lucide-react";
import { ArrowUpRight } from "lucide-react";

interface StatCardProps {
  title: string;
  value: number | string;
  description: string;
  icon: LucideIcon;
}

export default function StatCard({
  title,
  value,
  description,
  icon: Icon,
}: StatCardProps) {
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-[#101522] p-5 transition duration-300 hover:border-indigo-400/20 hover:bg-[#131a2a]">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-400">{title}</p>

          <h3 className="mt-4 text-3xl font-semibold tracking-tight text-white">
            {value}
          </h3>
        </div>

        <div className="rounded-xl border border-indigo-400/10 bg-indigo-500/10 p-3 text-indigo-300">
          <Icon size={21} />
        </div>
      </div>

      <div className="mt-5 flex items-center gap-2 border-t border-white/[0.06] pt-4">
        <ArrowUpRight size={14} className="text-indigo-300" />

        <p className="text-xs text-gray-500">{description}</p>
      </div>
    </div>
  );
}