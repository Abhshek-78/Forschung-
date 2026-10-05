import os
import re
import requests
import fitz


PAPERS_DIR = "papers"


# ============================================================
# SAFE FILE NAME
# ============================================================

def safe_filename(title: str) -> str:

    filename = re.sub(
        r'[<>:"/\\|?*]',
        "",
        title
    )

    filename = filename.strip()

    if not filename:
        filename = "unknown_paper"

    return filename[:120]


# ============================================================
# DOWNLOAD PDF
# ============================================================

def download_pdf(
    pdf_url: str,
    title: str
) -> str:

    os.makedirs(
        PAPERS_DIR,
        exist_ok=True
    )

    filename = safe_filename(title)

    filepath = os.path.join(
        PAPERS_DIR,
        f"{filename}.pdf"
    )

    response = requests.get(
        pdf_url,
        timeout=60,
        headers={
            "User-Agent":
            "AcademicResearchAgent/1.0"
        }
    )

    response.raise_for_status()

    with open(
        filepath,
        "wb"
    ) as file:

        file.write(
            response.content
        )

    return filepath


# ============================================================
# EXTRACT PDF TEXT
# ============================================================

def extract_pdf_text(
    filepath: str
) -> str:

    document = fitz.open(filepath)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        pages.append(
            f"""
===== PAGE {page_number + 1} =====

{text}
"""
        )

    document.close()

    return "\n".join(pages)


# ============================================================
# DOWNLOAD + EXTRACT
# ============================================================

def read_pdf(
    pdf_url: str,
    title: str
):

    filepath = download_pdf(
        pdf_url,
        title
    )

    text = extract_pdf_text(
        filepath
    )

    return {
        "title": title,
        "pdf_url": pdf_url,
        "pdf_path": filepath,
        "text": text
    }