import arxiv
import requests


# ============================================================
# COMMON CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = 15

USER_AGENT = (
    "ForschungResearchSystem/1.0 "
    "(academic-research-pipeline)"
)


# ============================================================
# ARXIV SEARCH
# ============================================================

def search_arxiv_papers(
    query: str,
    max_results: int = 5
):

    print("\nSearching arXiv...")

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

                "abstract": (
                    paper.summary or ""
                ),

                "source": "arxiv",

                "paper_url": (
                    paper.entry_id or ""
                ),

                "pdf_url": (
                    paper.pdf_url or ""
                )
            })

    except Exception as exc:

        print(
            f"⚠ arXiv error: {exc}"
        )

        return []

    print(
        f"✓ arXiv completed: "
        f"{len(papers)} papers"
    )

    return papers


# ============================================================
# SEMANTIC SCHOLAR SEARCH
#
# Uses the official REST API directly.
# If Semantic Scholar is unavailable, return [].
# The caller will continue with Crossref/OpenAlex.
# ============================================================

def search_semantic_scholar_papers(
    query: str,
    max_results: int = 5
):

    print(
        "\nSearching Semantic Scholar..."
    )

    url = (
        "https://api.semanticscholar.org/"
        "graph/v1/paper/search"
    )

    params = {

        "query": query,

        "limit": max_results,

        "fields": (
            "title,"
            "authors,"
            "year,"
            "abstract,"
            "url,"
            "openAccessPdf"
        )
    }

    try:

        response = requests.get(

            url,

            params=params,

            timeout=REQUEST_TIMEOUT,

            headers={
                "User-Agent": USER_AGENT
            }
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "data",
            []
        )

        papers = []

        for paper in results:

            authors = []

            for author in (
                paper.get("authors")
                or []
            ):

                name = author.get(
                    "name"
                )

                if name:
                    authors.append(name)

            open_access_pdf = (
                paper.get(
                    "openAccessPdf"
                )
                or {}
            )

            pdf_url = (
                open_access_pdf.get(
                    "url"
                )
                or ""
            )

            papers.append({

                "title": (
                    paper.get("title")
                    or "Unknown"
                ),

                "authors": authors,

                "year": paper.get(
                    "year"
                ),

                "abstract": (
                    paper.get(
                        "abstract"
                    )
                    or ""
                ),

                "source":
                    "semantic_scholar",

                "paper_url": (
                    paper.get("url")
                    or ""
                ),

                "pdf_url": pdf_url
            })

        print(
            "✓ Semantic Scholar completed: "
            f"{len(papers)} papers"
        )

        return papers

    except requests.exceptions.Timeout:

        print(
            "⚠ Semantic Scholar timeout."
        )

        return []

    except requests.exceptions.ConnectionError:

        print(
            "⚠ Semantic Scholar connection "
            "failed."
        )

        return []

    except requests.exceptions.HTTPError as exc:

        print(
            "⚠ Semantic Scholar HTTP error: "
            f"{exc}"
        )

        return []

    except Exception as exc:

        print(
            "⚠ Semantic Scholar failed: "
            f"{exc}"
        )

        return []


# ============================================================
# CROSSREF SEARCH
#
# Fallback academic metadata source.
# ============================================================

def search_crossref_papers(
    query: str,
    max_results: int = 3
):

    print(
        "\nSearching Crossref..."
    )

    url = (
        "https://api.crossref.org/works"
    )

    params = {

        "query": query,

        "rows": max_results,

        "select": (
            "DOI,title,author,"
            "published,URL,abstract"
        )
    }

    try:

        response = requests.get(

            url,

            params=params,

            timeout=REQUEST_TIMEOUT,

            headers={
                "User-Agent": USER_AGENT
            }
        )

        response.raise_for_status()

        data = response.json()

        items = (
            data
            .get("message", {})
            .get("items", [])
        )

        papers = []

        for item in items:

            titles = item.get(
                "title",
                []
            )

            if not titles:
                continue

            authors = []

            for author in (
                item.get("author")
                or []
            ):

                name_parts = [

                    author.get(
                        "given",
                        ""
                    ),

                    author.get(
                        "family",
                        ""
                    )
                ]

                name = " ".join(
                    part
                    for part in name_parts
                    if part
                )

                if name:
                    authors.append(name)

            date_parts = (
                item
                .get("published", {})
                .get("date-parts", [[]])
            )

            year = None

            if (
                date_parts
                and date_parts[0]
            ):

                year = date_parts[0][0]

            papers.append({

                "title": titles[0],

                "authors": authors,

                "year": year,

                "abstract": (
                    item.get(
                        "abstract"
                    )
                    or ""
                ),

                "source": "crossref",

                "paper_url": (
                    item.get("URL")
                    or ""
                ),

                # Crossref normally does
                # not provide direct PDF URLs.
                "pdf_url": ""
            })

        print(
            f"✓ Crossref completed: "
            f"{len(papers)} papers"
        )

        return papers

    except requests.exceptions.Timeout:

        print(
            "⚠ Crossref timeout."
        )

        return []

    except requests.exceptions.ConnectionError:

        print(
            "⚠ Crossref connection failed."
        )

        return []

    except requests.exceptions.HTTPError as exc:

        print(
            f"⚠ Crossref HTTP error: {exc}"
        )

        return []

    except Exception as exc:

        print(
            f"⚠ Crossref failed: {exc}"
        )

        return []


# ============================================================
# OPENALEX SEARCH
#
# Fallback academic source.
# ============================================================

def search_openalex_papers(
    query: str,
    max_results: int = 3
):

    print(
        "\nSearching OpenAlex..."
    )

    url = (
        "https://api.openalex.org/works"
    )

    params = {

        "search": query,

        "per-page": max_results,

        "select": (
            "id,"
            "doi,"
            "title,"
            "publication_year,"
            "authorships,"
            "primary_location,"
            "open_access"
        )
    }

    try:

        response = requests.get(

            url,

            params=params,

            timeout=REQUEST_TIMEOUT,

            headers={
                "User-Agent": USER_AGENT
            }
        )

        response.raise_for_status()

        data = response.json()

        items = data.get(
            "results",
            []
        )

        papers = []

        for item in items:

            title = item.get(
                "title"
            )

            if not title:
                continue

            authors = []

            for authorship in (
                item.get(
                    "authorships"
                )
                or []
            ):

                author = (
                    authorship.get(
                        "author"
                    )
                    or {}
                )

                name = author.get(
                    "display_name"
                )

                if name:
                    authors.append(name)

            primary_location = (
                item.get(
                    "primary_location"
                )
                or {}
            )

            landing_page = (
                primary_location.get(
                    "landing_page_url"
                )
                or ""
            )

            pdf_url = (
                primary_location.get(
                    "pdf_url"
                )
                or ""
            )

            if not pdf_url:

                open_access = (
                    item.get(
                        "open_access"
                    )
                    or {}
                )

                pdf_url = (
                    open_access.get(
                        "oa_url"
                    )
                    or ""
                )

            doi = (
                item.get("doi")
                or ""
            )

            paper_url = (
                doi
                or landing_page
                or item.get(
                    "id",
                    ""
                )
            )

            papers.append({

                "title": title,

                "authors": authors,

                "year": item.get(
                    "publication_year"
                ),

                "abstract": "",

                "source": "openalex",

                "paper_url": paper_url,

                "pdf_url": pdf_url
            })

        print(
            f"✓ OpenAlex completed: "
            f"{len(papers)} papers"
        )

        return papers

    except requests.exceptions.Timeout:

        print(
            "⚠ OpenAlex timeout."
        )

        return []

    except requests.exceptions.ConnectionError:

        print(
            "⚠ OpenAlex connection failed."
        )

        return []

    except requests.exceptions.HTTPError as exc:

        print(
            f"⚠ OpenAlex HTTP error: {exc}"
        )

        return []

    except Exception as exc:

        print(
            f"⚠ OpenAlex failed: {exc}"
        )

        return []


# ============================================================
# COMBINED ACADEMIC SEARCH
#
# IMPORTANT:
# Every source is independent.
#
# If one source fails, the other sources
# still execute.
# ============================================================

def collect_academic_papers(
    topic: str,
    max_results: int = 3
):

    print("\n")
    print("=" * 70)
    print("MULTI-SOURCE ACADEMIC SEARCH")
    print("=" * 70)

    search_functions = [

        (
            "arXiv",
            search_arxiv_papers
        ),

        (
            "Semantic Scholar",
            search_semantic_scholar_papers
        ),

        (
            "Crossref",
            search_crossref_papers
        ),

        (
            "OpenAlex",
            search_openalex_papers
        )
    ]

    all_papers = []

    source_statistics = {}

    # ========================================================
    # SEARCH EACH SOURCE
    # ========================================================

    for source_name, search_function in (
        search_functions
    ):

        print("\n")
        print("-" * 70)
        print(
            f"SOURCE: {source_name}"
        )
        print("-" * 70)

        try:

            results = search_function(

                topic,

                max_results=max_results
            )

            if results:

                all_papers.extend(
                    results
                )

                source_statistics[
                    source_name
                ] = len(results)

                print(
                    f"✓ {source_name}: "
                    f"{len(results)} results"
                )

            else:

                source_statistics[
                    source_name
                ] = 0

                print(
                    f"⚠ {source_name}: "
                    "0 results"
                )

        except Exception as exc:

            source_statistics[
                source_name
            ] = 0

            print(
                f"⚠ {source_name} failed: "
                f"{exc}"
            )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique_papers = []

    seen_titles = set()

    for paper in all_papers:

        title = (
            paper.get(
                "title",
                ""
            )
            .strip()
        )

        if not title:
            continue

        normalized_title = (
            " ".join(
                title.lower().split()
            )
        )

        if normalized_title in seen_titles:
            continue

        seen_titles.add(
            normalized_title
        )

        unique_papers.append(
            paper
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n")
    print("=" * 70)
    print("ACADEMIC SEARCH SUMMARY")
    print("=" * 70)

    for source_name, count in (
        source_statistics.items()
    ):

        print(
            f"{source_name}: {count}"
        )

    print(
        f"\nTotal raw papers: "
        f"{len(all_papers)}"
    )

    print(
        f"Total unique papers: "
        f"{len(unique_papers)}"
    )

    print("=" * 70)

    return unique_papers