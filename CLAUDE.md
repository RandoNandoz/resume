# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is Randy Zhu's personal resume repository. The primary artifact is a LaTeX resume (`Randy_Zhu_resume.tex`) compiled to PDF. The repo also contains cover letters and a cover letter generation tool.

## Building the Resume

```bash
# Compile to PDF (preferred — handles multiple passes automatically)
latexmk -pdf Randy_Zhu_resume.tex

# Or with pdflatex directly
pdflatex Randy_Zhu_resume.tex

# Clean auxiliary build files
latexmk -c
```

The `with-footer/main.tex` is a variant of the resume that includes a co-op footer image. Build it the same way from within that directory.

## LaTeX Structure

The `.tex` file defines custom commands used throughout:

| Command | Purpose |
|---|---|
| `\resumeSubheading{org}{date}{role}{location}` | Job/education entry header |
| `\resumeSubSubheading{subtitle}{date}` | Secondary line under a subheading (e.g., coursework) |
| `\resumeProjectHeading{title \| tech}{date}` | Project entry header |
| `\resumeItem{text}` | Single bullet point |
| `\resumeItemListStart` / `\resumeItemListEnd` | Wraps bullet lists |
| `\resumeSubHeadingListStart` / `\resumeSubHeadingListEnd` | Wraps all entries in a section |

The document sections in order: Heading → Technical Skills → Experience → Projects.

## Cover Letter Generation (`Cover Letters 2026S/`)

A Python tool generates an LLM prompt from Randy's existing cover letters to write new ones in his voice. See `Cover Letters 2026S/CLAUDE.md` for full details.

```bash
cd "Cover Letters 2026S"
source .venv/bin/activate
python generate_cover_letter_prompt.py
```

Output goes to `cover_letter_prompt_claude.md`.
