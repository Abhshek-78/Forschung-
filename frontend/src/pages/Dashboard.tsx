import {
  BookOpen,
  FileCheck2,
  Layers3,
  Sparkles,
  ArrowRight,
  Microscope,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
const navigate = useNavigate();

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import StatCard from "../components/dashboard/StatCard";
import RecentResearch from "../components/dashboard/RecentResearch";

import { researchProjects } from "../data/research";

export default function Dashboard() {
  const totalRuns = researchProjects.length;

  const totalPapers = researchProjects.reduce(
    (sum, project) => sum + project.papersFound,
    0
  );

  const totalEvidence = researchProjects.reduce(
    (sum, project) => sum + project.evidenceChunks,
    0
  );

  const completedReports = researchProjects.filter(
    (project) =>
      project.status === "completed"
  ).length;

  return (
    <div className="min-h-screen bg-[#080b14] text-gray-200">
      <div className="flex min-h-screen">
        <Sidebar />

        <main className="min-w-0 flex-1">
          <Header />

          <div className="mx-auto max-w-[1500px] p-5 sm:p-8">
            {/* Welcome section */}
            <section className="relative overflow-hidden rounded-3xl border border-indigo-400/10 bg-gradient-to-br from-[#151b31] via-[#101522] to-[#101522] p-6 sm:p-9">
              <div className="pointer-events-none absolute -right-12 -top-24 h-72 w-72 rounded-full bg-indigo-500/10 blur-3xl" />

              <div className="relative max-w-2xl">
                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-indigo-400/15 bg-indigo-400/10 px-3 py-1.5 text-xs text-indigo-300">
                  <Sparkles size={14} />

                  AI-Powered Research Workspace
                </div>

                <h1 className="text-3xl font-semibold leading-tight tracking-tight text-white sm:text-4xl">
                  Turn academic research into{" "}
                  <span className="text-indigo-400">
                    meaningful insights.
                  </span>
                </h1>

                <p className="mt-4 max-w-xl text-sm leading-7 text-gray-400 sm:text-base">
                  Explore academic literature, connect evidence
                  across papers, and develop research ideas using
                  your multi-agent AI research system.
                </p>

                <button
                  type="button"
                  className="mt-7 inline-flex items-center gap-2 rounded-xl bg-indigo-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/20 transition hover:-translate-y-0.5 hover:bg-indigo-400"
                >
                  <Sparkles size={17} />

                  New Research

                  <ArrowRight size={16} />
                </button>
              </div>
            </section>

            {/* Statistics */}
            <section className="mt-8">
              <div className="mb-5">
                <h2 className="text-lg font-semibold text-white">
                  Research Overview
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                  A summary of the research runs in this workspace.
                </p>
              </div>

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <StatCard
                  title="Research Runs"
                  value={totalRuns}
                  description="Projects in this sample"
                  icon={Microscope}
                />

                <StatCard
                  title="Papers Found"
                  value={totalPapers}
                  description="Across research runs"
                  icon={BookOpen}
                />

                <StatCard
                  title="Evidence Chunks"
                  value={totalEvidence}
                  description="Processed evidence"
                  icon={Layers3}
                />

                <StatCard
                  title="Completed Reports"
                  value={completedReports}
                  description="Successfully completed"
                  icon={FileCheck2}
                />
              </div>
            </section>

            {/* Recent research */}
            <RecentResearch />

            {/* Footer */}
            <footer className="mt-12 border-t border-white/[0.06] py-6 text-center text-xs text-gray-600">
              Research Studio · AI-assisted academic research
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
}