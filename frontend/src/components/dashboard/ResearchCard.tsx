import {
  ArrowUpRight,
  BookOpen,
  FileText,
  Layers3,
  CheckCircle2,
} from "lucide-react";

import type { ResearchProject } from "../../data/research";

interface ResearchCardProps {
  project: ResearchProject;
}

export default function ResearchCard({
  project,
}: ResearchCardProps) {
  const isCompleted = project.status === "completed";

  return (
    <article className="rounded-2xl border border-white/[0.07] bg-[#101522] p-5 transition hover:border-indigo-400/20 sm:p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-indigo-400/10 bg-indigo-500/10 text-indigo-300">
            <BookOpen size={23} />
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="font-semibold text-white">
                {project.topic}
              </h3>

              <span
                className={`rounded-full px-2.5 py-1 text-[10px] font-medium ${
                  isCompleted
                    ? "border border-emerald-400/10 bg-emerald-400/10 text-emerald-300"
                    : project.status === "running"
                      ? "border border-amber-400/10 bg-amber-400/10 text-amber-300"
                      : "border border-red-400/10 bg-red-400/10 text-red-300"
                }`}
              >
                {project.status === "completed"
                  ? "Completed"
                  : project.status === "running"
                    ? "Running"
                    : "Failed"}
              </span>
            </div>

            <p className="mt-2 text-xs text-gray-500">
              Research ID: {project.id}
            </p>
          </div>
        </div>

        <button
          type="button"
          aria-label="Open research project"
          className="self-end rounded-lg p-2 text-gray-500 transition hover:bg-white/[0.05] hover:text-white sm:self-auto"
        >
          <ArrowUpRight size={19} />
        </button>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-4">
          <BookOpen size={17} className="text-indigo-300" />

          <p className="mt-3 text-2xl font-semibold text-white">
            {project.papersFound}
          </p>

          <p className="mt-1 text-xs text-gray-500">
            Papers found
          </p>
        </div>

        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-4">
          <FileText size={17} className="text-violet-300" />

          <p className="mt-3 text-2xl font-semibold text-white">
            {project.papersRead}
          </p>

          <p className="mt-1 text-xs text-gray-500">
            Papers read
          </p>
        </div>

        <div className="rounded-xl border border-white/[0.05] bg-white/[0.02] p-4">
          <Layers3 size={17} className="text-sky-300" />

          <p className="mt-3 text-2xl font-semibold text-white">
            {project.evidenceChunks}
          </p>

          <p className="mt-1 text-xs text-gray-500">
            Evidence chunks
          </p>
        </div>
      </div>

      <div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-white/[0.06] pt-5">
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <CheckCircle2
            size={15}
            className="text-emerald-400"
          />

          <span>
            {project.errors === 0
              ? "No pipeline errors reported"
              : `${project.errors} pipeline errors reported`}
          </span>
        </div>

        <button
          type="button"
          className="rounded-lg bg-indigo-500/10 px-4 py-2.5 text-xs font-semibold text-indigo-300 transition hover:bg-indigo-500/20"
        >
          View Research
        </button>
      </div>
    </article>
  );
}