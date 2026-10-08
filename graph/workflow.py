from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import ResearchState

from graph.nodes import (
    academic_search_node,
    paper_reader_node,
    evidence_processor_node
)


def build_research_graph():

    graph = StateGraph(
        ResearchState
    )

    # ========================================================
    # NODES
    # ========================================================

    graph.add_node(
        "academic_search",
        academic_search_node
    )

    graph.add_node(
        "paper_reader",
        paper_reader_node
    )

    graph.add_node(
        "evidence_processor",
        evidence_processor_node
    )

    # ========================================================
    # EDGES
    # ========================================================

    graph.add_edge(
        START,
        "academic_search"
    )

    graph.add_edge(
        "academic_search",
        "paper_reader"
    )

    graph.add_edge(
        "paper_reader",
        "evidence_processor"
    )

    graph.add_edge(
        "evidence_processor",
        END
    )

    # ========================================================
    # COMPILE
    # ========================================================

    return graph.compile()