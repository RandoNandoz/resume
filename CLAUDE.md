# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is Randy Zhu's personal resume repository. The primary artifact is a LaTeX resume (`Randy_Zhu_resume.tex`) compiled to PDF. The repo also contains cover letters and a cover letter generation tool.

## Building the Resume

Use `build.py` — it reads `build.yaml` and handles grad-date variants and anonymized builds.

```bash
./build.py              # build default variant → Randy_Zhu_resume.pdf
./build.py anon         # anonymized variant → Randy_Zhu_resume_anon.pdf
./build.py dec2027      # December 2027 grad date
./build.py --all        # build every variant in build.yaml
./build.py --list       # show all variant names and settings
```

Variants and the redaction map (real company names → anonymized placeholders) are configured in `build.yaml`. The `.tex` source is never modified; a substituted copy is written to `.build/` (gitignored) and compiled there.

The `with-footer/main.tex` is a variant of the resume that includes a co-op footer image. Build it with `latexmk -pdf main.tex` from within that directory.

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
