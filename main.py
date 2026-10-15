from pathlib import Path
import sys
import argparse
import json
import threading
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import fitz

from graph.workflow import (
    build_research_graph
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
RUNS_FILE = OUTPUT_DIR / "research_runs.json"
RUNS_LOCK = threading.Lock()


def load_runs():
    if not RUNS_FILE.exists():
        return []
    try:
        return json.loads(RUNS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []


def save_runs(runs):
    OUTPUT_DIR.mkdir(exist_ok=True)
    RUNS_FILE.write_text(
        json.dumps(runs, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def project_path(path):
    candidate = Path(path)
    return candidate if candidate.is_absolute() else BASE_DIR / candidate


def run_pipeline(topic, run_id):
    run = {
        "id": run_id,
        "topic": topic,
        "status": "running",
        "papersFound": 0,
        "papersRead": 0,
        "evidenceChunks": 0,
        "errors": 0,
        "reportPath": None,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    with RUNS_LOCK:
        runs = load_runs()
        save_runs([run] + [item for item in runs if item["id"] != run_id])

    initial_state = {
        "topic": topic,
        "papers": [],
        "corpus": [],
        "evidence_chunks": [],
        "research_draft": "",
        "critic_feedback": "",
        "final_report": "",
        "errors": [],
    }

    try:
        final_state = build_research_graph().invoke(initial_state)
        final_report = final_state.get("final_report", "")
        report_path = save_report(final_report, topic) if final_report else None
        pdf_path = save_pdf(final_report, topic) if final_report else None
        run.update({
            "status": "completed" if final_report else "failed",
            "papersFound": len(final_state.get("papers", [])),
            "papersRead": len(final_state.get("corpus", [])),
            "evidenceChunks": len(final_state.get("evidence_chunks", [])),
            "errors": len(final_state.get("errors", [])),
            "reportPath": str(report_path) if report_path else None,
            "pdfPath": str(pdf_path) if pdf_path else None,
        })
    except Exception as exc:
        run.update({"status": "failed", "errors": 1, "error": str(exc)})

    with RUNS_LOCK:
        runs = load_runs()
        save_runs([run] + [item for item in runs if item["id"] != run_id])


class ResearchAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json(200, {"status": "ok"})
            return
        if path == "/api/research":
            with RUNS_LOCK:
                self._send_json(200, {"projects": load_runs()})
            return
        if path.startswith("/api/research/"):
            parts = path.split("/")
            if len(parts) == 5 and parts[4] in {"report", "report.pdf"}:
                run_id = parts[3]
                with RUNS_LOCK:
                    run = next((item for item in load_runs() if item["id"] == run_id), None)
                if not run:
                    self._send_json(404, {"error": "Research run not found"})
                    return
                relative_path = run.get("reportPath" if parts[4] == "report" else "pdfPath")
                file_path = project_path(relative_path) if relative_path else None
                if parts[4] == "report.pdf" and (file_path is None or not file_path.exists()):
                    markdown_path = project_path(run.get("reportPath", ""))
                    if markdown_path.exists():
                        file_path = save_pdf(
                            markdown_path.read_text(encoding="utf-8"),
                            run["topic"],
                        )
                        run["pdfPath"] = str(file_path.relative_to(BASE_DIR))
                        with RUNS_LOCK:
                            runs = load_runs()
                            save_runs([
                                run if item["id"] == run_id else item
                                for item in runs
                            ])
                if file_path is None:
                    self._send_json(404, {"error": "Report is not available yet"})
                    return
                if not file_path.exists():
                    self._send_json(404, {"error": "Report file is missing"})
                    return
                content_type = "text/markdown; charset=utf-8" if parts[4] == "report" else "application/pdf"
                body = file_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header(
                    "Content-Disposition",
                    f'{"inline" if parts[4] == "report" else "attachment"}; filename="{file_path.name}"',
                )
                self.end_headers()
                self.wfile.write(body)
                return
        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/research":
            self._send_json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            topic = str(payload.get("topic", "")).strip()
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "Request body must be valid JSON"})
            return
        if not topic:
            self._send_json(400, {"error": "Research topic cannot be empty"})
            return
        run_id = f"research-{uuid.uuid4().hex[:10]}"
        threading.Thread(
            target=run_pipeline,
            args=(topic, run_id),
            daemon=True,
        ).start()
        self._send_json(202, {"id": run_id, "status": "running"})

    def log_message(self, format, *args):
        print(f"[api] {format % args}")


def run_api_server(host="127.0.0.1", port=8000):
    ThreadingHTTPServer.allow_reuse_address = True
    try:
        server = ThreadingHTTPServer((host, port), ResearchAPIHandler)
    except OSError as exc:
        raise RuntimeError(
            f"Could not start the research API on {host}:{port}. "
            "The port may already be in use. Stop the existing backend "
            "process and try again."
        ) from exc
    print(f"Research API running at http://{host}:{port}")
    print("Use Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Research API.")
    finally:
        server.server_close()


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(
    report: str,
    topic: str
):

    output_dir = OUTPUT_DIR

    output_dir.mkdir(
        exist_ok=True
    )

    safe_topic = "".join(

        character
        if character.isalnum()
        else "_"

        for character in topic
    )

    filename = (
        output_dir
        / f"{safe_topic[:80]}"
        "_research_report.md"
    )

    filename.write_text(
        report,
        encoding="utf-8"
    )

    return filename


def save_pdf(report: str, topic: str):
    output_dir = OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    safe_topic = "".join(character if character.isalnum() else "_" for character in topic)
    filename = output_dir / f"{safe_topic[:80]}_research_report.pdf"
    document = fitz.open()
    page = document.new_page()
    y = 48
    for line in report.splitlines() or [topic]:
        if y > 760:
            page = document.new_page()
            y = 48
        page.insert_text((48, y), line[:110], fontsize=10)
        y += 15
    document.save(filename)
    document.close()
    return filename


# ============================================================
# MAIN
# ============================================================

def configure_console():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def main():
    configure_console()
    parser = argparse.ArgumentParser(description="Forschung research pipeline")
    parser.add_argument(
        "--server",
        "--api",
        action="store_true",
        help="Run the HTTP API for the frontend instead of the interactive CLI",
    )
    args = parser.parse_args()

    if args.server:
        run_api_server()
        return

    print("\n")

    print(
        "=" * 70
    )

    print(
        "MULTI-AGENT AI RESEARCH SYSTEM"
    )

    print(
        "=" * 70
    )

    topic = input(
        "\nEnter a research topic: "
    ).strip()

    if not topic:

        print(
            "\nResearch topic "
            "cannot be empty."
        )

        return

    # --------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------

    initial_state = {

        "topic": topic,

        "papers": [],

        "corpus": [],

        "evidence_chunks": [],

        "research_draft": "",

        "critic_feedback": "",

        "final_report": "",

        "errors": []
    }

    # --------------------------------------------------------
    # BUILD GRAPH
    # --------------------------------------------------------

    try:

        graph = (
            build_research_graph()
        )

    except Exception as exc:

        print(
            "\n Could not build "
            f"research graph: {exc}"
        )

        return

    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    try:

        final_state = graph.invoke(
            initial_state
        )

    except Exception as exc:

        print("\n")
        print(
            "=" * 70
        )

        print(
            " RESEARCH PIPELINE FAILED"
        )

        print(
            "=" * 70
        )

        print(
            f"\nError: {exc}"
        )

        return

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n")

    print(
        "=" * 70
    )

    print(
        "RESEARCH PIPELINE COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        "\nTopic:",
        final_state.get(
            "topic",
            topic
        )
    )

    print(
        "Papers found:",
        len(
            final_state.get(
                "papers",
                []
            )
        )
    )

    print(
        "Papers successfully read:",
        len(
            final_state.get(
                "corpus",
                []
            )
        )
    )

    print(
        "Evidence chunks:",
        len(
            final_state.get(
                "evidence_chunks",
                []
            )
        )
    )

    print(
        "Draft generated:",
        bool(
            final_state.get(
                "research_draft"
            )
        )
    )

    print(
        "Critic review generated:",
        bool(
            final_state.get(
                "critic_feedback"
            )
        )
    )

    print(
        "Final report generated:",
        bool(
            final_state.get(
                "final_report"
            )
        )
    )

    errors = final_state.get(
        "errors",
        []
    )

    print(
        "Errors:",
        len(errors)
    )

    # --------------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------------

    final_report = (
        final_state.get(
            "final_report",
            ""
        )
    )

    if final_report:

        try:

            report_path = save_report(
                final_report,
                topic
            )

            print(
                "\n✓ Final research paper "
                "saved to:"
            )

            print(
                f"  {report_path}"
            )

        except Exception as exc:

            print(
                "\n⚠ Could not save report:"
                f" {exc}"
            )

    # --------------------------------------------------------
    # DISPLAY ERRORS
    # --------------------------------------------------------

    if errors:

        print("\n")

        print(
            "=" * 70
        )

        print(
            "PIPELINE ERRORS"
        )

        print(
            "=" * 70
        )

        for error in errors:

            print(
                f"\n⚠ {error}"
            )

    # --------------------------------------------------------
    # DISPLAY FINAL REPORT
    # --------------------------------------------------------

    if final_report:

        print("\n")

        print(
            "=" * 70
        )

        print(
            "FINAL RESEARCH PAPER"
        )

        print(
            "=" * 70
        )

        print("\n")

        print(
            final_report
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()