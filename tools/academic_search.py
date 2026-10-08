import arxiv
from semanticscholar import SemanticScholar


# ============================================================
# ARXIV SEARCH
# ============================================================

def search_arxiv_papers(
    query: str,
    max_results: int = 5
):

    print("\n[1/2] Searching arXiv...")

    client = arxiv.Client(
        page_size=max_results,
        delay_seconds=1,
        num_retries=2
    )

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    try:

        for paper in client.results(search):

            papers.append({
                "title": paper.title,
                "authors": [
                    str(author)
                    for author in paper.authors
                ],
                "year": (
                    paper.published.year
                    if paper.published
                    else None
                ),
                "abstract": paper.summary,
                "source": "arxiv",
                "paper_url": paper.entry_id,
                "pdf_url": paper.pdf_url
            })

    except Exception as e:

        print(
            f"arXiv error: {e}"
        )

        raise

    print(
        f"✓ arXiv completed: "
        f"{len(papers)} papers"
    )

    return papers


# ============================================================
# SEMANTIC SCHOLAR SEARCH
# ============================================================

def search_semantic_scholar_papers(
    query: str,
    max_results: int = 5
):

    print("\n[2/2] Searching Semantic Scholar...")

    try:

        scholar = SemanticScholar(
            timeout=10
        )

        results = scholar.search_paper(
            query,
            limit=max_results
        )

        papers = []

        for paper in results:

            authors = []

            if paper.authors:

                authors = [
                    author.name
                    for author in paper.authors
                    if author.name
                ]

            papers.append({
                "title": paper.title,
                "authors": authors,
                "year": paper.year,
                "abstract": paper.abstract or "",
                "source": "semantic_scholar",
                "paper_url": paper.url,
                "pdf_url": None
            })

        print(
            f"✓ Semantic Scholar completed: "
            f"{len(papers)} papers"
        )

        return papers

    except Exception as e:

        print(
            f"⚠ Semantic Scholar failed: {e}"
        )

        # Don't crash the whole research pipeline.
        return []