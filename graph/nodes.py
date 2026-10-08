from tools.academic_search import (
    search_arxiv_papers,
    search_semantic_scholar_papers,
    search_crossref_papers,
    search_openalex_papers,
)
from llm.research_chains import (
    writer_chain,
    critic_chain,
    revision_chain
)

from tools.pdf_reader import read_pdf
from tools.evidence_processor import process_corpus
from graph.state import ResearchState


def academic_search_node(
    state: ResearchState
) -> ResearchState:

    topic = state["topic"]

    print("\n")
    print("=" * 70)
    print("ACADEMIC SEARCH NODE")
    print("=" * 70)

    print(
        f"\nSearching for: {topic}\n"
    )

    errors = state.get(
        "errors",
        []
    )

    papers = []

    # --------------------------------------------------------
    # arXiv
    # --------------------------------------------------------

    try:

        arxiv_papers = search_arxiv_papers(
            topic,
            max_results=3
        )

        print(
            f"arXiv papers found: "
            f"{len(arxiv_papers)}"
        )

        papers.extend(
            arxiv_papers
        )

    except Exception as e:

        print(
            f"arXiv search failed: {e}"
        )

        errors.append(
            f"arXiv search error: {str(e)}"
        )

    # --------------------------------------------------------
    # Semantic Scholar
    # --------------------------------------------------------

    try:

        semantic_papers = (
            search_semantic_scholar_papers(
                topic,
                max_results=3
            )
        )

        print(
            "Semantic Scholar papers found: "
            f"{len(semantic_papers)}"
        )

        papers.extend(
            semantic_papers
        )

    except Exception as e:

        print(
            f"Semantic Scholar search failed: {e}"
        )

        errors.append(
            f"Semantic Scholar search error: {str(e)}"
        )

    print(
        f"Total papers collected: "
        f"{len(papers)}"
    )

    return {
        **state,
        "papers": papers,
        "errors": errors
    }


def paper_reader_node(
    state: ResearchState
) -> ResearchState:

    print("\n")
    print("=" * 70)
    print("PAPER READER NODE")
    print("=" * 70)

    papers = state.get(
        "papers",
        []
    )

    corpus = []

    errors = state.get(
        "errors",
        []
    )

    for index, paper in enumerate(
        papers
    ):

        print(
            f"\nReading paper "
            f"{index + 1}/{len(papers)}"
        )

        title = paper.get(
            "title",
            "Unknown Paper"
        )

        pdf_url = paper.get(
            "pdf_url"
        )

        print(
            f"Title: {title}"
        )

        if not pdf_url:

            print(
                "No PDF URL available. Skipping."
            )

            errors.append(
                f"{title}: PDF URL unavailable"
            )

            continue

        try:

            result = read_pdf(
                pdf_url,
                title
            )

            corpus.append({

                "title": title,

                "source": paper.get(
                    "source"
                ),

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

                "paper_url": paper.get(
                    "paper_url"
                ),

                "pdf_url": pdf_url,

                "pdf_path": result[
                    "pdf_path"
                ],

                "text": result[
                    "text"
                ]
            })

            print(
                "PDF successfully extracted."
            )

        except Exception as e:

            print(
                f"Failed to read paper: {e}"
            )

            errors.append(
                f"{title}: {str(e)}"
            )

    print(
        f"\nSuccessfully extracted: "
        f"{len(corpus)} papers"
    )

    return {
        **state,
        "corpus": corpus,
        "errors": errors
    }

def collect_academic_papers(topic, max_results=3):

    papers = []

    search_functions = [
        ("arXiv", search_arxiv_papers),
        ("Semantic Scholar", search_semantic_scholar_papers),
        ("Crossref", search_crossref_papers),
        ("OpenAlex", search_openalex_papers),
    ]

    for source_name, search_function in search_functions:

        try:

            print(f"\nSearching {source_name}...")

            results = search_function(
                topic,
                max_results=max_results,
            )

            if results:
                papers.extend(results)

                print(
                    f"{source_name} returned "
                    f"{len(results)} papers."
                )

            else:
                print(
                    f"{source_name} returned no papers."
                )

        except Exception as exc:

            print(
                f"{source_name} failed: {exc}"
            )

    # Deduplicate papers by normalized title.
    unique_papers = []
    seen_titles = set()

    for paper in papers:

        title = paper.get("title", "").strip()

        if not title:
            continue

        normalized_title = " ".join(
            title.lower().split()
        )

        if normalized_title in seen_titles:
            continue

        seen_titles.add(normalized_title)
        unique_papers.append(paper)

    print(
        f"\nTotal unique academic papers: "
        f"{len(unique_papers)}"
    )

    return unique_papers
# ============================================================
# EVIDENCE PROCESSOR NODE
# ============================================================

def evidence_processor_node(
    state: ResearchState
) -> ResearchState:

    print("\n")
    print("=" * 70)
    print("EVIDENCE PROCESSOR NODE")
    print("=" * 70)

    corpus = state.get(
        "corpus",
        []
    )

    if not corpus:

        print(
            "\n⚠ No extracted papers available."
        )

        return {
            **state,
            "evidence_chunks": []
        }

    print(
        f"\nProcessing "
        f"{len(corpus)} papers..."
    )

    evidence_chunks = process_corpus(
        corpus
    )

    print(
        f"✓ Evidence processing completed."
    )

    print(
        f"✓ Total evidence chunks: "
        f"{len(evidence_chunks)}"
    )

    # --------------------------------------------------------
    # Show a small preview
    # --------------------------------------------------------

    if evidence_chunks:

        print("\nEvidence Preview:")

        for chunk in evidence_chunks[:3]:

            print(
                "\n--------------------------------------------------"
            )

            print(
                f"Chunk ID: "
                f"{chunk['chunk_id']}"
            )

            print(
                f"Paper: "
                f"{chunk['title']}"
            )

            print(
                f"Page: "
                f"{chunk['page_number']}"
            )

            print(
                f"Text: "
                f"{chunk['text'][:300]}..."
            )

    return {
        **state,
        "evidence_chunks": evidence_chunks
    }
def format_evidence(evidence_chunks, max_chars=6000):
    """
    Prepare a compact, source-aware evidence collection.

    Limits the prompt size while preserving source metadata.
    The input is already extracted academic evidence.
    """

    formatted = []
    used_chars = 0

    # Keep the evidence in its existing order.
    for chunk in evidence_chunks:

        text = chunk.get("text", "").strip()

        if not text:
            continue

        block = (
            f"\n--- ACADEMIC SOURCE ---\n"
            f"Title: {chunk.get('title', 'Unknown')}\n"
            f"Source: {chunk.get('source', 'Unknown')}\n"
            f"Paper URL: {chunk.get('paper_url', '')}\n"
            f"PDF URL: {chunk.get('pdf_url', '')}\n"
            f"Page: {chunk.get('page_number', 'Unknown')}\n"
            f"Chunk ID: {chunk.get('chunk_id', 'Unknown')}\n"
            f"Evidence: {text}\n"
        )

        remaining = max_chars - used_chars

        if remaining <= 0:
            break

        # Avoid exceeding the evidence character budget.
        if len(block) > remaining:
            if remaining > 300:
                block = block[:remaining]
                formatted.append(block)

            break

        formatted.append(block)
        used_chars += len(block)

    result = "\n".join(formatted)

    print(f"Evidence selected: {len(formatted)} chunks")
    print(f"Evidence size: {len(result)} characters")

    return result

def writer_node(state: ResearchState) -> ResearchState:

    print("\n")
    print("=" * 70)
    print("WRITER AGENT")
    print("=" * 70)

    topic = state.get("topic", "")
    evidence_chunks = state.get("evidence_chunks", [])

    if not evidence_chunks:
        print("\n⚠ No evidence available for writing.")

        return {
            **state,
            "research_draft": "",
            "errors": state.get("errors", []) + [
                "Writer received no evidence chunks."
            ]
        }

    print(f"\nResearch topic: {topic}")
    print(f"Evidence chunks available: {len(evidence_chunks)}")

    print("\nGenerating research draft with GroqCloud...")

    evidence = format_evidence(evidence_chunks)

    try:

        draft = writer_chain.invoke(
            {
                "topic": topic,
                "evidence": evidence
            }
        )

        print("\n✓ Research draft generated.")
        print(f"✓ Draft length: {len(draft)} characters")

        return {
            **state,
            "research_draft": draft
        }

    except Exception as exc:

        print(f"\n⚠ Writer failed: {exc}")

        return {
            **state,
            "research_draft": "",
            "errors": state.get("errors", []) + [
                f"Writer error: {str(exc)}"
            ]
        }
def critic_node(state: ResearchState) -> ResearchState:

    print("\n")
    print("=" * 70)
    print("CRITIC AGENT")
    print("=" * 70)

    topic = state.get("topic", "")
    draft = state.get("research_draft", "")
    evidence_chunks = state.get("evidence_chunks", [])

    if not draft:
        print("\n⚠ No research draft available.")

        return {
            **state,
            "critic_feedback": "",
            "errors": state.get("errors", []) + [
                "Critic received no research draft."
            ]
        }

    print("\nReviewing research draft...")
    print(f"Evidence chunks available: {len(evidence_chunks)}")

    evidence = format_evidence(evidence_chunks)

    try:

        feedback = critic_chain.invoke(
            {
                "topic": topic,
                "evidence": evidence,
                "draft": draft
            }
        )

        print("\n✓ Academic review completed.")
        print(f"✓ Review length: {len(feedback)} characters")

        return {
            **state,
            "critic_feedback": feedback
        }

    except Exception as exc:

        print(f"\n⚠ Critic failed: {exc}")

        return {
            **state,
            "critic_feedback": "",
            "errors": state.get("errors", []) + [
                f"Critic error: {str(exc)}"
            ]
        }
def revision_node(state: ResearchState) -> ResearchState:

    print("\n")
    print("=" * 70)
    print("REVISION AGENT")
    print("=" * 70)

    topic = state.get("topic", "")
    draft = state.get("research_draft", "")
    critique = state.get("critic_feedback", "")
    evidence_chunks = state.get("evidence_chunks", [])

    if not draft:
        print("\n⚠ No draft available for revision.")

        return {
            **state,
            "final_report": "",
            "errors": state.get("errors", []) + [
                "Revision received no research draft."
            ]
        }

    if not critique:
        print("\n⚠ No critic feedback available.")

        return {
            **state,
            "final_report": draft
        }

    print("\nRevising research paper using critic feedback...")

    evidence = format_evidence(evidence_chunks)

    try:

        final_report = revision_chain.invoke(
            {
                "topic": topic,
                "evidence": evidence,
                "draft": draft,
                "critique": critique
            }
        )

        print("\n✓ Final research paper generated.")
        print(
            f"✓ Final report length: "
            f"{len(final_report)} characters"
        )

        return {
            **state,
            "final_report": final_report
        }

    except Exception as exc:

        print(f"\n⚠ Revision failed: {exc}")

        return {
            **state,
            "final_report": draft,
            "errors": state.get("errors", []) + [
                f"Revision error: {str(exc)}"
            ]
        }