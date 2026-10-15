#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Winlator 숏컷(.desktop) 생성

숏컷 = 컨테이너 홈의 `~/.local/share/applications/<이름>.desktop`
  [Desktop Entry]
  Exec=wine "<Windows 경로>"
  [Extra Data]  ← Winlator 전용 오버라이드
  controlsProfile=<입력 프로필 id>

사용법:
  python make_shortcut_desktop.py <출력파일> <표시이름> <Windows exe 경로> [controlsProfile] [extra...]
예:
  python make_shortcut_desktop.py FT3.desktop "파랜드 택틱스 3" "D:\\FT3(K)\\FT3K.EXE" 5
"""
import sys

TEMPLATE = """[Desktop Entry]
Exec=wine "{exe}"
Icon={icon}
StartupWMClass=

[Extra Data]
{extra}
"""


def build(exe, name='', controls_profile=None, icon='', extra=None):
    lines = []
    if controls_profile is not None:
        lines.append('controlsProfile=%d' % controls_profile)
    if extra:
        lines.extend(extra)
    return TEMPLATE.format(exe=exe, icon=icon, extra='\n'.join(lines))


if __name__ == '__main__':
    out = sys.argv[1]
    name = sys.argv[2]
    exe = sys.argv[3]
    prof = int(sys.argv[4]) if len(sys.argv) > 4 else None
    txt = build(exe, name, prof, extra=sys.argv[5:])
    with open(out, 'w', encoding='utf-8', newline='\n') as fp:
        fp.write(txt)
    print('created: %s (name=%s, exe=%s, controlsProfile=%s)' % (out, name, exe, prof))
    print(txt)
