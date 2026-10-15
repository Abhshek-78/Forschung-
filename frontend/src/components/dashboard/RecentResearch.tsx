import { Clock3, ArrowRight } from "lucide-react";

import type { ResearchProject } from "../../data/research";
import ResearchCard from "./ResearchCard";

interface RecentResearchProps {
  projects: ResearchProject[];
  isLoading: boolean;
}

export default function RecentResearch({
  projects,
  isLoading,
}: RecentResearchProps) {
  return (
    <section className="mt-10">
      <div className="mb-5 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-white">
            Recent Research
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Review your latest research runs and their results.
          </p>
        </div>

        <button
          type="button"
          className="flex shrink-0 items-center gap-2 text-xs font-medium text-indigo-300 transition hover:text-indigo-200"
        >
          View all
          <ArrowRight size={15} />
        </button>
      </div>

      {isLoading ? (
        <div className="rounded-2xl border border-white/[0.07] bg-[#101522] p-10 text-center text-sm text-gray-500">
          Loading research runs...
        </div>
      ) : projects.length > 0 ? (
        <div className="space-y-4">
          {projects.map((project) => (
            <ResearchCard
              key={project.id}
              project={project}
            />
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-dashed border-white/10 p-10 text-center">
          <Clock3
            size={28}
            className="mx-auto text-gray-500"
          />

          <h3 className="mt-4 font-medium text-white">
            No research yet
          </h3>

          <p className="mt-2 text-sm text-gray-500">
            Start a research run to see its real results here.
          </p>
        </div>
      )}
    </section>
  );
}