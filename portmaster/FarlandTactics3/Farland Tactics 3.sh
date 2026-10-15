#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  파랜드 택틱스 3 (Farland Tactics 3) — Windows 95/98 / DirectDraw
#  실행 방식: box64 + wine(amd64 wow64)
#
#  필요 조건
#    · aarch64 CFW (ROCKNIX 계열 권장) + box64
#    · X11/Wayland 디스플레이 서버  ← JELOS 20231003 에는 없음(실행 불가)
#    · wine : roms/windows/.winecellar/wine-11.19-amd64-wow64
#    · 프리픽스 : roms/windows/.winecellar/prefix-farland
# ─────────────────────────────────────────────────────────────────────────────
XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

if [ -d "/opt/system/Tools/PortMaster/" ]; then
  controlfolder="/opt/system/Tools/PortMaster"
elif [ -d "/opt/tools/PortMaster/" ]; then
  controlfolder="/opt/tools/PortMaster"
elif [ -d "/roms/ports/PortMaster" ]; then
  controlfolder="/roms/ports/PortMaster"
else
  controlfolder="/storage/roms/ports/PortMaster"
fi

source $controlfolder/control.txt
get_controls

GAMEDIR="/$directory/ports/farlandtactics3"
[ -d "$GAMEDIR" ] || GAMEDIR="$(cd "$(dirname "$0")" && pwd)/farlandtactics3"
DATADIR="$GAMEDIR/data"

# wine 위치 탐색 (CFW 별 roms 경로 차이 대응)
for c in "/$directory/windows/.winecellar" "/roms/windows/.winecellar" "/storage/roms/windows/.winecellar"; do
  if [ -x "$c/wine-11.19-amd64-wow64/bin/wine" ]; then
    WINECELLAR="$c"
    break
  fi
done
WINE="$WINECELLAR/wine-11.19-amd64-wow64"

if [ ! -x "$WINE/bin/wine" ]; then
  echo "wine 을 찾을 수 없습니다 (roms/windows/.winecellar)" > /dev/tty0
  sleep 6
  exit 1
fi

# ── wine 환경 ────────────────────────────────────────────────────────────────
export WINEPREFIX="$WINECELLAR/prefix-farland"
export WINEARCH=win64
export WINEDEBUG=-all
# mscoree/mshtml=disabled : mono/gecko 팝업 방지
# ddraw=n,b : 게임 폴더의 dgVoodoo2 ddraw.dll 이 있으면 그것을, 없으면 wine 내장 ddraw
export WINEDLLOVERRIDES="mscoree,mshtml=d;ddraw=n,b"
export WINEDLLPATH="$WINE/lib/wine"

# ── box64 튜닝 (RK3566 A55 4코어 기준) ───────────────────────────────────────
export BOX64_NOBANNER=1
export BOX64_LOG=0
export BOX64_DYNAREC_BIGBLOCK=2
export BOX64_DYNAREC_STRONGMEM=1
export BOX64_DYNAREC_FASTNAN=1
export BOX64_DYNAREC_FASTROUND=1
export BOX64_DYNAREC_SAFEFLAGS=1
export BOX64_DYNAREC_X87DOUBLE=1
export BOX64_DYNAREC_ALIGNED_ATOMICS=1

cd "$DATADIR"

$ESUDO chmod 666 /dev/uinput 2>/dev/null
$GPTOKEYB "FT3K.EXE" -c "$GAMEDIR/farlandtactics3.gptk" &
GPTOKEYB_PID=$!

printf "\033c" > /dev/tty0
echo "파랜드 택틱스 3 실행 중... (첫 실행은 느립니다)" > /dev/tty0

box64 "$WINE/bin/wine" "FT3K.EXE" 2>&1 | tee "$GAMEDIR/log.txt"

kill -9 $GPTOKEYB_PID 2>/dev/null
$ESUDO kill -9 $(pidof gptokeyb) 2>/dev/null
$ESUDO systemctl restart oga_events 2>/dev/null &
printf "\033c" > /dev/tty0
