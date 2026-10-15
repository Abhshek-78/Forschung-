import { useEffect, useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import ResearchCard from "../components/dashboard/ResearchCard";
import { fetchResearchProjects, type ResearchProject } from "../data/research";

export default function ResearchHistory() {
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  useEffect(() => { void fetchResearchProjects().then(setProjects); }, []);
  return <div className="min-h-screen bg-[#080b14] text-gray-200"><div className="flex min-h-screen"><Sidebar /><main className="min-w-0 flex-1"><Header /><div className="mx-auto max-w-5xl p-4 sm:p-8"><h1 className="text-3xl font-semibold text-white">Research history</h1><p className="mt-2 text-sm text-gray-400">Every real research run and generated report.</p><div className="mt-8 space-y-4">{projects.length ? projects.map((project) => <ResearchCard key={project.id} project={project} />) : <div className="rounded-2xl border border-dashed border-white/10 p-10 text-center text-sm text-gray-500">No research runs yet.</div>}</div></div></main></div></div>;
}
