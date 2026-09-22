#!/usr/bin/env python3
"""Extract text, tables, or metadata from a PDF."""

import argparse
import csv
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber is required: pip install pdfplumber")


def parse_pages(spec, total):
    """Turn '1,4,7-9' into a sorted list of 0-indexed page numbers."""
    if not spec:
        return list(range(total))
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = (int(n) for n in part.split("-", 1))
        else:
            start = end = int(part)
        if start < 1 or end > total or start > end:
            sys.exit(f"page range '{part}' is out of bounds (document has {total} pages)")
        pages.update(range(start - 1, end))
    return sorted(pages)


def cmd_text(pdf, pages, out):
    chunks = []
    for i in pages:
        text = pdf.pages[i].extract_text() or ""
        chunks.append(f"--- page {i + 1} ---\n{text}")
    body = "\n\n".join(chunks)
    if out:
        Path(out).write_text(body, encoding="utf-8")
        print(f"wrote {len(body)} chars to {out}")
    else:
        print(body)
    if not body.replace("-", "").strip():
        print(
            "\nwarning: no embedded text found — this PDF is likely scanned images "
            "and needs OCR (e.g. ocrmypdf)",
            file=sys.stderr,
        )


def cmd_tables(pdf, pages, out):
    out_dir = Path(out or ".")
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for i in pages:
        for n, table in enumerate(pdf.pages[i].extract_tables(), start=1):
            path = out_dir / f"page{i + 1}_table{n}.csv"
            with path.open("w", newline="", encoding="utf-8") as fh:
                writer = csv.writer(fh)
                writer.writerows([[c if c is not None else "" for c in row] for row in table])
            print(f"wrote {path} ({len(table)} rows)")
            count += 1
    if not count:
        print("no tables detected on the requested pages", file=sys.stderr)


def cmd_meta(pdf, pages, out):
    print(f"pages: {len(pdf.pages)}")
    for key, value in (pdf.metadata or {}).items():
        print(f"{key}: {value}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["text", "tables", "meta"])
    parser.add_argument("pdf")
    parser.add_argument("--pages", help="e.g. 3, 2-5, or 1,4,7-9 (1-indexed)")
    parser.add_argument("--out", help="output file (text) or directory (tables)")
    args = parser.parse_args()

    path = Path(args.pdf)
    if not path.is_file():
        sys.exit(f"not a file: {path}")

    handler = {"text": cmd_text, "tables": cmd_tables, "meta": cmd_meta}[args.mode]
    with pdfplumber.open(path) as pdf:
        handler(pdf, parse_pages(args.pages, len(pdf.pages)), args.out)


if __name__ == "__main__":
    main()
