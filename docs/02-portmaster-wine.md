# 02. PortMaster + Wine 실행 전략 (핵심 문서)

## 1. 전제: PortMaster는 "설치/관리 도구", 실행 엔진은 별개

PortMaster는 리눅스 CFW 휴대기기에 **포트를 설치/관리**하는 도구입니다. 게임을 실제로 돌리는 것은
포트가 지정한 **런타임/번역 계층**입니다.

이 게임은 32비트 Windows(DirectDraw) 프로그램이므로 다음이 필요합니다.

```
[게임 PE32] → [Wine (win32 프리픽스)] → [box86 또는 hangover] → [ARM64 리눅스]
                                        ↑ 글라이드/GL 경로: wined3d → OpenGL(ES) / GL4ES
```

- **box86**: x86(32비트) → ARM 번역. **32비트 서브시스템(lib32) 필요**
- **box64**: x86_64 → ARM64 번역
- **Wine Hangover**: wine 내부에 box64를 포함한 wow64 빌드 → 32비트 서브시스템 없이도 32비트 exe 실행 가능(느림)

## 2. 러너 선택표 (실측 정보 기반)

| 상황 | 선택 | 환경변수/명령 | 비고 |
|---|---|---|---|
| Rockchip 기기(32비트 지원 O) | **wine x86 10.4 이하 + box86** | `WINEARCH=win32`, `WINEPREFIX=~/.wine32`, `box86 wine ...` | 가장 빠름. 10.4 초과 버전은 box86 호환 문제 |
| 32비트 지원 O + 최신 wine 원함 | Wine x86 + box86 (≤10.4 유지) | 위와 동일 | 버전을 올리지 말 것 |
| **32비트 지원 X (SM8650/SM8750 등)** | **Wine Hangover (wow64)** | `box64 wine ...` | 32→64 변환 비용으로 느림. 대신 미래지향 |
| 이미 `.winecellar`에 러너 있음 | 해당 러너 | 런처가 자동 선택 | `bottle.json` 의 `runner` 값 사용 |

> PortMaster 진영의 Wine 배포 형태: `JeodC/PortMaster-Wine`, `RHH-Wine`,
> 리눅스에서 `roms/windows/.winecellar`(러너/툴 보관), `bottle.json`(설정) 사용.

## 3. DirectDraw 처리

이 게임의 그래픽은 **DirectDraw(DDRAW.DLL)** 입니다. PortMaster 기기에는 **Vulkan이 없습니다.**

| 방법 | 사용 가능? | 설명 |
|---|---|---|
| wine 내장 wined3d → OpenGL | ✅ **권장** | GL4ES/GLES2 경로로 2D 블릿은 충분 |
| DXVK | ❌ | Direct3D 8~11용. DirectDraw 대상 아님 |
| dgVoodoo2 (ddraw→D3D11) | ❌(권장 안 함) | Vulkan/D3D11 필요 → 포터블 기기에 부적합 |
| `winetricks ddr=opengl` | ✅ | wine의 DirectDraw 렌더러를 OpenGL로 강제(팔레트/색상 문제 완화) |

초기 설정 예:

```bash
export WINEDLLOVERRIDES="ddraw,d3d8,d3d9,dinput,dsound=n,b"   # wine 내장 사용
winetricks -q ddr=opengl                                      # DirectDraw → OpenGL
# 필요 시: winetricks -q vcrun6   (구형 MSVC 런타임 사용하는 게임 대비)
```

## 4. 오디오 / BGM (중요)

이 게임의 BGM은 **CD 음악을 `_inmm.dll`로 파일 재생으로 대체**하는 구조입니다.

```
_inmm.dll (게임이 직접 임포트) + _inmm.ini (파일 목록) + DOOGIE\_inmmserv.exe (별도 프로세스 재생)
+ 레지스트리 HKCU\SOFTWARE\irori\_inmm.dll 설정
```

- **Wine에서 동작할 가능성**: `_inmmserv.exe`는 일반 Win32 프로세스이고 waveOut을 사용하므로
  Wine에서 돌 여지가 있습니다. 다만 `_inmm.ini`의 상대경로(`DOOGIE\_inmmserv.exe`) 때문에
  **작업 디렉터리를 게임 폴더로** 잡아야 합니다(런처 스크립트에서 `cd` 처리).
- 첫 실행 시 레지스트리 등록이 필요할 수 있습니다(포트의 `data/DOOGIE/_inmm.reg`):
  ```bash
  box86 wine regedit /S "$GAMEDIR/data/DOOGIE/_inmm.reg"   # 상대경로 주의
  ```
- **실패 시 대안**: BGM 없이 진행(효과음/음성은 정상), 또는 추출한 음원을 별도 재생하는 방식 검토.

## 5. 성능 기대치

| 항목 | 기대 |
|---|---|
| 2D DirectDraw 블릿 | box86 계열에서 충분(원작 요구사양이 낮음) |
| 해상도 | 원작 640×480 → 기기 스케일링 필요(런처에서 창/스케일 옵션) |
| 첫 실행 | wine 프리픽스 생성 + 초기 셋업으로 **수 분** 소요(정상) |
| 이후 실행 | 수십 초 내 진입 |
| Hangover 경로 | 프레임 저하 가능(특히 맵 이동/전투 애니메이션) |

## 6. 실행 전략 요약 (권장 순서)

1. 기기의 32비트 지원 여부 확인 → **box86 경로인지 hangover인지 결정** (가장 중요)
2. 포트 설치(`Farland Tactics 3.sh` + `farlandtactics3/`) 후 `data/`에 게임 데이터 복사
3. 첫 실행으로 wine 프리픽스 생성 + `ddr=opengl` 적용
4. `log.txt`로 오류 확인 → [06-troubleshooting.md](06-troubleshooting.md)
5. 조작 매핑(.gptk) 튜닝 → [04-controls-gptokeyb.md](04-controls-gptokeyb.md)
6. BGM(inmm) 검증 → 안 되면 무음 진행 또는 대안 검토

## 7. 법적/배포 주의

- 게임 데이터(원판)는 **사용자가 보유한 것만** 사용하며, 이 프로젝트는 데이터를 배포하지 않습니다.
- 포트 패키지에는 **런처 스크립트·설정·문서만** 포함합니다(Wine/box86 바이너리도 포함하지 않음).
- 스크린샷/커버 이미지는 본인 플레이 화면으로 직접 캡처해 사용하세요.
