#!/bin/bash
# .sh 문법 검사 (컨테이너/리눅스에서 실행)
ok=0; bad=0
for f in /src/portmaster/*/*.sh; do
  if bash -n "$f" 2>/dev/null; then
    echo "OK   $f"
    ok=$((ok+1))
  else
    echo "FAIL $f"
    bash -n "$f"
    bad=$((bad+1))
  fi
done
echo "----"
echo "OK=$ok FAIL=$bad"
