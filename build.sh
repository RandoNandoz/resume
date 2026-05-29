#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

build() {
  local date="$1"
  local outname="$2"
  local texcode="\newcommand{\graddate}{$date}\input{Randy_Zhu_resume}"
  pdflatex -interaction=nonstopmode -jobname="$outname" "$texcode"
  pdflatex -interaction=nonstopmode -jobname="$outname" "$texcode"
}

build "December 2027" "Randy_Zhu_resume_dec2027"
build "April 2028"    "Randy_Zhu_resume_apr2028"

# Clean aux files
for base in Randy_Zhu_resume_dec2027 Randy_Zhu_resume_apr2028; do
  rm -f "${base}.aux" "${base}.log" "${base}.out" "${base}.fls" "${base}.fdb_latexmk"
done
