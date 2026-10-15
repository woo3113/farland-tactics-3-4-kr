# 06. 문제 해결 (Troubleshooting)

먼저 **로그**를 확인하세요: `/roms/ports/farlandtactics3/log.txt`

## 1. 실행/런처

| 증상 | 원인/조치 |
|---|---|
| "box86: not found" | 기기에 32비트 서브시스템이 없음 → **Hangover 경로**로 전환(`box64 wine ...`) |
| "wine: not found" | ROCKNIX/Aurknix dev 빌드에 wine 동봉, 또는 `.winecellar` 러너 사용 |
| 첫 실행이 멈춘 듯 | **정상**: wine 프리픽스 생성 + 초기 셋업(수 분). 기다리기 |
| 창이 뜨고 바로 종료 | `cd "$GAMEDIR/data"` 로 **작업 디렉터리**가 게임 폴더인지 확인(상대경로 문제) |
| `_FT3_Kor_Voice.exe` 실패 | VB6 스텁 → **`FT3K.EXE` 직접 실행**으로 우회 |
| "Script Error / Stack Pointer Abnormal" | SCR 관련 아님. wine 버전/프리픽스 초기화(프리픽스 삭제 후 재생성) |

## 2. 그래픽

| 증상 | 조치 |
|---|---|
| 팔레트/색상 깨짐 | `winetricks -q ddr=opengl` (wine DirectDraw 렌더러를 OpenGL로) |
| 화면이 아예 안 뜸 | `DDRAW` 오버라이드 확인: `WINEDLLOVERRIDES="ddraw,dinput,dsound=n,b"` |
| 창이 너무 작음/큼 | 원작 640×480 고정 → CFW 쪽 스케일/레터박스 설정 사용 |
| 검은 화면 + 소리만 | `fullscreen` 관련 옵션 조정, 또는 `virtual desktop` 활성(`winecfg`) |

## 3. 사운드 / BGM

| 증상 | 원인/조치 |
|---|---|
| 효과음·음성은 나오는데 **BGM 없음** | `_inmm.dll` 구조 문제(아래 4절) |
| 소리 자체가 없음 | `dsound` 오버라이드, `winecfg` 오디오 드라이버(ALSA/Pulse) 확인 |
| 소리 끊김 | CPU 경합 → `TASKSET`(PortMaster 제공) 사용 |

## 4. BGM(inmm) 상세

이 게임은 CD음악을 `_inmm.dll` + `_inmmserv.exe`(별도 프로세스)로 대체합니다.

1. `_inmm.ini` 에 파일 목록이 있고, 경로가 **게임 폴더 기준 상대경로**입니다
   → 런처에서 `cd "$GAMEDIR/data"` 필수
2. 레지스트리 설정이 필요할 수 있습니다.
   ```bash
   box86 wine regedit /S "$GAMEDIR/data/DOOGIE/_inmm.reg"
   ```
3. `_inmmserv.exe` 가 실행되는지 확인(작업 관리자 대신 `ps` / 로그)
4. 안 되면 대안:
   - 무음으로 진행(게임 진행에 지장 없음)
   - 추출한 BGM 파일을 별도 플레이어로 재생(비동기) — 자동화는 미구현

## 5. 조작

| 증상 | 조치 |
|---|---|
| 커서가 안 움직임 | `.gptk` 에 `left_analog_up = mouse_movement_up` 포함 여부 확인 |
| 커서가 너무 빠름 | `mouse_scale` 값 **증가** |
| 클릭이 씹힘 | `mouse_delay` 증가, `mouse_left` 매핑 확인 |
| 시작+셀렉트로 안 꺼짐 | `$GPTOKEYB "$EXEC" -c ...` 형식으로 띄웠는지 확인(앱 이름 인자 필요) |

## 6. 성능

| 증상 | 조치 |
|---|---|
| 전반적으로 느림 | 프리픽스를 **win32 + box86** 로(가능한 기기라면 hangover 대신) |
| 특정 구간 프레임 저하 | `WINEDEBUG=-all` 확인, 백그라운드 서비스 정리 |
| 첫 실행만 느림 | 프리픽스 캐시 문제 아님(정상) |

## 7. 초기화(깨졌을 때)

```bash
# 프리픽스 삭제 후 재생성 (세이브는 config/ 에 bind 되어 있으면 안전)
rm -rf ~/.wine32 ~/.wine64
```

## 8. 안드로이드(Winlator)에서 같은 증상일 때

- 팔레트 깨짐 → `dgVoodoo2` ddraw.dll 적용(zip 내 `_Winlator\dgVoodoo2`)
- BGM → `_inmm.reg` 등록
- 자세한 절차는 zip 안의 `_안드로이드_실행가이드.txt`
