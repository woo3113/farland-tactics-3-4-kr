#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows .reg (v5) → Wine user.reg 형식 변환 + 기존 user.reg 뒤에 병합

사용법:
  python reg2wine.py <user.reg> <출력파일> <.reg 파일들...>
"""
import re
import sys
import time

HIVE_MAP = [
    (re.compile(r'^HKEY_CURRENT_USER', re.I), ''),
    (re.compile(r'^HKCU', re.I), ''),
    (re.compile(r'^HKEY_LOCAL_MACHINE', re.I), 'HKLM'),
    (re.compile(r'^HKLM', re.I), 'HKLM'),
]


def parse_reg(path):
    """Windows .reg → [(키경로, [(이름, 타입, 값)])]"""
    raw = open(path, 'rb').read()
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        text = raw.decode('utf-16')
    else:
        try:
            text = raw.decode('cp949')
        except Exception:
            text = raw.decode('latin-1')
    out = []
    cur = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(';'):
            continue
        if line.upper().startswith('WINDOWS REGISTRY') or line.upper().startswith('REGEDIT'):
            continue
        if line.startswith('['):
            key = line.strip('[]')
            out.append([key, []])
            cur = out[-1]
            continue
        if cur is None or '=' not in line:
            continue
        name, val = line.split('=', 1)
        name = name.strip()
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
        if name == '@':
            name = ''
        if val.startswith('"'):
            v = val[1:-1].replace('\\\\', '\x00')          # 이스케이프 보존용 임시
            typ, wv = 's', v
        elif val.lower().startswith('dword:'):
            typ, wv = 'd', 'dword:%08x' % (int(val[6:], 16) & 0xFFFFFFFF)
        elif val.lower().startswith('hex'):
            typ, wv = 'x', val
        else:
            typ, wv = 's', val
        cur[1].append((name, typ, wv))
    return out


def wine_key(key):
    k = key
    for rx, pref in HIVE_MAP:
        if rx.match(k):
            k = rx.sub(pref, k, count=1)
            break
    k = k.strip('\\')
    return k.replace('\\', '\\\\')


def to_wine(entries):
    ts = int(time.time())
    buf = []
    for key, values in entries:
        buf.append('')
        buf.append('[%s] %d' % (wine_key(key), ts))
        buf.append('#time=%x' % (ts * 10000000))
        for name, typ, v in values:
            if typ == 's':
                v = v.replace('\x00', '\\\\')
                buf.append('"%s"="%s"' % (name, v))
            else:
                buf.append('"%s"=%s' % (name, v))
    return '\n'.join(buf) + '\n'


def main(user_reg, out, regs):
    with open(user_reg, encoding='utf-8', errors='replace') as fp:
        base = fp.read()
    if not base.endswith('\n'):
        base += '\n'
    keymap = {}          # 소문자 키 → (원래 키, values)  : 중복 제거(마지막 우선)
    order = []
    for r in regs:
        for key, values in parse_reg(r):
            lk = key.lower()
            if lk in keymap:
                keymap[lk] = (key, values)
            else:
                keymap[lk] = (key, values)
                order.append(lk)
    add = ['', ';;;;;;;; FarlandPort: 게임/INMM 레지스트리 주입 ;;;;;;;;']
    ts = int(time.time())
    for lk in order:
        key, values = keymap[lk]
        add.append('')
        add.append('[%s] %d' % (wine_key(key), ts))
        add.append('#time=%x' % (ts * 10000000))
        for name, typ, v in values:
            if typ == 's':
                v = v.replace('\x00', '\\\\')
                add.append('"%s"="%s"' % (name, v))
            else:
                add.append('"%s"=%s' % (name, v))
    out_txt = base + '\n'.join(add) + '\n'
    with open(out, 'w', encoding='utf-8', newline='\n') as fp:
        fp.write(out_txt)
    print('merged: %s (%d bytes) <- %d keys (중복제거 후)'
          % (out, len(out_txt), len(order)))
    for lk in order:
        key, values = keymap[lk]
        print('   %-50s %d values' % (key, len(values)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
