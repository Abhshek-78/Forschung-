# Multi-Agent AI Research System

An AI-powered academic research pipeline built with **Python, LangGraph, LangChain, and Groq**. It searches multiple academic sources, extracts text from available PDFs, processes the text into evidence chunks, generates a research draft, reviews it, and prepares a final report.

> **Project status:** The pipeline is designed to continue when an individual search provider fails. Actual results depend on source availability, PDF access, and the configured LLM API.

## Features

- **Multi-source academic search**
  - arXiv
  - Semantic Scholar
  - Crossref
  - OpenAlex
- **PDF text extraction** using PyMuPDF.
- **Evidence processing** with text cleaning and overlapping chunks.
- **Multi-agent workflow** orchestrated by LangGraph:
  1. Academic Search
  2. Paper Reader
  3. Evidence Processor
  4. Writer
  5. Critic
  6. Revision
- **Groq-hosted language model** through LangChain's `ChatGroq` integration.
- **Markdown report output** in the `outputs/` directory.
- **Graceful handling** of many search, download, and processing errors.

## How the workflow works

```text
Research topic
     |
     v
Academic Search
(arXiv, Semantic Scholar, Crossref, OpenAlex)
     |
     v
Paper Reader
(download PDFs and extract text)
     |
     v
Evidence Processor
(clean, split, and label text chunks)
     |
     v
Writer Agent
(create a draft from available evidence)
     |
     v
Critic Agent
(check the draft against the evidence)
     |
     v
Revision Agent
     |
     v
Final Markdown report
(outputs/)
```

## Project structure

```text
Forschung-/
├── main.py
├── .env                     # API keys; do not commit this file
├── .gitignore
├── graph/
│   ├── __init__.py
│   ├── state.py             # LangGraph state definition
│   ├── nodes.py             # Workflow node implementations
│   └── workflow.py          # Graph construction
├── tools/
│   ├── __init__.py
│   ├── academic_search.py   # Academic source integrations
│   ├── pdf_reader.py        # PDF download and text extraction
│   └── evidence_processor.py
├── llm/
│   ├── __init__.py
│   ├── groq_model.py        # Groq model configuration
│   └── research_chains.py   # Writer, critic, and revision chains
├── outputs/                 # Generated reports
└── README.md
```

> The tree describes the intended layout. Keep your actual filenames if they differ, and ensure imports match them.

## Requirements

- Python 3.10 or newer (use a Python version supported by your installed dependencies).
- Internet access to query academic APIs and download publicly accessible PDFs.
- A Groq API key for the language-model stages.
- A Windows PowerShell terminal or another Python-compatible terminal.

## Setup on Windows (PowerShell)

### 1. Open the project directory

```powershell
cd "E:\Forschung-"
```

### 2. Create and activate a virtual environment

If you already have the project's `venv`, you can skip environment creation.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the Python executable directly instead:



### 3. Install dependencies

Install the packages used by the project:

```powershell
python -m pip install --upgrade pip
python -m pip install langgraph langchain langchain-core langchain-groq python-dotenv requests arxiv pymupdf
```

If your project uses additional packages, install those too. Once the project runs successfully, consider recording the exact environment:

```powershell
python -m pip freeze > requirements.txt
```

On future setups, install the recorded dependencies with:

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root (next to `main.py`) and add:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own key. **Do not share your API key or commit `.env` to Git.**

The model configuration in `llm/groq_model.py` should read `GROQ_API_KEY` and use a model available to your Groq account. For example, the current project configuration may use:

```python
GROQ_MODEL = "openai/gpt-oss-120b"
```

Model availability, request limits, and account quotas can change. If Groq returns a model or rate-limit error, verify the model ID and limits in the official Groq documentation.

## Run the system

From the project root:

```powershell
& "E:\Forschung-\venv\Scripts\python.exe" "E:\Forschung-\main.py"
```

When prompted, enter a research topic, for example:

```text
real time speech translation automatic speech recognition
```

The program should search for papers, attempt to read available PDFs, process extracted evidence, and run the writing/review stages when enough evidence is available.

## Output

Generated Markdown reports should be saved in:

```text
outputs/
```

The report filename may be based on the research topic. Check the terminal summary for:

- Number of papers discovered.
- Number of papers successfully read.
- Number of evidence chunks created.
- Whether the draft, critic review, and final report were generated.
- Any recorded errors.

## Important notes and limitations

### Academic search APIs

- **Semantic Scholar may return HTTP 429.** This generally indicates rate limiting. The system should log a warning and continue with other sources when possible.
- Search providers may return overlapping, irrelevant, incomplete, or metadata-only records. Deduplication by title does not guarantee that every result is relevant.
- Crossref and OpenAlex records do not always include an abstract or direct PDF link.
- A paper landing page is not necessarily a direct PDF URL.

### PDF extraction

- Only records with a usable PDF URL can be downloaded by the PDF reader.
- Some publishers block automated downloads or require authentication.
- Scanned PDFs may contain no extractable text unless OCR is added.
- A PDF download can fail because of network issues, invalid links, server restrictions, or timeouts.

### Evidence and generated reports

- If no PDFs are readable, the evidence processor may produce zero chunks and the writer may skip generation. This is expected behavior when evidence is unavailable; it is not a successful research report.
- The writer, critic, and revision agents depend on the LLM API and its current request/token limits.
- Always verify important claims and citations against the original papers. AI-generated output can contain mistakes and should not be treated as a substitute for reviewing the sources.
- A source listed in the report should be checked to ensure it supports the associated claim.

## Troubleshooting

### `NameError: name 'ResearchState' is not defined` in `tools/pdf_reader.py`

`ResearchState` belongs in the LangGraph state/node layer, not in the PDF utility. Make sure `tools/pdf_reader.py` contains only PDF-reading logic and does not have an annotation such as `state: ResearchState`.

### `read_pdf() missing 1 required positional argument: 'title'`

The reader function expects both a PDF URL and a title. In `graph/nodes.py`, call it with both arguments:

```python
text = read_pdf(pdf_url, title)
```

Check the actual function signature with:

```powershell
& "E:\Forschung-\venv\Scripts\python.exe" -c "from tools.pdf_reader import read_pdf; import inspect; print(inspect.signature(read_pdf))"
```

### `Semantic Scholar HTTP error: 429`

This is usually a rate-limit response. Continue using the other sources, reduce repeated requests, and retry later. Do not make Semantic Scholar the only source in the pipeline.

### Groq HTTP 413 or token/request-size errors

Reduce the amount of evidence passed to the model, shorten prompts, and keep the Writer, Critic, and Revision evidence limits appropriate for your account's model limits. A character limit is only an approximation of token count.

### `ModuleNotFoundError`

Activate the intended virtual environment and install the missing package into that same environment:

```powershell
& "E:\Forschung-\venv\Scripts\python.exe" -m pip install <package-name>
```

Replace `<package-name>` with the missing dependency's package name.

### No PDFs found or `Evidence chunks generated: 0`

Inspect the search results' `pdf_url` fields. Some sources provide only landing pages. Try a more specific topic, check whether the paper is open access, and confirm that `paper_reader_node()` passes both `pdf_url` and `title` to `read_pdf()`.

## Security

- Keep `.env` and all API keys private.
- Do not commit virtual environments, caches, temporary downloads, or generated files unless intentionally required.
- Add at least the following to `.gitignore`:


If you want generated reports tracked in Git, remove `outputs/` from `.gitignore`.

## Future improvements

Potential next steps:

- Improve relevance ranking and remove figure captions or low-quality metadata records.
- Add retries with exponential backoff and respect provider `Retry-After` headers.
- Add OCR for scanned PDFs.
- Store paper metadata and evidence with stable source identifiers and DOI links.
- Generate a bibliography and trace each report claim to evidence chunks.
- Add automated tests for search normalization, PDF extraction, chunking, and workflow behavior.
- Add structured logging and a run summary with source-level statistics.

## License

