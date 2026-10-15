export interface ResearchProject {
  id: string;
  topic: string;
  papersFound: number;
  papersRead: number;
  evidenceChunks: number;
  status: "completed" | "running" | "failed";
  errors: number;
  reportPath?: string | null;
  pdfPath?: string | null;
  createdAt?: string;
  error?: string;
}

interface ResearchResponse {
  projects: ResearchProject[];
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "/api";

export async function fetchResearchProjects(): Promise<ResearchProject[]> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/research`);
  } catch {
    throw new Error(
      "Research backend is not running. In another terminal run: npm run backend",
    );
  }
  if (!response.ok) {
    throw new Error(`Could not load research projects (${response.status})`);
  }
  const data = (await response.json()) as ResearchResponse;
  return data.projects;
}

export async function createResearch(topic: string): Promise<{ id: string }> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/research`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
  } catch {
    throw new Error(
      "Research backend is not running. In another terminal run: npm run backend",
    );
  }
  const data = (await response.json()) as { id?: string; error?: string };
  if (!response.ok || !data.id) {
    throw new Error(data.error ?? "Could not start research");
  }

  return { id: data.id };
}

export function researchReportUrl(id: string) {
  return `${API_BASE_URL}/research/${id}/report`;
}

export function researchPdfUrl(id: string) {
  return `${API_BASE_URL}/research/${id}/report.pdf`;
}
