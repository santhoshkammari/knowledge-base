#!/bin/bash
set -euo pipefail
BASE=/disk2/santhosh/cs224-audio
PY=/disk2/santhosh/envs-phonon/bin/python
OUT=/disk2/santhosh/cs224-transcripts/cs224/transcripts_phonon2
mkdir -p "$BASE/wav"
for f in "$BASE"/lecture_*.webm; do
  b=$(basename "$f" .webm)
  n=${b#lecture_}; n=${n%%_*}
  "$PY" -I "$BASE/towav.py" "$f" "$BASE/wav/lecture_$n.wav"
  "$PY" -u "$(dirname "$0")/stream_asr.py" "$BASE/wav/lecture_$n.wav" "$OUT/$b.txt"
done
touch /disk2/santhosh/cs224-audio/redo_success
