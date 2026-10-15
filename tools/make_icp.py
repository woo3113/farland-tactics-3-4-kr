#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Winlator 입력 프로필(.icp) 생성 — 파랜드 택틱스 3/4 용 (RP Classic 6버튼)

- 마우스 중심 게임이므로 D-패드 → 마우스 이동, 6버튼 → 마우스 클릭/확인/취소
- 물리 컨트롤러 바인딩은 .icp 안 'controllers' 배열에 기기 descriptor 로 저장된다.
- 오버레이는 비워 둔다(터치스크린도 그대로 커서로 쓸 수 있음)

Android KeyCode:
  A=96 B=97 X=99 Y=100 L1=102 R1=103 L2=104 R2=105 THUMBL=106 THUMBR=107 START=108 SELECT=109
  DPAD_UP=19 DOWN=20 LEFT=21 RIGHT=22
"""
import json
import sys

DESCRIPTOR = "dc75afea56e3c3a269b97967aa26b8c93c0bd3fb"   # Retroid Pocket Controller
DEVICE_NAME = "Retroid Pocket Controller"

# 물리 입력(keyCode) → Windows 이벤트(binding)
BINDINGS = [
    (19, "MOUSE_MOVE_UP"),      # D-패드 ↑ : 커서 위
    (20, "MOUSE_MOVE_DOWN"),    # D-패드 ↓ : 커서 아래
    (21, "MOUSE_MOVE_LEFT"),    # D-패드 ← : 커서 왼쪽
    (22, "MOUSE_MOVE_RIGHT"),   # D-패드 → : 커서 오른쪽
    (96, "MOUSE_LEFT_BUTTON"),  # A : 좌클릭(선택/이동/공격)
    (97, "MOUSE_RIGHT_BUTTON"),  # B : 우클릭(취소)
    (99, "KEY_ENTER"),          # X : 확인/대사 진행
    (100, "KEY_ESC"),           # Y : 취소/메뉴
    (102, "MOUSE_LEFT_BUTTON"),  # L1(6버튼 중 추가) : 좌클릭 보조
    (103, "KEY_ENTER"),         # R1(6버튼 중 추가) : 확인 보조
    (104, "KEY_F12"),           # L2 : FT3 던전 몬스터 토글 등
    (105, "KEY_SPACE"),         # R2 : 여유
    (106, "KEY_ENTER"),         # L3(뒷버튼)
    (107, "KEY_ESC"),           # R3(뒷버튼)
    (108, "KEY_ENTER"),         # START : 확인
    (109, "KEY_ESC"),           # SELECT : 취소
]


def build(profile_id=5, name="FarlandTactics", cursor_speed=1.5):
    binds = [{"keyCode": kc, "binding": b} for kc, b in BINDINGS]
    controller = {
        "id": DESCRIPTOR,
        "name": DEVICE_NAME,
        "controllerBindings": binds,
        "bindings": binds,          # 파서 키 이름 차이 대비(둘 다 기록)
    }
    return {
        "id": profile_id,
        "name": name,
        "cursorSpeed": cursor_speed,
        "elements": [],
        "controllers": [controller],
    }


if __name__ == '__main__':
    out = sys.argv[1]
    pid = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    nm = sys.argv[3] if len(sys.argv) > 3 else "FarlandTactics"
    prof = build(pid, nm)
    with open(out, 'w', encoding='utf-8', newline='\n') as fp:
        json.dump(prof, fp, ensure_ascii=False, separators=(',', ':'))
    print('created: %s  (id=%d, name=%s, bindings=%d)' % (out, pid, nm, len(BINDINGS)))
    for kc, b in BINDINGS:
        print('   keyCode %-4d -> %s' % (kc, b))
