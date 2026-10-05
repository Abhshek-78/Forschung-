from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import ResearchState

from graph.nodes import (
    academic_search_node,
    paper_reader_node
)


# ============================================================
# BUILD RESEARCH GRAPH
# ============================================================

def build_research_graph():

    graph = StateGraph(
        ResearchState
    )

    # --------------------------------------------------------
    # Add Nodes
    # --------------------------------------------------------

    graph.add_node(
        "academic_search",
        academic_search_node
    )

    graph.add_node(
        "paper_reader",
        paper_reader_node
    )

    # --------------------------------------------------------
    # Define Flow
    # --------------------------------------------------------

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
        END
    )

    # --------------------------------------------------------
    # Compile
    # --------------------------------------------------------

    return graph.compile()