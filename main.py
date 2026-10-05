from graph.workflow import build_research_graph


def main():

    print("\n")
    print("=" * 70)
    print("MULTI-AGENT AI RESEARCH SYSTEM")
    print("=" * 70)

    topic = input(
        "\nEnter a research topic: "
    ).strip()

    if not topic:

        print(
            "\nResearch topic cannot be empty."
        )

        return

    # --------------------------------------------------------
    # Build LangGraph
    # --------------------------------------------------------

    graph = build_research_graph()

    # --------------------------------------------------------
    # Initial state
    # --------------------------------------------------------

    initial_state = {

        "topic": topic,

        "papers": [],

        "corpus": [],

        "errors": []
    }

    # --------------------------------------------------------
    # Execute graph
    # --------------------------------------------------------

    final_state = graph.invoke(
        initial_state
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RESEARCH PIPELINE COMPLETE")
    print("=" * 70)

    print(
        "\nTopic:",
        final_state.get(
            "topic",
            topic
        )
    )

    print(
        "\nPapers found:",
        len(
            final_state.get(
                "papers",
                []
            )
        )
    )

    print(
        "Papers successfully read:",
        len(
            final_state.get(
                "corpus",
                []
            )
        )
    )

    print(
        "Errors:",
        len(
            final_state.get(
                "errors",
                []
            )
        )
    )

    # --------------------------------------------------------
    # Print errors
    # --------------------------------------------------------

    errors = final_state.get(
        "errors",
        []
    )

    if errors:

        print("\n")
        print("=" * 70)
        print("ERRORS / SKIPPED PAPERS")
        print("=" * 70)

        for error in errors:

            print(
                f"\n- {error}"
            )

    # --------------------------------------------------------
    # Print paper summary
    # --------------------------------------------------------

    papers = final_state.get(
        "papers",
        []
    )

    if papers:

        print("\n")
        print("=" * 70)
        print("PAPER SUMMARY")
        print("=" * 70)

        for index, paper in enumerate(
            papers,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{paper.get('title', 'Unknown')}"
            )

            print(
                f"   Source: "
                f"{paper.get('source', 'Unknown')}"
            )

            print(
                f"   Year: "
                f"{paper.get('year', 'Unknown')}"
            )

            print(
                f"   URL: "
                f"{paper.get('paper_url', 'N/A')}"
            )


if __name__ == "__main__":
    main()