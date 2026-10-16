#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Winlator 입력 프로필(.icp) 생성 — 파랜드 택틱스 3/4 (마우스 중심 게임)

레포클(Retroid Pocket Classic, 스틱 없음)과 포켓맥스(MANGMI Pocket Max, 스틱 있음)
프리셋을 지원한다.

사용법:
    python make_icp.py <출력.icp> [profile_id] [preset]
    preset: retroid(기본) | pocketmax

스키마 근거 (winlator-app 소스 ExternalController.java / ExternalControllerBinding.java):
  - controllerBindings: [{"keyCode": <int>, "binding": "<Binding 이름>"}]
  - 버튼 keyCode: Android KeyEvent (A=96 B=97 X=99 Y=100 L1=102 R1=103 L2=104 R2=105
                  THUMBL=106 THUMBR=107 START=108 SELECT=109, DPAD 19/20/21/22)
  - 아날로그 축은 음수 keyCode 로 저장:
        AXIS X-  = -1   AXIS X+  = -2      (왼쪽 스틱 좌/우)
        AXIS Y-  = -3   AXIS Y+  = -4      (왼쪽 스틱 상/하)
        AXIS Z-  = -5   AXIS Z+  = -6      (오른쪽 스틱 좌/우)
        AXIS RZ- = -7   AXIS RZ+ = -8      (오른쪽 스틱 상/하)
    ※ getKeyCodeForAxis() 기준: X/Y 축 값이 양수면 X+/Y-, 음수면 X-/Y+
"""
import json
import sys

# ── 기기(컨트롤러) descriptor ────────────────────────────────────────────────
RETROID_DESC = "dc75afea56e3c3a269b97967aa26b8c93c0bd3fb"   # Retroid Pocket Controller
XBOX_DESC = "6dc63f813a1022bc62973a1a4c664c4c53b1c2c3"      # Xbox Wireless Controller (포켓맥스)
AIRX_DESC = "9e3e78dc958266481b45f720d74c77b8e971889c"      # AIR X Controller (포켓맥스)

# 버튼/십자키 (두 기기 공통)
# ★★ 이 게임은 "키보드 게임"이다 (게임 내 CONFIGURATION 화면 실측):
#     이동 = 방향키 / 결정·공격 = Z / 취소 = X / 결정·주문사용 = C
#     메뉴 = Space / 순서교체 = A,S / 방향전환 = Ctrl + 방향키
#   → 마우스 매핑은 쓰지 않는다.
BUTTON_BINDINGS = [
    (19, "KEY_UP"),              # D-패드 ↑ : 이동
    (20, "KEY_DOWN"),            # D-패드 ↓
    (21, "KEY_LEFT"),            # D-패드 ←
    (22, "KEY_RIGHT"),           # D-패드 →
    (96, "KEY_Z"),               # A : 결정/공격
    (97, "KEY_X"),               # B : 취소
    (99, "KEY_C"),               # X : 결정/주문사용
    (100, "KEY_SPACE"),          # Y : 메뉴
    (102, "KEY_ENTER"),          # L1 : 확인/대사 진행 (자주 씀)
    (103, "KEY_ESC"),            # R1 : 취소/나가기 (자주 씀)
    (104, "KEY_A"),              # L2 : 순서교체
    (105, "KEY_S"),              # R2 : 순서교체
    (106, "KEY_CTRL_L"),         # L3 : 방향전환 보조
    (107, "KEY_CTRL_R"),         # R3 : 방향전환 보조
    (108, "KEY_ENTER"),          # START : 결정
    (109, "KEY_ESC"),            # SELECT : 취소
]

# 왼쪽 아날로그 스틱 → 이동(방향키) (스틱 있는 기기만)
#   getKeyCodeForAxis(): X축 양수→-2, 음수→-1 / Y축 양수→-3, 음수→-4
LEFT_STICK_KEYS = [
    (-1, "KEY_LEFT"),            # AXIS X-
    (-2, "KEY_RIGHT"),           # AXIS X+
    (-3, "KEY_DOWN"),            # AXIS Y-
    (-4, "KEY_UP"),              # AXIS Y+
]

PRESETS = {
    "retroid": {
        "name": "FarlandTactics-RPClassic",
        "cursor_speed": 1.5,
        "controllers": [(RETROID_DESC, "Retroid Pocket Controller")],
        "with_stick": False,
    },
    "pocketmax": {
        "name": "FarlandTactics-PocketMax",
        "cursor_speed": 2.0,
        "controllers": [(XBOX_DESC, "Xbox Wireless Controller"),
                        (AIRX_DESC, "AIR X Controller")],
        "with_stick": True,
    },
}


def build(preset="retroid", profile_id=5):
    p = PRESETS[preset]
    binds = list(BUTTON_BINDINGS)
    if p["with_stick"]:
        binds += LEFT_STICK_KEYS
    binds = [{"keyCode": kc, "binding": b} for kc, b in binds]
    controllers = [{
        "id": desc,
        "name": dev_name,
        "controllerBindings": binds,
        "bindings": binds,          # 파서 키 이름 차이 대비(둘 다 기록)
    } for desc, dev_name in p["controllers"]]
    return {
        "id": profile_id,
        "name": p["name"],
        "cursorSpeed": p["cursor_speed"],
        "elements": [],
        "controllers": controllers,
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    out = sys.argv[1]
    pid = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    preset = sys.argv[3] if len(sys.argv) > 3 else "retroid"
    if preset not in PRESETS:
        print("preset 은 %s 중 하나" % ", ".join(PRESETS))
        sys.exit(1)
    prof = build(preset, pid)
    with open(out, 'w', encoding='utf-8', newline='\n') as fp:
        json.dump(prof, fp, ensure_ascii=False, separators=(',', ':'))
    n = len(prof["controllers"][0]["controllerBindings"])
    print('created: %s (preset=%s, id=%d, name=%s, controllers=%d, bindings=%d)'
          % (out, preset, pid, prof["name"], len(prof["controllers"]), n))
    for c in prof["controllers"]:
        print("   controller: %s (%s)" % (c["name"], c["id"]))
