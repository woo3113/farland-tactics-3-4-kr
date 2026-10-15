# 03. 포트 패키징과 설치

PortMaster 패키징 규약(2025년 이후 "port/" 구조)을 따릅니다. 개인 사용이 목적이지만
규약을 지키면 PortMaster가 정상 인식/설치합니다.

## 1. 패키지 구조

```
FarlandTactics3/                 (포트 폴더)
├─ Farland Tactics 3.sh          ← 스크립트(대문자 시작, .sh)
├─ port.json                     ← PortMaster 메타데이터
├─ README.md                     ← 포트 설명(사용자용)
├─ gameinfo.xml                  ← EmulationStation 표시용
├─ screenshot.jpg                ← (직접 캡처해 추가)
└─ farlandtactics3/              ← 실행 디렉터리(폴더명 = 포트명)
   ├─ farlandtactics3.gptk       ← 조작 매핑
   ├─ data/                      ← ★ 게임 데이터를 넣는 곳
   ├─ config/                    ← 세이브/설정 bind 대상(자동 생성)
   └─ logs/                      ← 로그
```

> PortMaster 저장소 제출용 규약은 `port/<portname>/...` 이지만,
> **개인 설치**는 `/roms/ports/` 아래에 `Farland Tactics 3.sh` + `farlandtactics3/` 만 있으면 동작합니다.

## 2. port.json

`F:\FarlandPort\portmaster\FarlandTactics3\port.json` 참고. 핵심 필드:

| 필드 | 값(예) | 설명 |
|---|---|---|
| `name` | `farlandtactics3.zip` | 패키지 파일명 |
| `items` | `["Farland Tactics 3.sh", "farlandtactics3"]` | 설치 항목 |
| `attr.title` | `파랜드 택틱스 3` | 표시 이름 |
| `attr.inst` | 게임 데이터 넣는 방법 | 설치 안내 문구 |
| `attr.genres` | `["strategy","rpg"]` | 장르 |
| `attr.runtime` | `[]` | PortMaster 런타임 미사용(Wine은 자체 러너) |
| `attr.arch` | `["aarch64"]` | 호스트 아키텍처 |
| `attr.availability` | `"paid"` | 상용(원판 보유 필요) 표기 |

> `runtime` 은 Godot/Mono 같은 PortMaster 런타임용 필드입니다. Wine 포트는 비워 둡니다.

## 3. 설치 경로 (CFW별)

| CFW | 포트 설치 위치 | 자동설치(패키지 zip 투입) |
|---|---|---|
| ROCKNIX / AmberELEC / uOS | `/roms/ports/` | `/roms/ports/PortMaster/autoinstall/` |
| ArkOS | `/roms/tools/PortMaster/` | `/roms/tools/PortMaster/autoinstall/` |
| muOS | `/mmc/ports/` (+`.sh`는 `/mnt/mmc/ROMS/Ports/`) | `/mmc/MUOS/PortMaster/autoinstall/` |
| Knulli | `/userdata/roms/ports/` | `/userdata/roms/ports/autoinstall` |

**주의**: ArkOS는 `tools`, ROCKNIX는 `ports` 입니다. 잘못된 폴더에 넣으면 **오류 없이 그냥 무시**됩니다.

## 4. 패키징(Windows에서)

```powershell
# F:\FarlandPort 에서 실행
.\package.ps1 -Port FarlandTactics3      # → dist\farlandtactics3.zip 생성
```

`package.ps1`은 다음을 수행합니다.
1. `portmaster\<Port>\` 안에서 `port.json` 의 `items` 를 읽어 zip 구성
2. **`data/` 폴더는 포함하지 않음**(게임 데이터는 사용자가 복사 — 법적/용량)
3. zip 루트에 `Farland Tactics 3.sh` + `farlandtactics3/` 배치(설치 규약 준수)
4. LF 줄바꿈 확인(스크립트는 LF 필수)

## 5. 테스트 절차 (기기에서)

```bash
# 1) 프론트엔드 정지(포트 단독 테스트)
#    ROCKNIX: systemctl stop essway.service
#    ArkOS:   systemctl stop emulationstation
#    Knulli:  /etc/init.d/S31emulationstation stop
#    muOS:    killall -q frontend.sh muxlaunch

# 2) 스크립트 직접 실행(로그 확인)
cd /roms/ports && bash "Farland Tactics 3.sh"

# 3) 로그
cat /roms/ports/farlandtactics3/log.txt
```

## 6. 파일 인코딩/줄바꿈 규칙

- `.sh` 는 **UTF-8 + LF**(CRLF 금지). Windows에서 편집 시 반드시 LF로 저장.
- `port.json`, `gameinfo.xml` 은 UTF-8.
- `.gptk` 는 ASCII/UTF-8 무관하나 주석은 `#`.
