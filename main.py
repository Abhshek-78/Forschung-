from pathlib import Path
import sys

from graph.workflow import (
    build_research_graph
)


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(
    report: str,
    topic: str
):

    output_dir = Path(
        "outputs"
    )

    output_dir.mkdir(
        exist_ok=True
    )

    safe_topic = "".join(

        character
        if character.isalnum()
        else "_"

        for character in topic
    )

    filename = (
        output_dir
        / f"{safe_topic[:80]}"
        "_research_report.md"
    )

    filename.write_text(
        report,
        encoding="utf-8"
    )

    return filename


# ============================================================
# MAIN
# ============================================================

def main():

    # Windows terminals may default to cp1252, which cannot print the
    # status symbols used throughout the pipeline.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(
            encoding="utf-8",
            errors="replace"
        )

    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(
            encoding="utf-8",
            errors="replace"
        )

    print("\n")

    print(
        "=" * 70
    )

    print(
        "MULTI-AGENT AI RESEARCH SYSTEM"
    )

    print(
        "=" * 70
    )

    topic = input(
        "\nEnter a research topic: "
    ).strip()

    if not topic:

        print(
            "\nResearch topic "
            "cannot be empty."
        )

        return

    # --------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------

    initial_state = {

        "topic": topic,

        "papers": [],

        "corpus": [],

        "evidence_chunks": [],

        "research_draft": "",

        "critic_feedback": "",

        "final_report": "",

        "errors": []
    }

    # --------------------------------------------------------
    # BUILD GRAPH
    # --------------------------------------------------------

    try:

        graph = (
            build_research_graph()
        )

    except Exception as exc:

        print(
            "\n Could not build "
            f"research graph: {exc}"
        )

        return

    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    try:

        final_state = graph.invoke(
            initial_state
        )

    except Exception as exc:

        print("\n")
        print(
            "=" * 70
        )

        print(
            " RESEARCH PIPELINE FAILED"
        )

        print(
            "=" * 70
        )

        print(
            f"\nError: {exc}"
        )

        return

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n")

    print(
        "=" * 70
    )

    print(
        "RESEARCH PIPELINE COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        "\nTopic:",
        final_state.get(
            "topic",
            topic
        )
    )

    print(
        "Papers found:",
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
        "Evidence chunks:",
        len(
            final_state.get(
                "evidence_chunks",
                []
            )
        )
    )

    print(
        "Draft generated:",
        bool(
            final_state.get(
                "research_draft"
            )
        )
    )

    print(
        "Critic review generated:",
        bool(
            final_state.get(
                "critic_feedback"
            )
        )
    )

    print(
        "Final report generated:",
        bool(
            final_state.get(
                "final_report"
            )
        )
    )

    errors = final_state.get(
        "errors",
        []
    )

    print(
        "Errors:",
        len(errors)
    )

    # --------------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------------

    final_report = (
        final_state.get(
            "final_report",
            ""
        )
    )

    if final_report:

        try:

            report_path = save_report(
                final_report,
                topic
            )

            print(
                "\n✓ Final research paper "
                "saved to:"
            )

            print(
                f"  {report_path}"
            )

        except Exception as exc:

            print(
                "\n⚠ Could not save report:"
                f" {exc}"
            )

    # --------------------------------------------------------
    # DISPLAY ERRORS
    # --------------------------------------------------------

    if errors:

        print("\n")

        print(
            "=" * 70
        )

        print(
            "PIPELINE ERRORS"
        )

        print(
            "=" * 70
        )

        for error in errors:

            print(
                f"\n⚠ {error}"
            )

    # --------------------------------------------------------
    # DISPLAY FINAL REPORT
    # --------------------------------------------------------

    if final_report:

        print("\n")

        print(
            "=" * 70
        )

        print(
            "FINAL RESEARCH PAPER"
        )

        print(
            "=" * 70
        )

        print("\n")

        print(
            final_report
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()