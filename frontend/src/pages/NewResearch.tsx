import { useState } from "react";
import type { FormEvent } from "react";
import { ArrowLeft, LoaderCircle, Play, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import { createResearch } from "../data/research";

export default function NewResearch() {
  const navigate = useNavigate();
  const [topic, setTopic] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!topic.trim() || isSubmitting) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const { id } = await createResearch(topic.trim());
      navigate(`/research/${id}`);
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "Could not start research");
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#080b14] text-gray-200">
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="min-w-0 flex-1">
          <Header />
          <div className="mx-auto max-w-3xl p-5 sm:p-8">
            <button
              type="button"
              onClick={() => navigate("/")}
              className="mb-8 inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white"
            >
              <ArrowLeft size={17} /> Back to dashboard
            </button>
            <section className="rounded-3xl border border-indigo-400/10 bg-[#101522] p-6 sm:p-9">
              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-400/15 bg-indigo-400/10 px-3 py-1.5 text-xs text-indigo-300">
                <Sparkles size={14} /> AI-Powered Research
              </div>
              <h1 className="text-3xl font-semibold text-white">Start new research</h1>
              <p className="mt-3 text-sm leading-6 text-gray-400">
                Enter a topic. The backend will search academic sources, read available
                papers, process evidence, and generate the report.
              </p>
              <form onSubmit={handleSubmit} className="mt-8">
                <label htmlFor="topic" className="text-sm font-medium text-gray-300">
                  Research topic
                </label>
                <textarea
                  id="topic"
                  value={topic}
                  onChange={(event) => setTopic(event.target.value)}
                  placeholder="e.g. How can NLP improve language learning?"
                  rows={5}
                  className="mt-3 w-full resize-y rounded-xl border border-white/10 bg-white/[0.03] p-4 text-sm text-white outline-none transition focus:border-indigo-400/50"
                  required
                />
                {error && <p className="mt-3 text-sm text-red-300">{error}</p>}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="mt-5 inline-flex items-center gap-2 rounded-xl bg-indigo-500 px-5 py-3 text-sm font-semibold text-white hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isSubmitting ? <LoaderCircle size={17} className="animate-spin" /> : <Play size={17} />}
                  {isSubmitting ? "Starting pipeline..." : "Start research"}
                </button>
              </form>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}
