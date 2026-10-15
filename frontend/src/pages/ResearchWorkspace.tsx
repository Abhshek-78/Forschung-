import { useEffect, useMemo, useState } from "react";
import { ArrowLeft, Check, Circle, Download, FileText, LoaderCircle, Sparkles } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import {
  fetchResearchProjects,
  researchPdfUrl,
  researchReportUrl,
  type ResearchProject,
} from "../data/research";

const stageNames = ["Academic search", "Reading papers", "Processing evidence", "Writing report", "Reviewing research", "Final revision"];

export default function ResearchWorkspace() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [project, setProject] = useState<ResearchProject | null>(null);
  const [report, setReport] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    const load = async () => {
      try {
        const projects = await fetchResearchProjects();
        const found = projects.find((item) => item.id === id);
        if (!cancelled) setProject(found ?? null);
        if (found?.status === "completed") {
          const response = await fetch(researchReportUrl(id));
          if (response.ok && !cancelled) setReport(await response.text());
        }
      } catch (reason: unknown) {
        if (!cancelled) setError(reason instanceof Error ? reason.message : "Could not load this research");
      }
    };
    void load();
    const timer = window.setInterval(() => void load(), 3000);
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [id]);

  const completedStages = useMemo(() => {
    if (!project) return 0;
    if (project.status === "completed") return stageNames.length;
    if (project.status === "failed") return Math.max(1, project.papersFound ? 2 : 1);
    return Math.min(stageNames.length - 1, Math.max(1, project.papersFound ? 2 : 1));
  }, [project]);

  return (
    <div className="min-h-screen bg-[#080b14] text-gray-200">
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="min-w-0 flex-1">
          <Header />
          <div className="mx-auto max-w-5xl p-4 sm:p-8">
            <button type="button" onClick={() => navigate("/")} className="mb-6 inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white">
              <ArrowLeft size={17} /> Back to dashboard
            </button>
            {error && <div className="mb-5 rounded-xl border border-red-400/20 bg-red-400/10 p-4 text-sm text-red-200">{error}</div>}
            <section className="rounded-3xl border border-indigo-400/10 bg-gradient-to-br from-[#151b31] to-[#101522] p-5 sm:p-8">
              <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <span className="inline-flex items-center gap-2 rounded-full border border-indigo-400/15 bg-indigo-400/10 px-3 py-1.5 text-xs text-indigo-300">
                    <Sparkles size={14} /> Live research pipeline
                  </span>
                  <h1 className="mt-5 break-words text-2xl font-semibold text-white sm:text-3xl">{project?.topic ?? "Loading research..."}</h1>
                  <p className="mt-3 text-sm text-gray-400">Your real backend pipeline is working. This page refreshes automatically.</p>
                </div>
                <span className={`shrink-0 rounded-full px-3 py-1.5 text-xs font-medium ${project?.status === "completed" ? "bg-emerald-400/10 text-emerald-300" : project?.status === "failed" ? "bg-red-400/10 text-red-300" : "bg-amber-400/10 text-amber-300"}`}>
                  {project?.status ?? "Loading"}
                </span>
              </div>
              <div className="mt-8 h-2 overflow-hidden rounded-full bg-white/10">
                <div className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-violet-400 transition-all duration-700" style={{ width: `${(completedStages / stageNames.length) * 100}%` }} />
              </div>
              <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {stageNames.map((stage, index) => {
                  const done = index < completedStages;
                  const active = !done && project?.status === "running" && index === completedStages;
                  return (
                    <div key={stage} className={`flex items-center gap-3 rounded-xl border p-3 text-sm ${done ? "border-emerald-400/20 bg-emerald-400/5 text-emerald-200" : active ? "border-indigo-400/30 bg-indigo-400/10 text-indigo-200" : "border-white/[0.06] text-gray-500"}`}>
                      {done ? <Check size={17} /> : active ? <LoaderCircle size={17} className="animate-spin" /> : <Circle size={17} />}
                      {stage}
                    </div>
                  );
                })}
              </div>
              {project?.status === "running" && (
                <div className="mt-7 flex items-center gap-3 rounded-xl border border-indigo-400/15 bg-indigo-400/5 p-4 text-sm text-indigo-200">
                  <LoaderCircle size={18} className="animate-spin" />
                  Agents are searching, reading, and synthesizing academic sources...
                </div>
              )}
            </section>
            {project?.status === "completed" && (
              <section className="mt-6 rounded-3xl border border-emerald-400/15 bg-[#101522] p-5 sm:p-8">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h2 className="flex items-center gap-2 text-xl font-semibold text-white"><FileText size={20} className="text-emerald-300" /> Research report</h2>
                    <p className="mt-2 text-sm text-gray-400">{project.papersFound} papers found · {project.papersRead} read · {project.evidenceChunks} evidence chunks</p>
                  </div>
                  <a href={researchPdfUrl(project.id)} download className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-500 px-4 py-3 text-sm font-semibold text-white hover:bg-indigo-400"><Download size={17} /> Download PDF</a>
                </div>
                <article className="mt-6 max-h-[600px] overflow-auto whitespace-pre-wrap rounded-2xl border border-white/[0.06] bg-[#080b14] p-4 text-sm leading-7 text-gray-300 sm:p-6">{report || "Loading report..."}</article>
              </section>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
