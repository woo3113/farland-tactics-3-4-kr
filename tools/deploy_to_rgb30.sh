#!/bin/bash
# =============================================================================
#  RGB30 / RK3566 (JELOS·ROCKNIX·ArkOS 공통) 에 PortMaster 포트를 배포
#
#  사용법:
#    bash deploy_to_rgb30.sh <IP> <ROOT_PW>            # 포트 패키지만 설치
#    bash deploy_to_rgb30.sh <IP> <ROOT_PW> --with-data # 게임 데이터까지 복사(약 617MB)
#
#  전제: 기기에서 SSH 활성화(Network Settings) + root 암호 확인(System Settings)
#  실행 위치: WSL Ubuntu (sshpass 설치 필요: apt-get install -y sshpass)
# =============================================================================
set -u
IP="${1:-}"; PW="${2:-}"; MODE="${3:-}"
if [ -z "$IP" ] || [ -z "$PW" ]; then
  echo "usage: bash deploy_to_rgb30.sh <IP> <ROOT_PW> [--with-data]"; exit 1
fi

PORT_SRC="/mnt/f/FarlandPort/portmaster/FarlandTactics3"
DATA_SRC="/mnt/f/DGGL/Export/파랜드택틱스3(K)"
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10"
SSH="sshpass -p $PW ssh $SSH_OPTS root@$IP"
SCP="sshpass -p $PW scp $SSH_OPTS -O"

echo "== 1) 기기 정보 확인 =="
$SSH 'uname -a; echo "--- OS ---"; cat /etc/os-release 2>/dev/null | head -4; \
      echo "--- 포트 경로 ---"; ls -d /roms/ports /roms/tools /storage/roms/ports 2>/dev/null; \
      echo "--- 러너 확인 ---"; for b in box86 box64 wine wine64; do printf "%-7s " $b; command -v $b || echo "(없음)"; done; \
      echo "--- winecellar ---"; ls -d /roms/windows/.winecellar /storage/roms/windows/.winecellar ~/.winecellar 2>/dev/null || echo "(없음)"; \
      echo "--- PortMaster ---"; ls -d /roms/ports/PortMaster /roms/tools/PortMaster 2>/dev/null || echo "(없음)"'

# 포트 설치 경로 결정 (ROCKNIX/AmberELEC/uOS = /roms/ports, ArkOS = /roms/ports 도 존재)
PORTS_DIR="$($SSH 'if [ -d /roms/ports ]; then echo /roms/ports; elif [ -d /storage/roms/ports ]; then echo /storage/roms/ports; else echo /roms/ports; fi')"
echo "== 2) 포트 대상 경로: $PORTS_DIR =="

$SSH "mkdir -p '$PORTS_DIR/farlandtactics3/data' '$PORTS_DIR/farlandtactics3/logs'"

echo "== 3) 포트 패키지 업로드 =="
$SCP "$PORT_SRC/Farland Tactics 3.sh" "root@$IP:$PORTS_DIR/"
$SCP -r "$PORT_SRC/farlandtactics3/farlandtactics3.gptk" "root@$IP:$PORTS_DIR/farlandtactics3/"
$SCP -r "$PORT_SRC/farlandtactics3/data/PUT-GAME-DATA-HERE.txt" "root@$IP:$PORTS_DIR/farlandtactics3/data/"
$SSH "chmod +x '$PORTS_DIR/Farland Tactics 3.sh'; ls -la '$PORTS_DIR/Farland Tactics 3.sh'"

if [ "$MODE" = "--with-data" ]; then
  echo "== 4) 게임 데이터 복사 (약 617MB, 시간 소요) =="
  if [ -d "$DATA_SRC" ]; then
    $SCP -r "$DATA_SRC/." "root@$IP:$PORTS_DIR/farlandtactics3/data/"
    $SSH "du -sh '$PORTS_DIR/farlandtactics3/data'; ls '$PORTS_DIR/farlandtactics3/data' | head -20"
  else
    echo "  (로컬 데이터 폴더 없음: $DATA_SRC)"
  fi
fi

echo "== 5) 결과 =="
$SSH "ls -R '$PORTS_DIR/farlandtactics3' | head -30; echo; df -h /roms 2>/dev/null | tail -1"
echo
echo "기기에서: EmulationStation → Ports → 'Farland Tactics 3' 실행"
echo "wine/box86 이 없으면 실행되지 않습니다 → .winecellar 에 wine 러너 필요 (docs/02-portmaster-wine.md)"
