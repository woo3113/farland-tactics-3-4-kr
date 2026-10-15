#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Winlator .container 의 graphicsDriver / dxwrapper / screenSize 를 바꾼다.

사용법:
  python set_gfx.py <in.json> <out.json> <graphicsDriver> [dxwrapper] [screenSize]
예:
  python set_gfx.py container.json out.json "virgl" "wined3d" "640x480"
"""
import json
import sys


def main(src, dst, gfx, dx='', size=''):
    with open(src, encoding='utf-8') as fp:
        c = json.load(fp)
    old = c.get('graphicsDriver')
    c['graphicsDriver'] = gfx
    if dx:
        c['dxwrapper'] = dx
    if size:
        c['screenSize'] = size
    with open(dst, 'w', encoding='utf-8') as fp:
        json.dump(c, fp, ensure_ascii=False, separators=(',', ':'))
    print('graphicsDriver: %s -> %s' % (old, c['graphicsDriver']))
    print('dxwrapper     : %s' % c.get('dxwrapper'))
    print('screenSize    : %s' % c.get('screenSize'))


if __name__ == '__main__':
    main(*sys.argv[1:6])
