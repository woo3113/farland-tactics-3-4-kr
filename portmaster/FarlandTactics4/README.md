# 파랜드 택틱스 4 (PortMaster Wine 포트)

파랜드 오딧세이 2 ~그대에게 보내는 세레나데~ (2000, TGL) — 국내명 **파랜드 택틱스 4**.
Windows 95/98용 32비트 게임(PE32, DirectDraw)을 **Wine**으로 실행합니다.

## 설치

1. 이 폴더(`Farland Tactics 4.sh`, `farlandtactics4/`)를 기기의 포트 폴더로 복사
   - ROCKNIX/AmberELEC: `/roms/ports/`
   - ArkOS: `/roms/tools/PortMaster/`
   - muOS: `/mmc/ports/` (+ `.sh`는 `/mnt/mmc/ROMS/Ports/`)
2. **보유한 게임 파일 전체**를 `farlandtactics4/data/` 에 복사
   ```
   FT4.EXE  mapdata.pac  grpdata.pac  visual0.pac  voice0.pac
   bgm/  wav/  scr/  dat/  DOOGIE/
   ITEM.CFG  STAT.CFG  ITEMEDIT.EXE  STATEDIT.EXE
   _inmm.dll  _inmm.ini  _FT4.exe  fo2sv_*.fos
   ```
3. 포트 실행 → 첫 실행 시 Wine 프리픽스 생성(수 분) → 게임 시작

## 요구사항

| | |
|---|---|
| 32비트 지원 기기 | `box86` + wine x86(≤10.4) — **권장** |
| 32비트 미지원(SM8650/SM8750) | Wine Hangover(`box64`) — 느림 |
| wine 실행 파일 | CFW dev 빌드 동봉 또는 `.winecellar` 러너 |

## 조작

좌측 아날로그=마우스, **A=좌클릭**, **B=우클릭**, R1=마우스 느리게, X=Enter, Y=Esc,
L2=F12, **Start+Select=종료**. 자세한 튜닝은 `farlandtactics4.gptk`.

## 문제가 생기면

`farlandtactics4/logs/log.txt` 를 확인하세요.
문서: `docs/02-portmaster-wine.md`(전략), `docs/06-troubleshooting.md`(증상별 조치)

## 법적 안내

이 포트 패키지에는 **런처 스크립트와 설정만** 포함됩니다.
게임 데이터(정품)와 Wine/box86 바이너리는 포함하지 않으며, 사용자가 직접 준비합니다.
