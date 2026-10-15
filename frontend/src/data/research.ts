export interface ResearchProject {
  id: string;
  topic: string;
  papersFound: number;
  papersRead: number;
  evidenceChunks: number;
  status: "completed" | "running" | "failed";
  errors: number;
  reportPath?: string;
}

export const researchProjects: ResearchProject[] = [
  {
    id: "research-001",
    topic: "How to Apply YOLO in Traffic Management",
    papersFound: 9,
    papersRead: 6,
    evidenceChunks: 102,
    status: "completed",
    errors: 0,
    reportPath:
      "outputs/how_to_apply_yolo_in_trafic_management_research_report.md",
  },
];