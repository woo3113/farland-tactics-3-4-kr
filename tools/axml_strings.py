#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Winlator 메뉴 리소스(바이너리 XML)에서 문자열만 ASCII 로 추출"""
import re
import zipfile

z = zipfile.ZipFile(r'C:\Users\woo31\AppData\Local\Temp\opencode\Winlator_11.2.apk')
for n in ['res/menu/main_menu.xml', 'res/menu/shortcuts_menu.xml',
          'res/menu/containers_menu.xml', 'res/menu/container_popup_menu.xml',
          'res/menu/shortcuts_menu.xml']:
    try:
        d = z.read(n)
    except KeyError:
        continue
    runs = [m.group().decode('ascii') for m in re.finditer(rb'[\x20-\x7e]{4,60}', d)]
    # 중복 제거(순서 유지)
    seen = set()
    out = []
    for s in runs:
        if s not in seen:
            seen.add(s)
            out.append(s)
    print('== %s ==' % n)
    print('   ' + ' | '.join(out[:50]))
    print()
