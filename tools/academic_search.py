import arxiv
from semanticscholar import SemanticScholar
import requests

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
def search_crossref_papers(query, max_results=3):

    print("\nSearching Crossref as an academic fallback...")

    url = "https://api.crossref.org/works"

    params = {
        "query": query,
        "rows": max_results,
        "select": "DOI,title,author,published,URL,abstract",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=12,
            headers={
                "User-Agent": "ForschungResearchSystem/1.0"
            },
        )

        response.raise_for_status()

        items = response.json().get(
            "message", {}
        ).get("items", [])

        papers = []

        for item in items:

            titles = item.get("title", [])

            if not titles:
                continue

            authors = []

            for author in item.get("author", []):
                name = " ".join(
                    part for part in [
                        author.get("given", ""),
                        author.get("family", "")
                    ] if part
                )

                if name:
                    authors.append(name)

            date_parts = (
                item.get("published", {}).get("date-parts", [[]])
            )

            year = (
                date_parts[0][0]
                if date_parts and date_parts[0]
                else None
            )

            paper_url = item.get("URL", "")

            papers.append({
                "title": titles[0],
                "authors": authors,
                "year": year,
                "abstract": item.get("abstract", ""),
                "source": "crossref",
                "paper_url": paper_url,
                "pdf_url": "",
            })

        print(f"Crossref papers found: {len(papers)}")

        return papers

    except Exception as exc:

        print(f"Crossref search failed: {exc}")

        return []

def search_openalex_papers(query, max_results=3):

    print("\nSearching OpenAlex as an academic fallback...")

    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": max_results,
        "select": (
            "id,doi,title,publication_year,authorships,"
            "primary_location,open_access"
        ),
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=12,
        )

        response.raise_for_status()

        items = response.json().get("results", [])

        papers = []

        for item in items:

            title = item.get("title")

            if not title:
                continue

            authors = []

            for authorship in item.get("authorships", []):

                author = authorship.get("author", {})

                name = author.get("display_name")

                if name:
                    authors.append(name)

            paper_url = item.get("doi") or item.get("id", "")

            # Look for a PDF in the primary location.
            primary_location = item.get(
                "primary_location"
            ) or {}

            source_info = primary_location.get("source") or {}

            landing_page = primary_location.get(
                "landing_page_url"
            ) or ""

            pdf_url = (
                primary_location.get("pdf_url")
                or ""
            )

            # Fall back to an open-access PDF URL if available.
            if not pdf_url:
                oa_info = item.get("open_access") or {}
                pdf_url = oa_info.get("oa_url") or ""

            papers.append({
                "title": title,
                "authors": authors,
                "year": item.get("publication_year"),
                "abstract": "",
                "source": "openalex",
                "paper_url": paper_url or landing_page,
                "pdf_url": pdf_url,
            })

        print(f"OpenAlex papers found: {len(papers)}")

        return papers

    except Exception as exc:

        print(f"OpenAlex search failed: {exc}")

        return []