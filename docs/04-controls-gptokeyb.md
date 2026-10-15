# 04. 조작 매핑 (gptokeyb) 설계

파랜드 택틱스 3/4는 **마우스 중심** 게임입니다(이동/선택/공격/메뉴 대부분 좌클릭, 취소 우클릭).
따라서 `gptokeyb`로 **마우스 + 필수 키보드 키**를 매핑합니다.

## 1. gptokeyb 설정 형식(.gptk)

```
gamepad button = keyboard key 또는 mouse 동작
```
- 마우스 이동: `left_analog_up = mouse_movement_up` (한 축만 지정 — 좌/우 아날로그 중 하나만)
- 마우스 버튼: `a = mouse_left`, `b = mouse_right`
- 마우스 감도: `mouse_scale`(값이 클수록 **느림**), `mouse_delay`
- 정밀 이동: `r1 = mouse_slow`
- 종료: gptokeyb 실행 시 **Start+Select** 로 앱을 종료(런처에서 `$GPTOKEYB "$EXEC" -c ...`)

## 2. 이 프로젝트의 기본 매핑 (`farlandtactics3.gptk`)

| 패드 | 매핑 | 게임 내 기능 |
|---|---|---|
| 좌측 아날로그 | 마우스 이동 | 커서 이동 |
| A | 좌클릭 | 선택/이동/공격/확인 |
| B | 우클릭 | 취소/뒤로 |
| X | `enter` | 확인/대사 진행 |
| Y | `esc` | 메뉴/취소 |
| R1 | 마우스 느리게 | 정밀 커서 |
| L1 | 좌클릭(보조) | 연타 편의 |
| L2 | `f12` | (FT3) 던전 몬스터 토글 등 |
| R2 | `space` | (여유키) |
| 방향키 | 방향키 | 맵 스크롤/커서 미세 이동 |
| Start | `enter` | 확인 |
| Start+Select | 종료 | 포트 종료 |

## 3. 튜닝 포인트

| 증상 | 조치 |
|---|---|
| 커서가 너무 빠름/느림 | `mouse_scale` 조정 (8192 → 값↑ = 느림) |
| 커서 떨림 | `deadzone` / `deadzone_scale` 조정 |
| 클릭이 안 먹음 | `mouse_delay` 를 16~30 으로 |
| 방향키 스크롤이 필요 없음 | dpad 를 마우스 이동으로 전환(`dpad_mouse_step`) |
| 글자 입력(이름 입력) 필요 | gptokeyb `textinput` 옵션 + `TEXTINPUTINTERACTIVE=Y` |

## 4. gptokeyb2 (신형) 사용 시

CFW가 `gptokeyb2`를 쓰는 경우 `[config]`/`[controls]` 섹션 형식을 사용합니다.

```ini
[config]
mouse_scale = 6114
mouse_delay = 16
deadzone_mode = scaled_radial
deadzone = 2000

[controls]
a = mouse_left
b = mouse_right
x = enter
y = esc
r1 = mouse_slow
l2 = f12
start = enter
back = esc

dpad = mouse_movement
left_analog = mouse_movement
right_analog = arrow_keys repeat
```
- `gptokeyb2`가 없으면 구형 `.gptk`(1절 형식)를 그대로 사용합니다.
- 이 프로젝트는 **구형 형식**으로 작성했고, 필요 시 위 블록으로 변환하면 됩니다.

## 5. 확인 방법

1. 포트 실행 후 커서가 움직이는지 확인
2. 클릭/우클릭이 먹는지 확인
3. `log.txt` 에 gptokeyb 관련 오류가 없는지 확인
4. 필요 시 `-v` 로 gptokeyb 상세 로그 활성화
