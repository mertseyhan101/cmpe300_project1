#!/bin/bash
# Build submission/<No>.zip for both students and validate each from a clean extraction.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
OUT=$ROOT/submission
rm -rf "$OUT"; mkdir -p "$OUT"
VARIANT="Variant: 4 (p_a=2/5, p_b=2/5, p_c=1/5, d=2)"
for NO in 2023400213 2023400039; do
  D="$OUT/$NO"; mkdir -p "$D"
  cp report/main.pdf "$D/$NO.pdf"
  cp src/2023400213.py "$D/$NO.py"
  sed -e "s/@PROGRAM@/$NO.py/g" -e "s/@REPORT@/$NO.pdf/g" scripts/ReadMe.in > "$D/ReadMe"
  ! grep -q "@" "$D/ReadMe" || { echo "FAIL unrendered placeholder in ReadMe"; exit 1; }
  cp "workdone/${NO}_WorkDone.pdf" "$D/${NO}_WorkDone.pdf"
  (cd "$D" && zip -q -X "$OUT/$NO.zip" "$NO.pdf" "$NO.py" ReadMe "${NO}_WorkDone.pdf")
  rm -rf "$D"
  # ---- validation from a clean extraction ----
  T=$(mktemp -d)
  (cd "$T" && unzip -q "$OUT/$NO.zip")
  LIST=$(cd "$T" && ls | sort | tr '\n' ' ')
  EXP=$(printf '%s\n' "$NO.pdf" "$NO.py" ReadMe "${NO}_WorkDone.pdf" | sort | tr '\n' ' ')
  [[ "$LIST" == "$EXP" ]] || { echo "FAIL $NO contents: $LIST"; exit 1; }
  for f in "$NO.pdf" "${NO}_WorkDone.pdf"; do pdfinfo "$T/$f" > /dev/null || { echo "FAIL pdf $f"; exit 1; }; done
  OUTC=$(cd "$T" && python3 "$NO.py" 2023400213 2023400039 --count abcabcba)
  [[ "$OUTC" == "$VARIANT"$'\n'"Count(1): 13 Count(2): 14 Count(3): 10 Count(4): 61" ]] || { echo "FAIL count mode $NO"; exit 1; }
  OUTR=$(cd "$T" && python3 "$NO.py" 2023400213 2023400039 --count aabcbba)
  echo "$NO count-mode sample: $(echo "$OUTR" | tail -1)"
  NLINES=$(cd "$T" && python3 "$NO.py" 2023400213 2023400039 | tee "$OUT/${NO}_normal_mode_check.txt" | grep -c "^Case: ")
  [[ "$NLINES" == 45 ]] || { echo "FAIL normal mode $NO ($NLINES case lines)"; exit 1; }
  head -1 "$OUT/${NO}_normal_mode_check.txt" | grep -qx "$VARIANT" || { echo "FAIL variant line $NO"; exit 1; }
  # ---- run every command documented in the ReadMe literally (except the <string> template line) ----
  NCMD=0
  while IFS= read -r CMD; do
    NCMD=$((NCMD+1))
    if [[ "$CMD" == *"--count"* ]]; then
      GOT=$(cd "$T" && eval "$CMD")
      WANT=$(grep -A2 -F "\$ $CMD" "$T/ReadMe" | tail -2 | sed 's/^ *//')
      [[ "$GOT" == "$WANT" ]] || { echo "FAIL ReadMe command output: $CMD"; exit 1; }
    else
      N=$(cd "$T" && eval "$CMD" | grep -c "^Case: ")
      [[ "$N" == 45 ]] || { echo "FAIL ReadMe command: $CMD"; exit 1; }
    fi
    echo "  ReadMe command OK: $CMD"
  done < <(grep -E '^ +(\$ )?python3 ' "$T/ReadMe" | grep -v '<string>' | sed -E 's/^ +(\$ )?//' | sort -u)
  [[ $NCMD -ge 2 ]] || { echo "FAIL too few ReadMe commands found ($NCMD)"; exit 1; }
  rm -rf "$T"
  echo "$NO.zip OK: $LIST"
done
if grep -qF "fillin{" workdone/*_WorkDone.tex && ! grep -q '\\drafttrue' workdone/status.tex; then
  echo "FAIL: WorkDone placeholders remain but draft mode is off"; exit 1
fi
if grep -q '\\drafttrue' workdone/status.tex; then
  echo "WARNING: WorkDone documents are still DRAFTS (banner on). NOT READY FOR SUBMISSION."
  echo "         Each student must confirm/edit workdone/<No>_WorkDone.tex, set workdone/status.tex to \\draftfalse, rebuild and repackage."
fi
