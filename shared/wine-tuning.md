# 공유 코어 — Wine 튜닝 값 (두 플랫폼 공통)

이 게임은 **32비트 + DirectDraw** 라는 두 가지 특성이 모든 설정의 기준입니다.
아래 값은 PortMaster(리눅스)와 Winlator(안드로이드) **양쪽에 같은 개념으로 적용**됩니다.

## 1. 프리픽스 아키텍처 = 32비트

```
WINEARCH = win32
WINEPREFIX = ~/.wine32        (PortMaster)
             (Winlator 컨테이너 내부 prefix)
```
- 근거: `FT3K.EXE`, `FT4.EXE` 는 **PE32**(32비트). `PE32+`(64비트) 아님.
- 런처 스크립트에서 `file "$EXE" | grep PE32` 로 자동 판별해도 됩니다.

## 2. DLL 오버라이드

```
WINEDLLOVERRIDES="ddraw,dinput,dsound=n,b"
```
- `n,b` = native 우선, 없으면 builtin → **wine 내장 wined3d/ddraw를 쓰게** 유도.
- `_inmm.dll` 은 **게임 폴더 안에 있는 로컬 DLL**이라 오버라이드 대상이 아닙니다.

## 3. DirectDraw 렌더러

| 플랫폼 | 설정 |
|---|---|
| PortMaster(리눅스) | `winetricks -q ddr=opengl` — DirectDraw를 OpenGL(GL4ES 경로)로 렌더 |
| Winlator(안드로이드) | ① wine 내장 ddraw 먼저 시도 ② 색상 깨지면 **dgVoodoo2**(`ddraw.dll`+`D3DImm.dll`+`dgVoodoo.conf`) ③ DDrawCompat |

> PortMaster 기기에는 **Vulkan이 없어 dgVoodoo2/DXVK 부적합** → `ddr=opengl` 이 정답.
> 안드로이드는 Vulkan/DXVK가 가능하므로 선택지가 더 넓습니다.

## 4. 공통 환경변수

```
WINEDEBUG=-all                      # 로그 소음 제거(성능)
SDL_GAMECONTROLLERCONFIG=<...>      # PortMaster: control.txt 제공값 사용
```
- 디버깅 시에는 `WINEDEBUG=+ddraw` 등으로 좁혀서 확인.

## 5. 실행 규칙

1. **작업 디렉터리 = 게임 폴더** (BGM/음성/`_inmm` 상대경로)
2. **첫 실행은 느림** — wine 프리픽스 생성(수 분). 정상 동작.
3. 오디오: 소리가 없으면 `winecfg` 에서 오디오 드라이버 확인(ALSA/Pulse).
4. 해상도: 원작 **640×480** → 기기 스케일링/레터박스 설정 사용.

## 6. 진단 순서 (양 플랫폼 동일)

```
1) 실행 자체가 안 됨        → 로그 확인 (PortMaster: logs/log.txt)
                             → 러너 존재 여부(box86/box64/와인), 프리픽스 재생성
2) 실행되는데 화면 깨짐     → ddr=opengl (리눅스) / dgVoodoo2 (안드로이드)
3) 소리 안 남              → winecfg 오디오, dsound 오버라이드
4) BGM만 안 남             → _inmm 구조(정상적 실패 모드) → 무음 진행 가능
5) 클릭/커서 문제          → 조작 매핑 (PortMaster: .gptk / 안드로이드: 터치 오버레이)
```

## 7. BGM(inmm) 관련 공통 사실

- 게임은 `_inmm.dll` + `_inmmserv.exe`(별도 프로세스) + `HKCU\SOFTWARE\irori\_inmm.dll` 레지스트리로
  CD음악을 파일로 대체합니다.
- 두 환경 모두 **검증 필요**하며, 실패 시 게임은 **무음 BGM으로 정상 진행**됩니다.
- 등록 시도(선택):
  ```
  wine regedit /S "DOOGIE\_inmm.reg"      # 작업 디렉터리 = 게임 폴더에서
  ```
