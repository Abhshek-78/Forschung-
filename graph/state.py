from typing import TypedDict, List, Dict, Any


class ResearchState(TypedDict, total=False):
    """
    Shared state passed between all LangGraph nodes.
    """

    # --------------------------------------------------------
    # USER INPUT
    # --------------------------------------------------------

    topic: str

    # --------------------------------------------------------
    # ACADEMIC SEARCH RESULTS
    # --------------------------------------------------------

    papers: List[Dict[str, Any]]

    # --------------------------------------------------------
    # FULL PDF CORPUS
    # --------------------------------------------------------

    corpus: List[Dict[str, Any]]

    # --------------------------------------------------------
    # PAGE-AWARE EVIDENCE CHUNKS
    # --------------------------------------------------------

    evidence_chunks: List[Dict[str, Any]]

    # --------------------------------------------------------
    # ERRORS
    # --------------------------------------------------------

    errors: List[str]