#!/usr/bin/env python3
"""Resume build tool: named variants with grad-date and anonymization support."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.resolve()
SOURCE_TEX = REPO_ROOT / "Randy_Zhu_resume.tex"
BUILD_DIR = REPO_ROOT / ".build"
CONFIG_FILE = REPO_ROOT / "build.yaml"


def load_config() -> dict:
    with CONFIG_FILE.open() as f:
        return yaml.safe_load(f)


def apply_redactions(content: str, redactions: dict[str, str]) -> str:
    for key in sorted(redactions, key=len, reverse=True):
        content = content.replace(key, redactions[key])
    return content


def verify_redactions(content: str, redactions: dict[str, str]) -> None:
    missed = [k for k in redactions if k in content]
    if missed:
        sys.exit(
            "ERROR: Redaction incomplete — these strings still appear in the output:\n  "
            + "\n  ".join(missed)
        )


def run_pdflatex(tex_code: str, output: str, verbose: bool = False) -> None:
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={BUILD_DIR}",
        f"-jobname={output}",
        tex_code,
    ]
    pipe = None if verbose else subprocess.DEVNULL
    result = subprocess.run(cmd, cwd=REPO_ROOT, stdout=pipe, stderr=pipe)
    if result.returncode != 0 and not (BUILD_DIR / f"{output}.pdf").exists():
        log = BUILD_DIR / f"{output}.log"
        hint = f" (see {log} for details)" if log.exists() else ""
        sys.exit(f"ERROR: pdflatex failed for '{output}'{hint}")


def build_variant(name: str, variant: dict, redactions: dict[str, str], verbose: bool = False) -> None:
    output = variant.get("output", name)
    graddate = variant.get("graddate", "April 2028")
    anonymize = variant.get("anonymize", False)

    BUILD_DIR.mkdir(exist_ok=True)

    source = SOURCE_TEX.read_text()
    if anonymize:
        source = apply_redactions(source, redactions)
        verify_redactions(source, redactions)

    tmp_tex = BUILD_DIR / f"{output}.tex"
    tmp_tex.write_text(source)

    # \newcommand pre-defines \graddate before \input reads the source, so
    # the \providecommand in the .tex file becomes a no-op — grad date wins.
    tex_code = rf"\newcommand{{\graddate}}{{{graddate}}}\input{{{tmp_tex}}}"

    run_pdflatex(tex_code, output, verbose)

    built_pdf = BUILD_DIR / f"{output}.pdf"
    dest_pdf = REPO_ROOT / f"{output}.pdf"
    shutil.move(str(built_pdf), str(dest_pdf))
    print(f"  → {dest_pdf.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build resume variants defined in build.yaml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  ./build.py              # build default variant\n"
            "  ./build.py anon         # build anonymized variant\n"
            "  ./build.py dec2027 anon # build two variants\n"
            "  ./build.py --all        # build all variants\n"
            "  ./build.py --list       # show available variants"
        ),
    )
    parser.add_argument("variants", nargs="*", metavar="VARIANT")
    parser.add_argument("--all", action="store_true", help="build every variant")
    parser.add_argument("--list", action="store_true", help="list available variants")
    parser.add_argument("--verbose", "-v", action="store_true", help="show pdflatex output")
    args = parser.parse_args()

    config = load_config()
    all_variants: dict = config.get("variants", {})
    redactions: dict = config.get("redactions", {})
    default_name: str = config.get("default", next(iter(all_variants), ""))

    if args.list:
        for vname, vcfg in all_variants.items():
            parts = [f"output={vcfg.get('output', vname)}", f"graddate={vcfg.get('graddate', '')}"]
            if vcfg.get("anonymize"):
                parts.append("anonymize=true")
            marker = " [default]" if vname == default_name else ""
            print(f"  {vname}{marker}: {', '.join(parts)}")
        return

    if args.all:
        targets = list(all_variants.keys())
    elif args.variants:
        targets = args.variants
    else:
        targets = [default_name]

    for name in targets:
        if name not in all_variants:
            sys.exit(f"ERROR: Unknown variant '{name}'. Run ./build.py --list for options.")
        print(f"Building [{name}]")
        build_variant(name, all_variants[name], redactions, args.verbose)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
