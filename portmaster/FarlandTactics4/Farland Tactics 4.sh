#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  파랜드 택틱스 4 (Farland Odyssey 2 / 파랜드 택틱스 4) — Windows / DirectDraw
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

GAMEDIR="/$directory/ports/farlandtactics4"
[ -d "$GAMEDIR" ] || GAMEDIR="$(cd "$(dirname "$0")" && pwd)/farlandtactics4"
DATADIR="$GAMEDIR/data"

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

export WINEPREFIX="$WINECELLAR/prefix-farland"
export WINEARCH=win64
export WINEDEBUG=-all
export WINEDLLOVERRIDES="mscoree,mshtml=d;ddraw=n,b"
export WINEDLLPATH="$WINE/lib/wine"

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
$GPTOKEYB "FT4.EXE" -c "$GAMEDIR/farlandtactics4.gptk" &
GPTOKEYB_PID=$!

printf "\033c" > /dev/tty0
echo "파랜드 택틱스 4 실행 중... (첫 실행은 느립니다)" > /dev/tty0

box64 "$WINE/bin/wine" "FT4.EXE" 2>&1 | tee "$GAMEDIR/log.txt"

kill -9 $GPTOKEYB_PID 2>/dev/null
$ESUDO kill -9 $(pidof gptokeyb) 2>/dev/null
$ESUDO systemctl restart oga_events 2>/dev/null &
printf "\033c" > /dev/tty0
