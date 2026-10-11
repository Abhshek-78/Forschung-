from graph.state import ResearchState

from tools.academic_search import (
    collect_academic_papers
)

from tools.pdf_reader import (
    read_pdf
)

from tools.evidence_processor import (
    process_corpus
)

from llm.research_chains import (
    writer_chain,
    critic_chain,
    revision_chain
)


# ============================================================
# ACADEMIC SEARCH NODE
# ============================================================

def academic_search_node(
    state: ResearchState
) -> ResearchState:

    topic = state.get(
        "topic",
        ""
    )

    print("\n")
    print("=" * 70)
    print("ACADEMIC SEARCH NODE")
    print("=" * 70)

    print(
        f"\nSearching for: {topic}"
    )

    errors = list(
        state.get(
            "errors",
            []
        )
    )

    try:

        papers = collect_academic_papers(
            topic,
            max_results=3
        )

    except Exception as exc:

        print(
            f"\n⚠ Academic search failed: "
            f"{exc}"
        )

        errors.append(
            "Academic search error: "
            f"{str(exc)}"
        )

        papers = []

    print(
        f"\nTotal papers collected: "
        f"{len(papers)}"
    )

    return {

        **state,

        "papers": papers,

        "errors": errors
    }


# ============================================================
# PAPER READER NODE
# ============================================================

def paper_reader_node(
    state: ResearchState
) -> ResearchState:

    papers = state.get(
        "papers",
        []
    )

    print("\n")
    print("=" * 70)
    print("PAPER READER NODE")
    print("=" * 70)

    corpus = []

    errors = list(
        state.get(
            "errors",
            []
        )
    )

    for index, paper in enumerate(
        papers,
        start=1
    ):

        title = paper.get(
            "title",
            "Unknown"
        )

        pdf_url = (
            paper.get(
                "pdf_url"
            )
            or ""
        )

        print(
            f"\n[{index}/{len(papers)}] "
            f"{title}"
        )

        # ----------------------------------------------------
        # No PDF available
        # ----------------------------------------------------

        if not pdf_url:

            print(
                "⚠ No PDF URL available. "
                "Skipping PDF extraction."
            )

            continue

        try:

            text = read_pdf(
                pdf_url,
                title
            )

            if not text:

                print(
                    "⚠ PDF returned no text."
                )

                continue

            corpus.append({

                "title": title,

                "authors": paper.get(
                    "authors",
                    []
                ),

                "year": paper.get(
                    "year"
                ),

                "abstract": paper.get(
                    "abstract",
                    ""
                ),

                "source": paper.get(
                    "source",
                    "unknown"
                ),

                "paper_url": paper.get(
                    "paper_url",
                    ""
                ),

                "pdf_url": pdf_url,

                "text": text
            })

            print(
                "✓ PDF extracted successfully."
            )

        except Exception as exc:

            print(
                f"⚠ PDF extraction failed: "
                f"{exc}"
            )

            errors.append(
                f"PDF extraction failed for "
                f"'{title}': {str(exc)}"
            )

    print(
        f"\nSuccessfully read: "
        f"{len(corpus)} papers"
    )

    return {

        **state,

        "corpus": corpus,

        "errors": errors
    }


# ============================================================
# EVIDENCE PROCESSOR NODE
# ============================================================

def evidence_processor_node(
    state: ResearchState
) -> ResearchState:

    corpus = state.get(
        "corpus",
        []
    )

    print("\n")
    print("=" * 70)
    print("EVIDENCE PROCESSOR NODE")
    print("=" * 70)

    errors = list(
        state.get(
            "errors",
            []
        )
    )

    try:

        evidence_chunks = (
            process_corpus(
                corpus
            )
        )

        print(
            f"\nEvidence chunks generated: "
            f"{len(evidence_chunks)}"
        )

    except Exception as exc:

        print(
            f"⚠ Evidence processing failed: "
            f"{exc}"
        )

        errors.append(
            "Evidence processing error: "
            f"{str(exc)}"
        )

        evidence_chunks = []

    return {

        **state,

        "evidence_chunks":
            evidence_chunks,

        "errors": errors
    }


# ============================================================
# FORMAT EVIDENCE
#
# Prevents huge prompts.
# Never cuts a source in the middle.
# ============================================================

def format_evidence(
    evidence_chunks,
    max_chars=4000
):

    formatted = []

    used_chars = 0

    for chunk in evidence_chunks:

        text = (
            chunk.get(
                "text",
                ""
            )
            .strip()
        )

        if not text:
            continue

        block = (

            "\n--- ACADEMIC SOURCE ---\n"

            f"Title: "
            f"{chunk.get('title', 'Unknown')}\n"

            f"Source: "
            f"{chunk.get('source', 'Unknown')}\n"

            f"Paper URL: "
            f"{chunk.get('paper_url', '')}\n"

            f"PDF URL: "
            f"{chunk.get('pdf_url', '')}\n"

            f"Page: "
            f"{chunk.get('page_number', 'Unknown')}\n"

            f"Chunk ID: "
            f"{chunk.get('chunk_id', 'Unknown')}\n"

            f"Evidence: {text}\n"
        )

        if (
            used_chars
            + len(block)
            > max_chars
        ):

            continue

        formatted.append(
            block
        )

        used_chars += len(
            block
        )

    result = "\n".join(
        formatted
    )

    print(
        f"Evidence selected: "
        f"{len(formatted)} chunks"
    )

    print(
        f"Evidence size: "
        f"{len(result)} characters"
    )

    return result


# ============================================================
# WRITER NODE
# ============================================================

def writer_node(
    state: ResearchState
) -> ResearchState:

    topic = state.get(
        "topic",
        ""
    )

    evidence_chunks = state.get(
        "evidence_chunks",
        []
    )

    print("\n")
    print("=" * 70)
    print("WRITER AGENT")
    print("=" * 70)

    errors = list(
        state.get(
            "errors",
            []
        )
    )

    if not evidence_chunks:

        print(
            "⚠ No evidence available."
        )

        errors.append(
            "Writer skipped: "
            "no evidence available."
        )

        return {

            **state,

            "research_draft": "",

            "errors": errors
        }

    evidence = format_evidence(
        evidence_chunks,
        max_chars=4000
    )

    try:

        print(
            "\nGenerating research draft..."
        )

        draft = writer_chain.invoke({

            "topic": topic,

            "evidence": evidence
        })

        draft = (
            draft
            if isinstance(
                draft,
                str
            )
            else str(draft)
        )

        print(
            f"✓ Draft generated: "
            f"{len(draft)} characters"
        )

        return {

            **state,

            "research_draft":
                draft,

            "errors": errors
        }

    except Exception as exc:

        print(
            f"⚠ Writer failed: "
            f"{exc}"
        )

        errors.append(
            "Writer error: "
            f"{str(exc)}"
        )

        return {

            **state,

            "research_draft": "",

            "errors": errors
        }


# ============================================================
# CRITIC NODE
# ============================================================

def critic_node(
    state: ResearchState
) -> ResearchState:

    topic = state.get(
        "topic",
        ""
    )

    draft = state.get(
        "research_draft",
        ""
    )

    evidence_chunks = state.get(
        "evidence_chunks",
        []
    )

    print("\n")
    print("=" * 70)
    print("CRITIC AGENT")
    print("=" * 70)

    errors = list(
        state.get(
            "errors",
            []
        )
    )

    if not draft:

        print(
            "⚠ No draft available. "
            "Skipping critic."
        )

        return {

            **state,

            "critic_feedback": "",

            "errors": errors
        }

    evidence = format_evidence(
        evidence_chunks,
        max_chars=2000
    )

    try:

        print(
            "\nReviewing research draft..."
        )

        feedback = critic_chain.invoke({

            "topic": topic,

            "draft": draft,

            "evidence": evidence
        })

        feedback = (
            feedback
            if isinstance(
                feedback,
                str
            )
            else str(feedback)
        )

        print(
            f"✓ Critic review generated: "
            f"{len(feedback)} characters"
        )

        return {

            **state,

            "critic_feedback":
                feedback,

            "errors": errors
        }

    except Exception as exc:

        print(
            f"⚠ Critic failed: "
            f"{exc}"
        )

        errors.append(
            "Critic error: "
            f"{str(exc)}"
        )

        return {

            **state,

            "critic_feedback": "",

            "errors": errors
        }


# ============================================================
# REVISION NODE
# ============================================================

def revision_node(
    state: ResearchState
) -> ResearchState:

    topic = state.get(
        "topic",
        ""
    )

    draft = state.get(
        "research_draft",
        ""
    )

    feedback = state.get(
        "critic_feedback",
        ""
    )

    evidence_chunks = state.get(
        "evidence_chunks",
        []
    )

    print("\n")
    print("=" * 70)
    print("REVISION AGENT")
    print("=" * 70)

    errors = list(
        state.get(
            "errors",
            []
        )
    )

    if not draft:

        print(
            "⚠ No draft available. "
            "Skipping revision."
        )

        return {

            **state,

            "final_report": "",

            "errors": errors
        }

    if not feedback:

        print(
            "⚠ No critic feedback. "
            "Using draft as final report."
        )

        return {

            **state,

            "final_report":
                draft,

            "errors": errors
        }

    evidence = format_evidence(
        evidence_chunks,
        max_chars=1500
    )

    try:

        print(
            "\nRevising research paper..."
        )

        final_report = (
            revision_chain.invoke({

                "topic": topic,

                "draft": draft,

                "feedback": feedback,

                "evidence": evidence
            })
        )

        final_report = (
            final_report
            if isinstance(
                final_report,
                str
            )
            else str(final_report)
        )

        print(
            f"✓ Final report generated: "
            f"{len(final_report)} characters"
        )

        return {

            **state,

            "final_report":
                final_report,

            "errors": errors
        }

    except Exception as exc:

        print(
            f"⚠ Revision failed: "
            f"{exc}"
        )

        errors.append(
            "Revision error: "
            f"{str(exc)}"
        )

        # ----------------------------------------------------
        # Important fallback:
        # If revision fails but draft exists,
        # don't lose the entire research paper.
        # ----------------------------------------------------

        return {

            **state,

            "final_report":
                draft,

            "errors": errors
        }