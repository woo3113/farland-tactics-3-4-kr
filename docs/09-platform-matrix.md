# 09. 플랫폼 매트릭스 — "한 번 만들면 어디까지 되나?"

이 문서는 **"PortMaster로 만들면 안드로이드든 리눅스든 다 되지 않나?"** 라는 질문에 대한 정확한 답입니다.

## 1. 결론 요약

| 질문 | 답 |
|---|---|
| PortMaster 포트를 만들면 그게 안드로이드에서 바로 돌아가나? | **아니오.** PortMaster는 **리눅스 CFW 전용**입니다 (공식 FAQ: Android 미지원, 이유 = 파일시스템/권한/패키지 모델이 다름) |
| 그럼 안드로이드에서는 못 하나? | **세 가지 우회로**가 있습니다 → 2절 |
| Wine으로 게임을 돌리는 **작업**은 재사용되나? | **예, 대부분 재사용됩니다** → 3절 |
| 패키지/런처도 재사용되나? | **아니오.** 플랫폼별로 다시 만들어야 합니다(형식이 다름) → 3절 |

## 2. 안드로이드에서 이 게임을 하는 3가지 길

| 길 | 방법 | 실현성 | 비고 |
|---|---|---|---|
| **A. Winlator** | 안드로이드 앱(Wine + Box64/FEX)에 게임 폴더 연결 | ★★★ **현실적** | **이미 패키지 제작 완료** (`F:\DGGL\Export\...zip`) |
| **B. Starboard** | 안드로이드에서 **Debian 리눅스 런타임**을 띄우고 PortMaster 카탈로그 포트 실행 | ★☆☆ 보류 | 비공식 3rd-party. **ARM 네이티브 포트**가 주 대상이고, 우리처럼 **box86/wine에 의존하는 포트는 런타임에 wine/box86이 없으면 불가** → [10-starboard-android.md](10-starboard-android.md) |
| **C. 듀얼부트** | 같은 기기의 리눅스 CFW(ROCKNIX 등) 부팅 → PortMaster 사용 | ★★☆ | "안드로이드에서"가 아니라 "기기의 리눅스 쪽에서". CFW가 지원하는 기기여야 함 |

> 정리: **안드로이드 단독 기기 → A(Winlator)** 가 정답입니다.
> 리눅스 CFW를 올릴 수 있는 기기라면 → **PortMaster(이 프로젝트)** 가 성능·편의가 가장 좋습니다.

## 3. 무엇이 재사용되고, 무엇이 재사용되지 않나

### ✅ 재사용되는 것 (핵심 자산)
| 자산 | 설명 |
|---|---|
| **게임 데이터 준비** | 무엇을 복사하고 무엇을 빼도 되는지(일본어 음성 등) — `shared/game-notes.md` |
| **Wine 튜닝 값** | `winetricks ddr=opengl`(DirectDraw→OpenGL), dll 오버라이드, win32 프리픽스, `WINEDEBUG=-all` — `shared/wine-tuning.md` |
| **런처 로직(의사코드)** | 작업디렉터리를 게임 폴더로(상대경로 BGM 때문에), 프리픽스 1회 생성, `_inmm` reg 등록 시도 |
| **조작 설계** | 마우스 중심 → 좌클릭/우클릭/커서이동/마우스 느리게. 패드 매핑 *개념*은 두 플랫폼 공통 |
| **문제 해결 지식** | 팔레트 깨짐, 무음(BGM), 첫 실행 지연, 클릭 씹힘 → [06-troubleshooting.md](06-troubleshooting.md) |
| **게임 포맷 분석** | PAC/LZSS/SCR — 데이터 가공(에셋 추출·검증)에 유용 |

### ❌ 재사용되지 않는 것 (플랫폼별 재작업)
| 항목 | PortMaster(리눅스) | Android(Winlator) |
|---|---|---|
| 패키지 형식 | `zip` + `port.json` + `<Port>.sh` + `.gptk` | 컨테이너/숏컷 + Winlator 설정 + 드라이브 매핑 |
| 실행 계층 | `box86 wine` (32비트) / Hangover | Box64/FEX + Wine (+ DXVK/wined3d 선택) |
| 조작 | **gptokeyb**(패드→마우스/키) | 터치 오버레이 / BT 마우스 |
| 그래픽 워크어라운드 | `ddr=opengl`(GL4ES 경로) | dgVoodoo2 또는 wine 내장 ddraw |
| 설치 경로 | `/roms/ports/...` | 앱 내부 드라이브 |

## 4. 그래서 이 프로젝트는 이렇게 갑니다

```
            [공유 코어]  게임 데이터 · Wine 설정 · 조작 설계 · 트러블슈팅
                    │
     ┌──────────────┼──────────────────────────┐
     ▼              ▼                          ▼
 PortMaster       Winlator                   Starboard(실험)
 (리눅스 CFW)     (안드로이드)                (안드로이드 + Debian 런타임)
 portmaster/      (기존 Export zip)           docs/10 참고
```

- **PortMaster = 주력 산출물** (이 저장소의 `portmaster/`)
- **Winlator = 병행 산출물** (이미 완성, `F:\DGGL\Export\*.zip`)
- **Starboard = 실험 후보** (가능성 낮음, 문서만 정리)

## 5. "하나의 포트로 양쪽"이 가능한 예외 케이스

- **네이티브 ARM 포트**(오픈소스 엔진 재구현, Godot/Love2D 등)라면 Starboard로 안드로이드에서도 실행될 여지가 큽니다.
- 반대로 **우리처럼 Windows 게임 + Wine** 구조는 **포트 컨테이너에 wine/box86 바이너리가 포함되지 않으므로**
  Starboard에서 그대로 돌기 어렵습니다(런타임 부재).
- 즉, **"PortMaster 포트 = 리눅스 / Winlator = 안드로이드"** 로 이해하는 것이 정확합니다.
