import arxiv
from semanticscholar import SemanticScholar


# ============================================================
# arXiv SEARCH
# ============================================================

def search_arxiv_papers(
    query: str,
    max_results: int = 5
):
    """
    Search arXiv for academic papers.

    Returns structured paper metadata.
    """

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

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

    return papers


# ============================================================
# SEMANTIC SCHOLAR SEARCH
# ============================================================

def search_semantic_scholar_papers(
    query: str,
    max_results: int = 5
):
    """
    Search Semantic Scholar for academic papers.

    Returns structured paper metadata.
    """

    scholar = SemanticScholar()

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

    return papers