#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resources.arsc 에서 UI 라벨 문자열 추출 (메뉴 이름 확인용)"""
import re
import zipfile

z = zipfile.ZipFile(r'C:\Users\woo31\AppData\Local\Temp\opencode\Winlator_11.2.apk')
arsc = z.read('resources.arsc')
print('resources.arsc size = %d' % len(arsc))

# UTF-8(1바이트) 및 UTF-16LE 문자열 후보
ascii_runs = set()
for m in re.finditer(rb'[\x20-\x7e]{5,40}', arsc):
    ascii_runs.add(m.group().decode('ascii'))
utf16_runs = set()
for m in re.finditer(rb'(?:[\x20-\x7e]\x00){5,40}', arsc):
    try:
        utf16_runs.add(m.group().decode('utf-16-le'))
    except Exception:
        pass

allstr = ascii_runs | utf16_runs
print('추출 문자열: ascii=%d utf16=%d' % (len(ascii_runs), len(utf16_runs)))

want = ['Input Control', 'Container', 'Shortcut', 'Settings', 'About', 'Exit',
        'Export', 'Import', 'Contents', 'Box64', 'Wine', 'Graphic', 'Screen',
        'Controls', 'Profile', 'Drive', 'Add', 'Remove', 'Create', 'Edit']
print()
print('== 관심 라벨 ==')
for s in sorted(allstr):
    if any(w.lower() in s.lower() for w in want) and ' ' in s and len(s) < 40:
        print('   ', s)
