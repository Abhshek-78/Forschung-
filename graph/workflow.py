from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState

from graph.nodes import (
    academic_search_node,
    paper_reader_node,
    evidence_processor_node,
    writer_node,
    critic_node,
    revision_node
)


def build_research_graph():

    graph = StateGraph(ResearchState)

    # -----------------------------------------------------
    # Nodes
    # -----------------------------------------------------

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

    graph.add_node(
        "writer",
        writer_node
    )

    graph.add_node(
        "critic",
        critic_node
    )

    graph.add_node(
        "revision",
        revision_node
    )

    # -----------------------------------------------------
    # Workflow
    # -----------------------------------------------------

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
        "writer"
    )

    graph.add_edge(
        "writer",
        "critic"
    )

    graph.add_edge(
        "critic",
        "revision"
    )

    graph.add_edge(
        "revision",
        END
    )

    return graph.compile()