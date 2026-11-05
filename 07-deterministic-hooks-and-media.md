# 7. Deterministic Hooks and Media Protocol

## Hooks over prompts

Prompts are probabilistic — the model might skip a rule. Hooks are deterministic — the harness always runs them.

Use hooks for mandatory rules: "always do X when Y" belongs in a hook, not in a prompt.

## PDF extraction

Native PDF read costs 1,500–3,000 tokens per page. When you only need the text:

```bash
python scripts/extract_pdf.py document.pdf output.txt
```

Requires `pypdf` (`pip install pypdf`). The script extracts text page by page, reports blank pages, and exits with code 3 if the PDF is image-only (needs OCR instead).

## Screenshot OCR

Screenshots of text, logs or code should be OCR'd locally, not sent to the vision model:

```bash
python scripts/extract_image_ocr.py screenshot.png output.txt
```

Requires `tesseract` installed and in PATH. Uses Italian + English by default.

## Visual exception

When charts, UI mockups or diagrams need to be **seen** (not just read as text), use the model's native image reading. The scripts above are only for text content in images.
