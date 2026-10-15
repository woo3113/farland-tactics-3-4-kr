# 10. (실험) Starboard — 안드로이드에서 PortMaster 포트를 시도하는 길

## 1. Starboard가 뭔가

- **비공식 3rd-party 프로젝트**(get-starboard.app, GitHub `get-starboard/starboard`).
- 안드로이드 기기 위에 **Debian 리눅스 실행 환경**을 만들고, 그 안에서 **PortMaster 카탈로그의 포트**를 실행합니다.
  영상/사운드는 안드로이드 화면으로, 입력은 반대로 전달됩니다.
- **Obtainium**으로 APK를 설치하고, 첫 실행 시 런타임을 내려받습니다(수 분).

## 2. 한계 (공식 문서 기준)

- **모든 포트가 되는 게 아닙니다** — compatibility list가 있고, "일부는 잘 되고, 일부는 겨우 되고, 일부는 안 됩니다".
- 개발자 본인도 *"PortMaster 전체를 안드로이드로 옮기는 것이 목적이 아니다"* 라고 명시.
- 네이티브 안드로이드 포트가 있는 게임은 그쪽이 항상 더 좋습니다.
- **Wine 기반 포트**는 런타임에 `wine`/`box86`이 필요하므로 별도 준비 없이는 동작하지 않습니다.

## 3. 우리 게임(FT3/FT4)에 적용하면?

우리 포트는 **Wine + box86(wine x86)** 로 Windows exe를 돌리는 구조입니다.

| 필요한 것 | Starboard Debian 환경에 기본 제공? | 판단 |
|---|---|---|
| `wine` (x86, 32비트) | ❌ (별도 설치 필요) | 불리 |
| `box86` (32비트 번역) | ❌ | 불리 |
| 32비트 라이브러리 | 환경에 따라 상이 | 불확실 |
| GL4ES/OpenGL ES 경로 | 부분 지원 | 조건부 |

→ **결론: 우리 포트를 Starboard에 그대로 올리는 것은 권장하지 않습니다.**
   (네이티브 ARM 포트였다면 이야기가 다릅니다.)

## 4. 그래도 시도해볼 가치가 있는 경우

1. Starboard 런타임 안에 `box86` + `wine`(또는 hangover)을 **직접 넣을 수 있다면** 이론상 가능합니다.
   - PortMaster 포트 스크립트가 `wine`을 PATH에서 찾는 구조이므로, 런타임에 wine을 배치하면 실행될 수 있습니다.
2. 이 경우 **우리 포트 패키지를 "Starboard용 런타임 포함판"으로 별도 제작**해야 합니다.
   - `bottle.json`/`.winecellar` 스타일(JeodC 계열) 접근이 더 적합합니다.

즉, **"실험적 확장"** 으로만 취급하고, 기본 경로는:
- 리눅스 기기 → **PortMaster 포트** ([03-packaging-and-install.md](03-packaging-and-install.md))
- 안드로이드 기기 → **Winlator** ([05-android-winlator.md](05-android-winlator.md))

## 5. 참고 링크

- Starboard: https://get-starboard.app/ (호환 목록/FAQ)
- PortMaster FAQ(안드로이드 미지원 명시): https://portmaster.games/faq.html
- Wine 포트(bottle) 스타일 참고: `JeodC/PortMaster-Wine`, `RHH-Wine`
