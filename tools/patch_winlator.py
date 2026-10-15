#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Winlator 컨테이너/시작메뉴 패치

- .container : drives 를 게임 폴더로 교정 (D: -> /storage/emulated/0/Winlator)
               startupSelection 을 0(Normal)으로 (오디오/서비스 호환)
- .startmenu: 파랜드 택틱스 3/4 바로가기 추가

사용법:
  python patch_winlator.py <container.json> <startmenu.json> <출력폴더>
"""
import json
import os
import sys

DEV_GAME_DIR = "/storage/emulated/0/Winlator"
DEV_STORAGE = "/data/data/com.winlator/storage"

SHORTCUTS = [
    {"name": "파랜드 택틱스 3", "path": "D:/FT3(K)/FT3K.EXE"},
    {"name": "파랜드 택틱스 4", "path": "D:/FT4(K)/FT4.EXE"},
]


def build_drives():
    # 형식: <드라이브문자>:<장치경로> 를 이어붙임 (Winlator 규약)
    return "D:%sE:%s" % (DEV_GAME_DIR, DEV_STORAGE)


def main(cont_path, menu_path, outdir):
    os.makedirs(outdir, exist_ok=True)

    # --- .container ---
    with open(cont_path, encoding='utf-8') as fp:
        c = json.load(fp)
    old_drives = c.get('drives')
    c['drives'] = build_drives()
    c['startupSelection'] = 0          # 0=Normal (오디오 서비스 포함)
    c['name'] = c.get('name') or 'FT3'
    if c.get('screenSize') != '640x480':
        c['screenSize'] = '640x480'
    c.setdefault('box64Preset', 'PERFORMANCE')
    out_c = os.path.join(outdir, 'container_new.json')
    with open(out_c, 'w', encoding='utf-8') as fp:
        json.dump(c, fp, ensure_ascii=False, separators=(',', ':'))
    print('container  : drives  %s  ->  %s' % (old_drives, c['drives']))
    print('             startupSelection -> %s, screenSize=%s, box64=%s'
          % (c['startupSelection'], c['screenSize'], c['box64Preset']))

    # --- .startmenu ---
    with open(menu_path, encoding='utf-8') as fp:
        m = json.load(fp)
    # 기존 '파랜드 택틱스' 그룹이 있으면 교체
    m = [g for g in m if g.get('name') != '파랜드 택틱스']
    m.append({"name": "파랜드 택틱스", "children": SHORTCUTS})
    out_m = os.path.join(outdir, 'startmenu_new.json')
    with open(out_m, 'w', encoding='utf-8') as fp:
        json.dump(m, fp, ensure_ascii=False, separators=(',', ':'))
    print('startmenu  : 그룹 %d개 -> 바로가기 추가 %s'
          % (len(m), [s['name'] for s in SHORTCUTS]))
    print('출력:', out_c, ',', out_m)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
