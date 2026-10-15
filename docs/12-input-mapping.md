# 12. 입력(키) 매핑 — Retroid Pocket Classic 6버튼

파랜드 택틱스 3/4는 **마우스 중심** 게임입니다. RP 클래식은 **아날로그 스틱이 없고 6버튼**이므로,
물리 버튼 → 마우스/키보드로 변환해야 합니다.

## 1. 기기 입력 사실 (실측)

| 항목 | 값 |
|---|---|
| Android InputDevice | `8: Retroid Pocket Controller` (KEYBOARD\|GAMEPAD\|JOYSTICK) |
| Descriptor | `dc75afea56e3c3a269b97967aa26b8c93c0bd3fb` |
| 6버튼 보고 방식 | A·B·X·Y (4개) + **L1·R1 (추가 2개)** |
| 추가 버튼 | L2·R2 (숄더), L3·R3 (뒷버튼: THUMBL/THUMBR), START, SELECT |
| 스틱 | 없음 (터치스크린/D-패드만) |

## 2. Winlator 입력 프로필(.icp) 구조

- 저장 위치: `/data/data/com.winlator/files/profiles/controls-<id>.icp`
- 필드: `id`, `name`, `cursorSpeed`, `elements[]`, `controllers[]`
- 물리 컨트롤러 바인딩은 **profile 안**에 저장된다(전역 아님)
  ```json
  "controllers":[{"id":"<descriptor>","name":"<기기명>",
     "controllerBindings":[{"keyCode":96,"binding":"MOUSE_LEFT_BUTTON"}]}]
  ```
- 바인딩 값: `MOUSE_LEFT_BUTTON`, `MOUSE_RIGHT_BUTTON`, `MOUSE_MOVE_UP/DOWN/LEFT/RIGHT`,
  `MOUSE_SCROLL_UP/DOWN`, `KEY_*`(예: `KEY_ENTER`, `KEY_ESC`, `KEY_F12`), `GAMEPAD_*`(패스스루)
- 요소 타입: `BUTTON`, `D_PAD`, `STICK`, `TRACKPAD`, `RANGE_BUTTON`, `RADIAL_MENU`

## 3. 적용한 매핑 (`FarlandTactics` 프로필, id=5)

| RP Classic 버튼 | keyCode | binding | 게임 동작 |
|---|---|---|---|
| D-패드 ↑ / ↓ / ← / → | 19/20/21/22 | `MOUSE_MOVE_UP/DOWN/LEFT/RIGHT` | 커서 이동 |
| **A** | 96 | `MOUSE_LEFT_BUTTON` | 선택 / 이동 / 공격 |
| **B** | 97 | `MOUSE_RIGHT_BUTTON` | 취소 / 뒤로 |
| **X** | 99 | `KEY_ENTER` | 확인 / 대사 진행 |
| **Y** | 100 | `KEY_ESC` | 메뉴 / 취소 |
| **L1** (6버튼 중 추가) | 102 | `MOUSE_LEFT_BUTTON` | 좌클릭 연타 편의 |
| **R1** (6버튼 중 추가) | 103 | `KEY_ENTER` | 확인 보조 |
| L2 (숄더) | 104 | `KEY_F12` | FT3 던전 몬스터 토글 등 |
| R2 (숄더) | 105 | `KEY_SPACE` | 여유 |
| L3 / R3 (뒷버튼) | 106/107 | `KEY_ENTER` / `KEY_ESC` | 보조 |
| START / SELECT | 108/109 | `KEY_ENTER` / `KEY_ESC` | 확인 / 취소 |

- `cursorSpeed = 1.5` (D-패드 커서 이동 속도 — 너무 빠르면 낮추세요)
- `elements = []` → **오버레이 없음**. 터치스크린은 그대로 커서로 사용.
  (터치가 커서로 안 움직이면 `TRACKPAD` 요소를 추가해야 합니다 → 아래 5번)

## 4. 생성/적용 (ADB, 재현 가능)

```powershell
$adb = "C:\Users\woo31\Android\Sdk\platform-tools\adb.exe"
python tools/make_icp.py controls-5.icp 5 FarlandTactics     # .icp 생성
& $adb shell "am force-stop com.winlator"
& $adb shell "run-as com.winlator mkdir -p /data/data/com.winlator/files/profiles"
& $adb push controls-5.icp /data/local/tmp/
& $adb shell "run-as com.winlator cp /data/local/tmp/controls-5.icp /data/data/com.winlator/files/profiles/"
```

### 앱에서 연결 (2단계)
1. **Input Controls** → 목록에서 `FarlandTactics` 선택
2. 숏컷에 지정: 홈 화면에서 숏컷 **길게 누름 → Settings → Controls Profile → FarlandTactics**

> 숏컷이 없으면: Containers → 컨테이너 → Explorer → `D:\FT3(K)\FT3K.EXE` 를 길게 눌러 숏컷 생성.

## 5. 문제 시

| 증상 | 조치 |
|---|---|
| Input Controls 목록에 프로필이 안 보임 | 앱 재시작. 그래도 없으면 **앱에서 새 프로필을 만들고 물리 버튼을 한 번 눌러 한 개 바인딩을 저장**한 뒤, 그 파일을 기준으로 나머지를 채우면 됨(스키마가 확실해짐) |
| 버튼이 반응 없음 | 숏컷에 프로필이 지정됐는지 확인(4-2). 컨트롤러가 `Retroid Pocket Controller`로 잡히는지 확인 |
| 커서가 너무 빠름/느림 | `.icp` 의 `cursorSpeed` 조정(0.5~3) |
| 터치로 커서가 안 움직임 | `.icp` `elements` 에 `TRACKPAD` 추가 필요 |
| 게임이 키 입력을 요구 | `BUTTON` 요소를 추가해 `KEY_*` 바인딩을 화면에 배치 |

## 6. 참고: 6버튼 시스템(새턴/제네시스) 매핑

RP 클래식 6은 새턴/제네시스 6버튼용으로 설계된 기기입니다. 다른 에뮬레이터에서는
A·B·X·Y + **C/Z = L1/R1** 조합이 일반적이며, RetroArch에서는 `L3/R3`(뒷버튼)을 C/Z로 쓰는 구성도 널리 쓰입니다.
이 프로젝트(마우스 게임)에서는 위 3번 매핑이 목적에 맞게 재배치한 것입니다.
