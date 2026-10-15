# FarlandPort — 파랜드 택틱스 3 / 4 이식 프로젝트

> 원제: **파랜드 오딧세이 ~전설을 잇는 자~**(1999) / **파랜드 오딧세이 2 ~그대에게 보내는 세레나데~**(2000)
> 국내 유통명: **파랜드 택틱스 3** / **파랜드 택틱스 4** (TGL / Family Production, Windows 95·98)

리눅스 휴대기기(**PortMaster**)에서 이 두 게임을 돌리는 것을 **주 목표**로 하고,
같은 데이터로 **안드로이드(Winlator)** 병행 실행과 **드림캐스트 네이티브 이식** 연구를 함께 다룹니다.

> 이 프로젝트는 게임 데이터를 배포하지 않습니다. **정품(보유한 원판)의 파일만** 사용합니다.

---

## 1. 왜 "Wine 래핑"인가

이 게임들은 DOS 게임이 아니라 **Windows 95/98용 32비트 게임**입니다.

| 항목 | 파랜드 택틱스 3 | 파랜드 택틱스 4 |
|---|---|---|
| 실행 파일 | `FT3K.EXE` (한국어판) | `FT4.EXE` |
| 포맷 | PE32 / i386 / GUI (Win32) | PE32 / i386 / GUI |
| 사용 API | `DDRAW.DLL`, `DINPUT.DLL`, `DSOUND.DLL`, `_INMM.DLL` | 동일 |
| BGM | `_inmm.dll`이 CD음악을 `bgm\*.wav`로 대체 | `_inmm.dll`이 `bgm\Track02~21.mp3`로 대체 |
| CD 요구 | 없음 | 없음 |

→ **DirectDraw 2D 게임**이라 번역 계층(Wine)에서 잘 돌아가는 부류입니다.
소스가 없으므로 "네이티브 리컴파일"은 불가능하고, **Wine 으로 감싸서 실행**하는 것이 실용적인 정답입니다.

---

## 2. 실행 경로 3개

| 경로 | 대상 | 상태 | 문서 |
|---|---|---|---|
| ★ **A. PortMaster + Wine** | 리눅스 CFW 휴대기기 (ROCKNIX/Aurknix/ArkOS/muOS) | **이 프로젝트의 주력** | [docs/02-portmaster-wine.md](docs/02-portmaster-wine.md) |
| **B. Android + Winlator** | 안드로이드 게임기 (Snapdragon 등) | 패키지 제작 완료 | [docs/05-android-winlator.md](docs/05-android-winlator.md) |
| C. Dreamcast 네이티브 | 드림캐스트(실기/Flycast) | POC 검증 완료(연구) | [docs/08-reference-dreamcast.md](docs/08-reference-dreamcast.md) |

세 경로는 **같은 원본 데이터**를 쓰고, 검증된 데이터 포맷 지식([docs/01-game-and-data.md](docs/01-game-and-data.md))을 공유합니다.

### 2.1 자주 하는 질문 — "PortMaster로 만들면 안드로이드에서도 되나?"

| 질문 | 답 |
|---|---|
| PortMaster 포트가 안드로이드에서 바로 돌아가나? | **아니오.** PortMaster는 **리눅스 CFW 전용** (공식 FAQ에 Android 미지원 명시) |
| 안드로이드에서 이 게임을 하려면? | **Winlator**(현실적, 이미 완성) / Starboard(실험적, Wine 포트는 불리) / **듀얼부트**로 리눅스 CFW 부팅 |
| Wine 튜닝·데이터 준비·조작 설계는 재사용되나? | **예** → `shared/` ([game-notes](shared/game-notes.md) · [wine-tuning](shared/wine-tuning.md)) |
| 패키지/런처는 재사용되나? | **아니오.** 플랫폼별로 다시 만들어야 함 (zip+port.json ↔ Winlator 컨테이너) |

> 정리: **PortMaster = 리눅스 / Winlator = 안드로이드**.
> 같은 기기에서 둘 다 쓰려면 **리눅스 CFW 듀얼부트**가 방법입니다.
> 상세: [docs/09-platform-matrix.md](docs/09-platform-matrix.md), 실험적 안드로이드 경로: [docs/10-starboard-android.md](docs/10-starboard-android.md)

---

## 3. 빠른 시작 (PortMaster 경로)

### 3.1 기기 요구사항 — **가장 중요한 갈림길**

이 게임은 **32비트 PE**이므로 32비트 x86 실행이 필요합니다.

| 기기/SoC | 32비트 서브시스템 | 사용할 러너 | 비고 |
|---|---|---|---|
| RK3326/RK3566/RK3588 등 Rockchip | 있음 | **`box86` + wine x86(≤10.4)** | 가장 빠름. ArkOS/muOS/ROCKNIX |
| Snapdragon (구형, 32비트 지원) | 있음 | `box86` + wine x86 | ROCKNIX/Aurknix |
| **SM8650 / SM8750 (Odin 3, Pocket S2 등)** | **없음** | **Wine Hangover**(wow64) | `box64`가 wine 내부에 포함. **느림** |
| SM8250/SM8550 (RP5/RP6 계열) | 기기/빌드에 따라 다름 | 확인 후 선택 | ROCKNIX dev 빌드에 `box64`+`wine` 동봉 |

> PortMaster는 **안드로이드에서 직접 돌지 않습니다.** 안드로이드 기기에서 이 경로를 쓰려면
> **ROCKNIX 등 리눅스 CFW를 설치(듀얼부트 또는 대체)** 해야 합니다.

### 3.2 설치 (자동 설치 폴더)

1. 이 저장소의 `portmaster/` 결과물을 zip으로 만듭니다 → `package.ps1` 사용
   (또는 `Farland Tactics 3.sh` + `farlandtactics3/` 폴더를 그대로 복사)
2. CFW별 경로에 넣습니다.

| CFW | 포트 설치 경로 | 자동설치 폴더 |
|---|---|---|
| ROCKNIX / AmberELEC / uOS | `/roms/ports/` | `/roms/ports/PortMaster/autoinstall/` |
| ArkOS | `/roms/tools/PortMaster/` | `/roms/tools/PortMaster/autoinstall/` |
| muOS | `/mmc/ports/` (`.sh`는 `/mnt/mmc/ROMS/Ports/`) | `/mmc/MUOS/PortMaster/autoinstall/` |
| Knulli | `/userdata/roms/ports/` | `/userdata/roms/ports/autoinstall` |

3. **게임 데이터 넣기**: `farlandtactics3/data/` 안에 보유한 한국어판 파일 전체를 복사
   (`FT3K.EXE`, `GRPDATA.PAC`, `MAPDATA.PAC`, `BGM/`, `CVK/`, `WVK/`, `DAT/`, `SCR/`,
    `data_ud/`, `_inmm.*`, `DOOGIE/` …)
4. 포트를 실행 → 첫 실행 시 Wine 프리픽스 생성(수 분 소요) → 게임 시작

### 3.3 조작

마우스 중심 게임이므로 `gptokeyb`로 마우스를 매핑합니다.

| 패드 | 기능 |
|---|---|
| 좌측 아날로그 | 마우스 이동 |
| A | 좌클릭 (선택/이동/공격) |
| B | 우클릭 (취소/메뉴) |
| R1 | 마우스 느리게(정밀) |
| X | Enter (확인) |
| Y | Esc (취소) |
| L2 | F12 (FT3: 던전 몬스터 토글 등) |
| Start + Select | 게임 종료 |

→ 상세/튜닝: [docs/04-controls-gptokeyb.md](docs/04-controls-gptokeyb.md)

---

## 4. 폴더 구조

```
F:\FarlandPort\
├─ README.md                     ← 이 문서 (PortMaster 중심)
├─ docs\
│  ├─ 01-game-and-data.md        게임/데이터 포맷 요약 (PAC·LZSS·SCR)
│  ├─ 02-portmaster-wine.md      ★ Wine 런타임 선택과 실행 전략
│  ├─ 03-packaging-and-install.md 포트 패키징/설치 규약
│  ├─ 04-controls-gptokeyb.md     조작 매핑 설계와 .gptk
│  ├─ 05-android-winlator.md      안드로이드 병행 경로 (완료된 패키지)
│  ├─ 06-troubleshooting.md       문제 해결
│  ├─ 07-roadmap.md               단계별 계획/체크리스트
│  ├─ 08-reference-dreamcast.md   참고: 드림캐스트 네이티브 POC
│  ├─ 09-platform-matrix.md       ★ "어디까지 되나" 정리 (재사용 범위)
│  └─ 10-starboard-android.md     (실험) 안드로이드에서 PortMaster 포트 시도
├─ shared\                       두 플랫폼 공통 자산
│  ├─ game-notes.md               게임 데이터 준비(무엇을 복사/제외)
│  └─ wine-tuning.md              Wine 설정값(ddraw→OpenGL 등)
├─ portmaster\
│  ├─ FarlandTactics3\           포트 패키지 (스크립트+json+gptk)
│  └─ FarlandTactics4\
├─ tools\                        데이터 도구 (PAC 해제 등)
├─ package.ps1                   포트 zip 패키징 스크립트
├─ stage_data.ps1                보유 게임 데이터를 포트 data/ 로 복사
└─ dist\                         생성된 autoinstall zip
```

기존 리버싱 작업장: `F:\DGGL\RE\` (PAC/SCR 리버싱 도구·문서·추출 에셋, `README.md` 참고)

---

## 5. 현재 상태

| 항목 | 상태 |
|---|---|
| 데이터 포맷 규명(PAC/IEL1/LZSS) | ✅ 완료 — 에셋 전량 추출 검증 |
| 안드로이드(Winlator) 실행 패키지 | ✅ 완료 (`Export\파랜드택틱스3(K)_Winlator.zip` 등) |
| 조작 매핑(.gptk) 설계 | ✅ 초안 (`farlandtactics3.gptk`) |
| PortMaster 포트 패키지(스크립트/json) | ✅ 초안 작성 |
| 실기 검증(ROCKNIX/ArkOS) | ⬜ **다음 단계** — 32비트 러너 확보 후 |
| BGM(inmm) 동작 검증 | ⬜ 미검증 |
| SCR 스크립트 디스어셈블러 | 🔶 85% (`F:\DGGL\RE\docs\FORMAT_SCR.md`) |

자세한 계획: [docs/07-roadmap.md](docs/07-roadmap.md)
