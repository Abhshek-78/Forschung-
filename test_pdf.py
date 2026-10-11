from tools.pdf_reader import read_pdf


def main():

    pdf_url = input(
        "Enter an arXiv PDF URL: "
    ).strip()

    title = input(
        "Enter paper title: "
    ).strip()

    result = read_pdf(
        pdf_url,
        title
    )

    print("\n")
    print("=" * 70)
    print("PDF TEST RESULT")
    print("=" * 70)

    print(
        "\nExtracted characters:",
        len(result)
    )

    print("\n")
    print("=" * 70)
    print("FIRST 5000 CHARACTERS")
    print("=" * 70)

    print(
        result[:5000]
    )


if __name__ == "__main__":
    main()