from tools.academic_search import (
    search_arxiv_papers,
    search_semantic_scholar_papers
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