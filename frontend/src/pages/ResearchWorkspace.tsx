import { useEffect, useState } from "react";

import {
  ArrowLeft,
  BookOpen,
  Check,
  CheckCircle2,
  Circle,
  Clock3,
  Download,
  FileText,
  FlaskConical,
  Layers3,
  LoaderCircle,
  Play,
  RotateCcw,
  Sparkles,
  XCircle,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

// =====================================================
// PIPELINE TYPES
// =====================================================

type StageStatus = "pending" | "running" | "completed";

interface PipelineStage {
  id: number;
  title: string;
  description: string;
  status: StageStatus;
}

// =====================================================
// INITIAL PIPELINE STAGES
// =====================================================

const initialStages: PipelineStage[] = [
  {
    id: 1,
    title: "Academic Search",
    description: "Searching academic databases for relevant papers.",
    status: "pending",
  },
  {
    id: 2,
    title: "PDF Reader",
    description: "Downloading and extracting research paper content.",
    status: "pending",
  },
  {
    id: 3,
    title: "Evidence Processor",
    description: "Creating evidence chunks from extracted content.",
    status: "pending",
  },
  {
    id: 4,
    title: "Research Writer",
    description: "Generating a structured research report.",
    status: "pending",
  },
  {
    id: 5,
    title: "Research Critic",
    description: "Reviewing the report for missing evidence and gaps.",
    status: "pending",
  },
  {
    id: 6,
    title: "Revision",
    description: "Improving the report using the review feedback.",
    status: "pending",
  },
];

// =====================================================
// RESEARCH WORKSPACE
// =====================================================

export default function ResearchWorkspace() {
  const navigate = useNavigate();

  const [stages, setStages] =
    useState<PipelineStage[]>(initialStages);

  const [currentStage, setCurrentStage] = useState(-1);

  const [isRunning, setIsRunning] = useState(false);

  const [isCompleted, setIsCompleted] = useState(false);

  const [started, setStarted] = useState(false);

  // Demo research information.
  // Later, this information will come from the backend.

  const researchTopic =
    "How to Apply YOLO in Traffic Management";

  const papersFound = 9;

  const papersRead = 6;

  const evidenceChunks = 102;

  // ===================================================
  // CALCULATE PROGRESS
  // ===================================================

  const completedStages = stages.filter(
    (stage) => stage.status === "completed"
  ).length;

  const progress = Math.round(
    (completedStages / stages.length) * 100
  );

  // ===================================================
  // SIMULATE PIPELINE EXECUTION
  // ===================================================

  useEffect(() => {
    if (!isRunning) {
      return;
    }

    const timer = window.setTimeout(() => {
      const nextStage = currentStage + 1;

      // All stages have finished.
      if (nextStage >= stages.length) {
        setIsRunning(false);
        setIsCompleted(true);
        return;
      }

      setCurrentStage(nextStage);

      setStages((previousStages) =>
        previousStages.map((stage, index) => {
          if (index < nextStage) {
            return {
              ...stage,
              status: "completed",
            };
          }

          if (index === nextStage) {
            return {
              ...stage,
              status: "running",
            };
          }

          return {
            ...stage,
            status: "pending",
          };
        })
      );
    }, 1500);

    return () => {
      window.clearTimeout(timer);
    };
  }, [isRunning, currentStage, stages.length]);

  // ===================================================
  // START RESEARCH DEMO
  // ===================================================

  function startResearch() {
    if (isRunning) {
      return;
    }

    setStages(
      initialStages.map((stage, index) => ({
        ...stage,
        status: index === 0 ? "running" : "pending",
      }))
    );

    setCurrentStage(0);

    setIsCompleted(false);

    setStarted(true);

    setIsRunning(true);
  }

  // ===================================================
  // RESET DEMO
  // ===================================================

  function resetResearch() {
    setStages(initialStages);

    setCurrentStage(-1);

    setIsRunning(false);

    setIsCompleted(false);

    setStarted(false);
  }

  // ===================================================
  // STAGE ICON
  // ===================================================

  function getStageIcon(status: StageStatus) {
    if (status === "completed") {
      return <Check size={18} />;
    }

    if (status === "running") {
      return (
        <LoaderCircle
          size={18}
          className="animate-spin"
        />
      );
    }

    return <Circle size={18} />;
  }

  // ===================================================
  // RENDER PAGE
  // ===================================================

  return (
    <div className="min-h-screen bg-[#080b14] text-gray-200">
      <div className="flex min-h-screen">
        <Sidebar />

        <main className="min-w-0 flex-1">
          <Header />

          <div className="mx-auto max-w-[1500px] p-5 sm:p-8">

            {/* ========================================= */}
            {/* BACK NAVIGATION */}
            {/* ========================================= */}

            <button
              type="button"
              onClick={() => navigate("/")}
              className="mb-6 inline-flex items-center gap-2 text-sm text-gray-400 transition hover:text-white"
            >
              <ArrowLeft size={17} />

              Back to Dashboard
            </button>

            {/* ========================================= */}
            {/* RESEARCH HEADING */}
            {/* ========================================= */}

            <section className="rounded-3xl border border-indigo-400/10 bg-gradient-to-br from-[#151b31] via-[#101522] to-[#101522] p-6 sm:p-8">

              <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-start">

                <div className="max-w-3xl">

                  <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-indigo-400/15 bg-indigo-400/10 px-3 py-1.5 text-xs text-indigo-300">
                    <FlaskConical size={14} />

                    Research Workspace
                  </div>

                  <h1 className="text-2xl font-semibold leading-tight text-white sm:text-3xl">
                    {researchTopic}
                  </h1>

                  <p className="mt-4 text-sm leading-7 text-gray-400">
                    Monitor the research pipeline as academic
                    papers are collected, processed, analyzed,
                    and converted into a final report.
                  </p>

                  <div className="mt-5 flex flex-wrap items-center gap-3 text-xs text-gray-500">

                    <span className="rounded-lg border border-white/[0.08] bg-white/[0.03] px-3 py-2">
                      Research ID: research-demo-001
                    </span>

                    <span className="rounded-lg border border-white/[0.08] bg-white/[0.03] px-3 py-2">
                      Demo Mode
                    </span>

                  </div>
                </div>

                {/* ACTION BUTTONS */}

                <div className="flex flex-wrap gap-3">

                  {!isRunning && !isCompleted && (
                    <button
                      type="button"
                      onClick={startResearch}
                      className="inline-flex items-center gap-2 rounded-xl bg-indigo-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400"
                    >
                      <Play size={17} />

                      {started
                        ? "Run Again"
                        : "Start Demo"}
                    </button>
                  )}

                  {isRunning && (
                    <div className="inline-flex items-center gap-2 rounded-xl border border-indigo-400/20 bg-indigo-500/10 px-5 py-3 text-sm font-medium text-indigo-300">
                      <LoaderCircle
                        size={17}
                        className="animate-spin"
                      />

                      Processing...
                    </div>
                  )}

                  {isCompleted && (
                    <button
                      type="button"
                      onClick={resetResearch}
                      className="inline-flex items-center gap-2 rounded-xl border border-white/10 px-5 py-3 text-sm font-medium text-gray-300 transition hover:bg-white/[0.05]"
                    >
                      <RotateCcw size={17} />

                      Reset Demo
                    </button>
                  )}

                </div>

              </div>

              {/* OVERALL PROGRESS */}

              <div className="mt-8 border-t border-white/[0.07] pt-6">

                <div className="mb-3 flex items-center justify-between gap-3">

                  <span className="text-sm font-medium text-gray-300">
                    Overall Progress
                  </span>

                  <span className="text-sm font-semibold text-indigo-300">
                    {progress}%
                  </span>

                </div>

                <div
                  className="h-2.5 overflow-hidden rounded-full bg-white/[0.07]"
                  role="progressbar"
                  aria-label="Research pipeline progress"
                  aria-valuenow={progress}
                  aria-valuemin={0}
                  aria-valuemax={100}
                >
                  <div
                    className="h-full rounded-full bg-indigo-500 transition-all duration-700"
                    style={{
                      width: `${progress}%`,
                    }}
                  />
                </div>

                <p className="mt-3 text-xs text-gray-500">
                  {isCompleted
                    ? "All demo stages have completed."
                    : `${completedStages} of ${stages.length} stages completed.`}
                </p>

              </div>

            </section>

            {/* ========================================= */}
            {/* STATISTICS */}
            {/* ========================================= */}

            <section className="mt-7 grid grid-cols-1 gap-4 sm:grid-cols-3">

              <div className="rounded-2xl border border-white/[0.07] bg-[#101522] p-5">

                <div className="flex items-center justify-between">

                  <span className="text-sm text-gray-400">
                    Papers Found
                  </span>

                  <BookOpen
                    size={20}
                    className="text-indigo-300"
                  />

                </div>

                <h2 className="mt-4 text-3xl font-semibold text-white">
                  {papersFound}
                </h2>

                <p className="mt-2 text-xs text-gray-500">
                  Across academic sources
                </p>

              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#101522] p-5">

                <div className="flex items-center justify-between">

                  <span className="text-sm text-gray-400">
                    Papers Read
                  </span>

                  <FileText
                    size={20}
                    className="text-violet-300"
                  />

                </div>

                <h2 className="mt-4 text-3xl font-semibold text-white">
                  {papersRead}
                </h2>

                <p className="mt-2 text-xs text-gray-500">
                  Successfully extracted
                </p>

              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#101522] p-5">

                <div className="flex items-center justify-between">

                  <span className="text-sm text-gray-400">
                    Evidence Chunks
                  </span>

                  <Layers3
                    size={20}
                    className="text-sky-300"
                  />

                </div>

                <h2 className="mt-4 text-3xl font-semibold text-white">
                  {evidenceChunks}
                </h2>

                <p className="mt-2 text-xs text-gray-500">
                  Processed evidence segments
                </p>

              </div>

            </section>

            {/* ========================================= */}
            {/* PIPELINE */}
            {/* ========================================= */}

            <section className="mt-10">

              <div className="mb-5">

                <h2 className="text-lg font-semibold text-white">
                  Research Pipeline
                </h2>

                <p className="mt-2 text-sm text-gray-500">
                  Follow the progress of each research agent.
                </p>

              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#101522] p-5 sm:p-7">

                <div className="space-y-0">

                  {stages.map((stage, index) => {

                    const isLast =
                      index === stages.length - 1;

                    return (
                      <div
                        key={stage.id}
                        className="relative flex gap-4 pb-8 last:pb-0"
                      >

                        {/* TIMELINE */}

                        <div className="relative flex flex-col items-center">

                          <div
                            className={`z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border ${
                              stage.status === "completed"
                                ? "border-emerald-400/20 bg-emerald-400/10 text-emerald-300"
                                : stage.status === "running"
                                  ? "border-indigo-400/30 bg-indigo-500/15 text-indigo-300"
                                  : "border-white/[0.08] bg-white/[0.03] text-gray-500"
                            }`}
                          >
                            {getStageIcon(stage.status)}
                          </div>

                          {!isLast && (
                            <div
                              className={`absolute top-10 h-full w-px ${
                                stage.status === "completed"
                                  ? "bg-emerald-400/30"
                                  : "bg-white/[0.08]"
                              }`}
                            />
                          )}

                        </div>

                        {/* STAGE INFORMATION */}

                        <div className="min-w-0 flex-1 pb-1">

                          <div className="flex flex-wrap items-center justify-between gap-3">

                            <h3 className="font-medium text-white">
                              {stage.title}
                            </h3>

                            <span
                              className={`rounded-full px-2.5 py-1 text-[10px] font-medium ${
                                stage.status === "completed"
                                  ? "bg-emerald-400/10 text-emerald-300"
                                  : stage.status === "running"
                                    ? "bg-indigo-400/10 text-indigo-300"
                                    : "bg-white/[0.04] text-gray-500"
                              }`}
                            >
                              {stage.status === "completed"
                                ? "Completed"
                                : stage.status === "running"
                                  ? "Running"
                                  : "Pending"}
                            </span>

                          </div>

                          <p className="mt-2 text-sm leading-6 text-gray-500">
                            {stage.description}
                          </p>

                          {stage.status === "running" && (
                            <div className="mt-3 flex items-center gap-2 text-xs text-indigo-300">

                              <LoaderCircle
                                size={14}
                                className="animate-spin"
                              />

                              Agent is processing...
                            </div>
                          )}

                          {stage.status === "completed" && (
                            <div className="mt-3 flex items-center gap-2 text-xs text-emerald-300">

                              <CheckCircle2 size={14} />

                              Stage completed successfully
                            </div>
                          )}

                        </div>

                      </div>
                    );
                  })}

                </div>

                {/* PIPELINE FOOTER */}

                <div className="mt-7 border-t border-white/[0.07] pt-5">

                  {isCompleted ? (
                    <div className="flex items-center gap-3 rounded-xl border border-emerald-400/10 bg-emerald-400/[0.05] p-4">

                      <CheckCircle2
                        size={21}
                        className="shrink-0 text-emerald-300"
                      />

                      <div>
                        <p className="text-sm font-medium text-emerald-300">
                          Research pipeline completed
                        </p>

                        <p className="mt-1 text-xs text-gray-500">
                          The simulated research stages have finished.
                        </p>
                      </div>

                    </div>
                  ) : (
                    <div className="flex items-center gap-3 rounded-xl border border-white/[0.05] bg-white/[0.02] p-4">

                      <Clock3
                        size={20}
                        className="shrink-0 text-gray-500"
                      />

                      <p className="text-xs leading-5 text-gray-500">
                        {isRunning
                          ? "The demo is advancing through each stage."
                          : "Start the demo to watch the pipeline progress."}
                      </p>

                    </div>
                  )}

                </div>

              </div>

            </section>

            {/* ========================================= */}
            {/* FINAL REPORT PREVIEW */}
            {/* ========================================= */}

            <section className="mt-10">

              <div className="mb-5">

                <h2 className="text-lg font-semibold text-white">
                  Final Research Report
                </h2>

                <p className="mt-2 text-sm text-gray-500">
                  Preview the report section that becomes available
                  after the pipeline finishes.
                </p>

              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#101522] p-6 sm:p-8">

                {!isCompleted ? (
                  <div className="py-8 text-center">

                    <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-indigo-400/10 bg-indigo-500/10 text-indigo-300">

                      <FileText size={25} />

                    </div>

                    <h3 className="mt-5 font-medium text-white">
                      Report not ready yet
                    </h3>

                    <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-gray-500">
                      Complete the demo pipeline to reveal the
                      sample report preview.
                    </p>

                  </div>
                ) : (
                  <div>

                    <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">

                      <div className="flex items-center gap-3">

                        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-400/10 text-emerald-300">

                          <FileText size={22} />

                        </div>

                        <div>

                          <h3 className="font-semibold text-white">
                            Research Report
                          </h3>

                          <p className="mt-1 text-xs text-gray-500">
                            Demo preview · Markdown report
                          </p>

                        </div>

                      </div>

                      <span className="inline-flex items-center gap-2 self-start rounded-full bg-emerald-400/10 px-3 py-1.5 text-xs text-emerald-300">

                        <CheckCircle2 size={14} />

                        Generated in demo
                      </span>

                    </div>

                    <div className="mt-7 border-t border-white/[0.07] pt-6">

                      <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-indigo-300">

                        <Sparkles size={14} />

                        Executive Summary
                      </div>

                      <h4 className="mt-4 text-xl font-semibold text-white">
                        YOLO-Based Traffic Management
                      </h4>

                      <p className="mt-4 text-sm leading-7 text-gray-400">
                        Object detection models can support traffic
                        monitoring by identifying vehicles and
                        road users in video streams. A research
                        system can compare detection accuracy,
                        inference speed, and performance under
                        different traffic and environmental conditions.
                      </p>

                      <div className="mt-5 rounded-xl border border-amber-400/10 bg-amber-400/[0.04] p-4">

                        <p className="text-xs leading-6 text-amber-200/80">
                          This is illustrative demo text, not the
                          report generated by your Python backend.
                          The real report will be loaded from your
                          saved Markdown output when backend
                          integration is implemented.
                        </p>

                      </div>

                    </div>

                  </div>
                )}

              </div>

            </section>

            {/* ========================================= */}
            {/* FOOTER */}
            {/* ========================================= */}

            <footer className="mt-12 border-t border-white/[0.06] py-6 text-center text-xs text-gray-600">

              Research Studio · Research Workspace

            </footer>

          </div>
        </main>
      </div>
    </div>
  );
}