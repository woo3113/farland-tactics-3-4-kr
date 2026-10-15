#!/bin/bash
# =============================================================================
#  Farland Tactics 4 (파랜드 택틱스 4 / 파랜드 오딧세이 2) — PortMaster Wine 런처
#  PORTMASTER: farlandtactics4.zip
#  실행 방식: box86 + wine(win32)  또는  Wine Hangover(box64)
#  자세한 배경: FarlandPort/docs/02-portmaster-wine.md
# =============================================================================

XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

# --- PortMaster preamble -----------------------------------------------------
if [ -d "/opt/system/Tools/PortMaster/" ]; then
  controlfolder="/opt/system/Tools/PortMaster"
elif [ -d "/opt/tools/PortMaster/" ]; then
  controlfolder="/opt/tools/PortMaster"
elif [ -d "/roms/ports/PortMaster" ]; then
  controlfolder="/roms/ports/PortMaster"
else
  controlfolder="/roms/tools/PortMaster"
fi

source "$controlfolder/control.txt"
[ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
get_controls

# --- paths -------------------------------------------------------------------
GAMEDIR="/$directory/ports/farlandtactics4"
EXEC="FT4.EXE"
cd "$GAMEDIR" || { echo "GAMEDIR 없음: $GAMEDIR"; exit 1; }
mkdir -p "$GAMEDIR/logs"
LOG="$GAMEDIR/logs/log.txt"
> "$LOG" && exec > >(tee "$LOG") 2>&1

echo "[FarlandPort] 시작 $(date)"
echo "[FarlandPort] GAMEDIR=$GAMEDIR"

# --- 게임 데이터 확인 -----------------------------------------------------------
if [ ! -f "$GAMEDIR/data/$EXEC" ]; then
  echo "[FarlandPort] 게임 데이터 없음: data/$EXEC"
  pm_message "farlandtactics4/data/ 안에 보유한 게임 파일을 복사하세요."
  sleep 8
  exit 1
fi

# --- exports -----------------------------------------------------------------
export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
export WINEDEBUG=-all
export WINEDLLOVERRIDES="ddraw,dinput,dsound=n,b"

# --- 러너 선택: 32비트 서브시스템 유무로 결정 --------------------------------------
HAVE32=0
if [ -d /usr/lib32 ] || [ -d /lib32 ] || [ -d /usr/lib/i386-linux-gnu ]; then HAVE32=1; fi

if command -v box86 >/dev/null 2>&1 && [ "$HAVE32" = "1" ]; then
  BOX="box86"
  export WINEARCH=win32
  export WINEPREFIX="$HOME/.wine32"
  echo "[FarlandPort] 러너: box86 + wine(win32)  [32비트 경로]"
else
  BOX="box64"
  export WINEPREFIX="$HOME/.wine"
  echo "[FarlandPort] 러너: box64 + Wine Hangover  [32비트 미지원 기기 → 느릴 수 있음]"
fi

if ! command -v wine >/dev/null 2>&1; then
  echo "[FarlandPort] wine 실행 파일을 찾을 수 없습니다."
  pm_message "Wine 러너가 필요합니다. (docs/02-portmaster-wine.md 참고)"
  sleep 8
  exit 1
fi

# --- wine prefix 초기화(첫 실행: 수 분 소요 가능) -----------------------------------
if [ ! -d "$WINEPREFIX" ]; then
  echo "[FarlandPort] wine prefix 생성: $WINEPREFIX"
  $BOX wine wineboot -u || true
fi

# --- DirectDraw → OpenGL (1회) --------------------------------------------------
if [ ! -f "$WINEPREFIX/.farland_ddr_done" ]; then
  if command -v winetricks >/dev/null 2>&1; then
    echo "[FarlandPort] winetricks ddr=opengl 적용"
    winetricks -q ddr=opengl || true
  else
    echo "[FarlandPort] winetricks 없음 → ddr 설정 생략(색상 문제 시 수동 적용)"
  fi
  touch "$WINEPREFIX/.farland_ddr_done"
fi

# --- _inmm(BGM) 레지스트리 (실패해도 진행) ------------------------------------------
if [ -f "$GAMEDIR/data/DOOGIE/_inmm.reg" ] && [ ! -f "$WINEPREFIX/.farland_inmm_done" ]; then
  echo "[FarlandPort] _inmm 레지스트리 등록 시도"
  ( cd "$GAMEDIR/data" && $BOX wine regedit /S "DOOGIE\\_inmm.reg" ) || true
  touch "$WINEPREFIX/.farland_inmm_done"
fi

# --- 컨트롤 매핑 ---------------------------------------------------------------
$GPTOKEYB "$EXEC" -c "$GAMEDIR/farlandtactics4.gptk" &

# --- 실행 (작업 디렉터리 = data : bgm\ _inmm 상대경로 때문) ---------------------------
echo "[FarlandPort] 실행: $BOX wine $EXEC"
( cd "$GAMEDIR/data" && $BOX wine "$EXEC" 2>&1 )

# --- 정리 ---------------------------------------------------------------------
$ESUDO kill -9 $(pidof gptokeyb) 2>/dev/null
unset LD_LIBRARY_PATH
unset SDL_GAMECONTROLLERCONFIG
[ -n "$ESUDO" ] && $ESUDO systemctl restart oga_events >/dev/null 2>&1 &

echo "[FarlandPort] 종료 $(date)"
exit 0
