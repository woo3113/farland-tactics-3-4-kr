#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Winlator .container 의 drives 만 단일 항목으로 교정 (파싱 모호성 제거)"""
import json
import sys

p = sys.argv[1]
with open(p, encoding='utf-8') as fp:
    c = json.load(fp)
c['drives'] = 'D:/storage/emulated/0/Winlator'     # 단일 드라이브 = 모호성 없음
c['startupSelection'] = 0
c['screenSize'] = '640x480'
c['box64Preset'] = 'PERFORMANCE'
c['dxwrapper'] = 'wined3d'
out = sys.argv[2]
with open(out, 'w', encoding='utf-8') as fp:
    json.dump(c, fp, ensure_ascii=False, separators=(',', ':'))
print('drives ->', c['drives'])
