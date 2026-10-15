#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Winlator APK 에서 UI 메뉴/문자열(영어/한국어) 확인"""
import re
import sys
import zipfile

APK = r'C:\Users\woo31\AppData\Local\Temp\opencode\Winlator_11.2.apk'
z = zipfile.ZipFile(APK)
names = z.namelist()

print('== res/menu 파일 ==')
for n in [x for x in names if x.startswith('res/menu')]:
    d = z.read(n).decode('utf-8', 'replace')
    ids = re.findall(r'android:(?:id|title)="([^"]+)"', d)
    print('  %s -> %s' % (n, ids))

print()
print('== values-ko(한국어) 존재 ==', [n for n in names if 'values-ko' in n][:5])


def load(path):
    if path not in names:
        return {}
    d = z.read(path).decode('utf-8', 'replace')
    return dict(re.findall(r'<string name="([^"]+)"[^>]*>(.*?)</string>', d, re.S))


en = load('res/values/strings.xml')
ko = load('res/values-ko/strings.xml')
print()
print('== 관련 문자열 (EN / KO) ==')
keys = [k for k in en if re.search(r'input|control|container|shortcut|settings|menu|profile', k, re.I)]
for k in sorted(keys)[:45]:
    print('   %-30s EN=%-26s KO=%s' % (k, en[k][:26], ko.get(k, '-')[:26]))
