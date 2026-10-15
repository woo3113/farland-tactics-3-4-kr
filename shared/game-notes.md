# 공유 코어 — 게임 데이터 준비 (두 플랫폼 공통)

PortMaster(리눅스)와 Winlator(안드로이드) **양쪽에 그대로 쓰이는** 데이터 준비 안내입니다.

## 1. 원본 위치 (이 PC)

| 게임 | 원본 폴더 | 크기 |
|---|---|---|
| 파랜드 택틱스 3 | `F:\DGGL\Games\FT3_Win` | 약 0.95 GB (일본어 음성 포함) |
| 파랜드 택틱스 4 | `F:\DGGL\Games\FT4_Win` | 약 0.55 GB |

## 2. 넣는 위치

| 플랫폼 | 목적지 |
|---|---|
| PortMaster | `.../farlandtactics3/data/` (또는 `farlandtactics4/data/`) |
| Winlator | 컨테이너 내 `D:\FT3` / `D:\FT4` (경로는 짧게) |

자동 스테이징(PC에서): `.\stage_data.ps1 -Game 3` / `-Game 4` / `-Game all`

## 3. 복사할 파일

### 파랜드 택틱스 3
```
FT3K.EXE            게임 본체(한국어판)
GRPDATA.PAC         그래픽 (약 50MB)
MAPDATA.PAC         맵 (약 30MB)
GEMT.CFG
ODDATA00~08.FOS
BGM\                BGM WAV 20곡 (약 140MB)
CVK\                한국어 음성 (약 374MB)
WVK\                한국어 음성/효과음 (약 18MB)
DAT\  data_ud\  SCR\
DOOGIE\             _inmmserv.exe, FT3.reg, _inmm.reg, dxwnd 프로필
_inmm.dll  _inmm.ini  _FT3_Kor_Voice.exe
```

**용량 절약(선택)**: `CVJ\`, `WVJ\`, `FT3J.EXE`, `_FT3_Jap_Voice.exe` 제거 → **약 390MB 절감**
(한국어 음성만 남김. 일본어 음성으로 플레이할 계획이 없으면 지우는 것을 권장)

### 파랜드 택틱스 4
```
FT4.EXE             게임 본체
mapdata.pac         맵 (약 180MB)
grpdata.pac         그래픽 (약 36MB)
visual0.pac         비주얼 (약 6MB)
voice0.pac          음성 (약 114MB)
bgm\                BGM mp3 21곡
wav\                효과음/보이스
scr\  dat\  DOOGIE\
ITEM.CFG  STAT.CFG  ITEMEDIT.EXE  STATEDIT.EXE
_inmm.dll  _inmm.ini  _FT4.exe  fo2sv_00~09.fos
```

> `DosBox\` 폴더(DGGL 런처의 메타데이터/스크린샷)는 **불필요** → 지워도 됩니다.

## 4. 절대 규칙 (두 플랫폼 공통)

1. **작업 디렉터리를 게임 폴더로** — BGM/음성이 상대경로(`bgm\Track02.mp3`, `CVK\VO0000.WAV`)이고
   `_inmm.ini`의 `_inmmserv` 경로도 상대경로입니다.
2. **CD 불필요** — DGGL 설정상 `CD=0`(원판 CD 없이 실행됨).
3. 런처(VB6 스텁 `_FT3_Kor_Voice.exe`, `_FT4.exe`)는 실패할 수 있음 → **본체(`FT3K.EXE`, `FT4.EXE`) 직접 실행**이 안전.
4. 파일명/경로에 한글이 있어도 동작하지만, **경로가 짧고 ASCII인 편이 문제가 적습니다**(특히 Winlator).

## 5. 검증 팁

- 실행 직후 게임이 뜨면 OK. 검은 화면/즉시 종료면 [06-troubleshooting.md](../docs/06-troubleshooting.md)
- BGM만 안 나오는 경우는 **정상적인 실패 모드**입니다(게임 진행은 가능).
