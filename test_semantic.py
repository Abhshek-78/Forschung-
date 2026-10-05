from tools.academic_search import (
    search_semantic_scholar_papers
)


def main():

    query = "large language models healthcare"

    papers = search_semantic_scholar_papers(
        query,
        max_results=5
    )

    print("\n")
    print("=" * 70)
    print("SEMANTIC SCHOLAR RESULTS")
    print("=" * 70)

    for index, paper in enumerate(
        papers,
        start=1
    ):

        print(
            f"\n{index}. {paper['title']}"
        )

        print(
            f"Authors: "
            f"{', '.join(paper['authors'])}"
        )

        print(
            f"Year: "
            f"{paper['year']}"
        )

        print(
            f"URL: "
            f"{paper['paper_url']}"
        )


if __name__ == "__main__":
    main()