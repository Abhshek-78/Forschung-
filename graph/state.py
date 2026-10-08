from typing import TypedDict, List, Dict, Any


class ResearchState(TypedDict, total=False):
    # Research topic entered by the user
    topic: str

    # Papers discovered by academic search
    papers: List[Dict[str, Any]]

    # Extracted PDF corpus
    corpus: List[Dict[str, Any]]

    # Page-aware evidence chunks
    evidence_chunks: List[Dict[str, Any]]

    # First research draft
    research_draft: str

    # Critic's evaluation
    critic_feedback: str

    # Final revised research paper
    final_report: str

    # Pipeline errors
    errors: List[str]