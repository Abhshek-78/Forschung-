from typing import TypedDict, List, Dict, Any


class ResearchState(TypedDict, total=False):
    """
    Shared state passed between all nodes
    in the LangGraph research workflow.
    """

    # User's research topic
    topic: str

    # Papers discovered by academic search
    papers: List[Dict[str, Any]]

    # Full extracted text from PDFs
    corpus: List[Dict[str, Any]]

    # Errors encountered during the workflow
    errors: List[str]