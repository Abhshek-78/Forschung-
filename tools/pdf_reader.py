import requests
import pymupdf


def read_pdf(pdf_url: str, title: str) -> str:
    """
    Download a PDF from pdf_url and extract its text.

    Args:
        pdf_url: Direct URL of the PDF.
        title: Paper title, used for logging/file naming.

    Returns:
        Extracted PDF text as a string.
    """

    if not pdf_url:
        raise ValueError("PDF URL is empty.")

    print(f"Downloading PDF: {title}")

    try:
        response = requests.get(
            pdf_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        raise RuntimeError("PDF download timed out.")

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"PDF download failed: {exc}")

    pdf_bytes = response.content

    if not pdf_bytes:
        raise RuntimeError("Downloaded PDF is empty.")

    try:
        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

    except Exception as exc:
        raise RuntimeError(
            f"Could not open downloaded PDF: {exc}"
        )

    pages = []

    try:
        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text")

            if text and text.strip():

                pages.append(
                    f"===== PAGE {page_number} =====\n"
                    f"{text.strip()}"
                )

    finally:
        document.close()

    if not pages:
        raise RuntimeError(
            "PDF was opened successfully, but no text could be extracted."
        )

    extracted_text = "\n\n".join(pages)

    print(
        f"✓ Extracted {len(pages)} pages "
        f"({len(extracted_text)} characters)"
    )

    return extracted_text