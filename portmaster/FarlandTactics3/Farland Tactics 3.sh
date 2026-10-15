#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  파랜드 택틱스 3 (Farland Tactics 3) — Windows 95/98 / DirectDraw
#  실행 방식: (번들 weston 필요시 기동) + box64 + wine(amd64 wow64)
#
#  필요 파일 (모두 roms/windows/.winecellar/ 아래)
#    wine-11.19-amd64-wow64/   wine 본체
#    prefix-farland/           wine 프리픽스 (TGL/irori 레지스트리 주입 완료)
#    weston/                   디스플레이 서버 번들 (X11/Wayland 없는 CFW 대응)
#
#  환경변수로 조정 가능
#    FARLAND_VDESK   wine 가상 데스크톱 해상도 (기본 720x720 = RGB30 패널)
#    FARLAND_NOWESTON=1  weston 자동 기동 끄기
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
LOG="$GAMEDIR/log.txt"

for c in "/$directory/windows/.winecellar" "/roms/windows/.winecellar" "/storage/roms/windows/.winecellar"; do
  if [ -x "$c/wine-11.19-amd64-wow64/bin/wine" ]; then
    WINECELLAR="$c"
    break
  fi
done
WINE="$WINECELLAR/wine-11.19-amd64-wow64"
WESTON="$WINECELLAR/weston"

if [ ! -x "$WINE/bin/wine" ]; then
  echo "wine 을 찾을 수 없습니다: roms/windows/.winecellar" > /dev/tty0
  sleep 6
  exit 1
fi

: > "$LOG"
echo "=== Farland Tactics 3 $(date) ===" >> "$LOG"

# ── wine 환경 ────────────────────────────────────────────────────────────────
export WINEPREFIX="$WINECELLAR/prefix-farland"
export WINEARCH=win64
export WINEDEBUG=-all
export WINEDLLOVERRIDES="mscoree,mshtml=d;ddraw=n,b"
export WINEDLLPATH="$WINE/lib/wine"

# ── box64 ────────────────────────────────────────────────────────────────────
export BOX64_NOBANNER=1
export BOX64_LOG=0
export BOX64_DYNAREC_BIGBLOCK=2
export BOX64_DYNAREC_STRONGMEM=1
export BOX64_DYNAREC_FASTNAN=1
export BOX64_DYNAREC_FASTROUND=1
export BOX64_DYNAREC_SAFEFLAGS=1
export BOX64_DYNAREC_X87DOUBLE=1
export BOX64_DYNAREC_ALIGNED_ATOMICS=1

# ── 디스플레이 서버 (X11/Wayland 가 없는 CFW 대응) ───────────────────────────
WESTON_PID=""
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ] && [ -x "$WESTON/bin/weston" ] && [ -z "$FARLAND_NOWESTON" ]; then
  # weston 은 모듈 경로가 컴파일 시 고정 → 짧은 경로 /roms/w 를 만들어 사용
  [ -e /roms/w ] || ln -sfn "$WESTON/lib/weston" /roms/w
  export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp/wine-$USER}"
  mkdir -p "$XDG_RUNTIME_DIR"; chmod 700 "$XDG_RUNTIME_DIR"
  export LD_LIBRARY_PATH="$WESTON/lib:$WESTON/lib/weston:${LD_LIBRARY_PATH:-}"
  export XKB_CONFIG_ROOT="$WESTON/share/X11/xkb"
  export XDG_DATA_DIRS="$WESTON/share:${XDG_DATA_DIRS:-/usr/share}"

  weston_start() {
    "$WESTON/bin/weston" --backend=drm-backend.so --shell=kiosk-shell.so \
        --socket=wayland-1 --idle-time=0 "$@" --log="$GAMEDIR/weston.log" >> "$LOG" 2>&1 &
    WESTON_PID=$!
  }
  weston_start
  sleep 4
  if ! kill -0 "$WESTON_PID" 2>/dev/null; then
    echo "[display] GL 렌더러 실패 → pixman 으로 재시도" >> "$LOG"
    weston_start --use-pixman
    sleep 4
  fi
  export WAYLAND_DISPLAY=wayland-1
  echo "[display] weston pid=$WESTON_PID socket=wayland-1" >> "$LOG"
fi

cd "$DATADIR"

$ESUDO chmod 666 /dev/uinput 2>/dev/null
$GPTOKEYB "FT3K.EXE" -c "$GAMEDIR/farlandtactics3.gptk" &
GPTOKEYB_PID=$!

printf "\033c" > /dev/tty0
echo "파랜드 택틱스 3 실행 중... (첫 실행은 느립니다)" > /dev/tty0

# kiosk-shell 은 창을 화면에 꽉 채우므로 가상 데스크톱으로 원본 비율(4:3)을 유지한다
VDSK="${FARLAND_VDESK:-720x720}"
box64 "$WINE/bin/wine" explorer "/desktop=farland,$VDSK" "FT3K.EXE" >> "$LOG" 2>&1

kill -9 $GPTOKEYB_PID 2>/dev/null
$ESUDO kill -9 $(pidof gptokeyb) 2>/dev/null
[ -n "$WESTON_PID" ] && kill "$WESTON_PID" 2>/dev/null
$ESUDO systemctl restart oga_events 2>/dev/null &
printf "\033c" > /dev/tty0
echo "=== 종료 $(date) ===" >> "$LOG"
