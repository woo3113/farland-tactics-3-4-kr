# 파랜드 택틱스 3 (PortMaster Wine 포트)

파랜드 오딧세이(1999, TGL) — 국내명 **파랜드 택틱스 3**.
Windows 95/98용 32비트 게임(PE32, DirectDraw)을 **Wine**으로 실행합니다.

## 설치

1. 이 폴더(`Farland Tactics 3.sh`, `farlandtactics3/`)를 기기의 포트 폴더로 복사
   - ROCKNIX/AmberELEC: `/roms/ports/`
   - ArkOS: `/roms/tools/PortMaster/`
   - muOS: `/mmc/ports/` (+ `.sh`는 `/mnt/mmc/ROMS/Ports/`)
2. **보유한 한국어판 파일 전체**를 `farlandtactics3/data/` 에 복사
   ```
   FT3K.EXE  GRPDATA.PAC  MAPDATA.PAC  GEMT.CFG
   BGM/  CVK/  WVK/  DAT/  SCR/  data_ud/  DOOGIE/
   _inmm.dll  _inmm.ini  _FT3_Kor_Voice.exe  OD*.FOS
   ```
   (용량 절약: 일본어 음성 `CVJ/`, `WVJ/`, `FT3J.EXE` 는 생략 가능 — 390MB 절감)
3. 포트 실행 → 첫 실행 시 Wine 프리픽스 생성(수 분) → 게임 시작

## 요구사항

| | |
|---|---|
| 32비트 지원 기기 | `box86` + wine x86(≤10.4) — **권장** |
| 32비트 미지원(SM8650/SM8750) | Wine Hangover(`box64`) — 느림 |
| wine 실행 파일 | CFW dev 빌드 동봉 또는 `.winecellar` 러너 |

## 조작

좌측 아날로그=마우스, **A=좌클릭**, **B=우클릭**, R1=마우스 느리게, X=Enter, Y=Esc,
L2=F12, **Start+Select=종료**. 자세한 튜닝은 `farlandtactics3.gptk`.

## 문제가 생기면

`farlandtactics3/logs/log.txt` 를 확인하세요.
문서: `docs/02-portmaster-wine.md`(전략), `docs/06-troubleshooting.md`(증상별 조치)

## 법적 안내

이 포트 패키지에는 **런처 스크립트와 설정만** 포함됩니다.
게임 데이터(정품)와 Wine/box86 바이너리는 포함하지 않으며, 사용자가 직접 준비합니다.
