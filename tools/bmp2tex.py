#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
게임 BMP(8bpp 팔레트) -> Dreamcast PVR 텍스처 데이터

출력:
  *.tex : width*height 바이트, 8bpp 선형(top-down). 트위들링은 KOS의
          pvr_txr_load_ex(..., PVR_TXRLOAD_8BPP) 가 처리한다.
  *.pal : 256 * 4바이트 little-endian uint32 ARGB8888 (pvr_set_pal_entry 용)

BMP는 bottom-up 이므로 top-down 으로 뒤집고, 팔레트 인덱스는 그대로 보존한다.

사용법:
  python bmp2tex.py <in.bmp> <out_prefix> [width height [offsetX offsetY]]
"""
import os, struct, sys


def load_bmp8(p):
    d = open(p, 'rb').read()
    assert d[:2] == b'BM', 'BMP 아님'
    off = struct.unpack_from('<I', d, 10)[0]
    hdrsz = struct.unpack_from('<I', d, 14)[0]
    w, h = struct.unpack_from('<ii', d, 18)
    bpp = struct.unpack_from('<H', d, 28)[0]
    comp = struct.unpack_from('<I', d, 30)[0]
    ncol = struct.unpack_from('<I', d, 46)[0]
    assert bpp == 8 and comp == 0, '8bpp 무압축만 지원 (bpp=%d comp=%d)' % (bpp, comp)
    if ncol == 0:
        ncol = 256
    pal = []
    for i in range(256):
        if i < ncol:
            b, g, r, _ = d[54 + i * 4:54 + i * 4 + 4]
        else:
            b = g = r = 0
        pal.append(0xFF000000 | (r << 16) | (g << 8) | b)
    flip = h > 0
    H = abs(h)
    stride = ((w + 3) // 4) * 4
    base = off
    rows = []
    for y in range(H):
        yy = (H - 1 - y) if flip else y
        rows.append(d[base + yy * stride: base + yy * stride + w])
    return w, H, pal, rows


def save(prefix, w, H, pal, rows, ox=0, oy=0, ow=None, oh=None, keygreen=False):
    ow = ow or w
    oh = oh or H
    if keygreen:
        for i, v in enumerate(pal):
            if (v & 0x00FFFFFF) == 0x0000FF00:      # 순수 초록 = 컬러키
                pal[i] = v & 0x00FFFFFF            # 알파 0
    out = bytearray()
    for y in range(oh):
        sy = oy + y
        if 0 <= sy < H:
            r = rows[sy]
            out += r[ox:ox + ow] + bytes(max(0, ow - len(r[ox:ox + ow])))
        else:
            out += bytes(ow)
    open(prefix + '.tex', 'wb').write(out)
    open(prefix + '.pal', 'wb').write(b''.join(struct.pack('<I', v) for v in pal))
    print('%s : %dx%d crop@(%d,%d) -> tex=%d bytes, pal=%d bytes'
          % (prefix, ow, oh, ox, oy, len(out), 256 * 4))


def main():
    a = sys.argv
    src, pre = a[1], a[2]
    w, H, pal, rows = load_bmp8(src)
    kw = '--keygreen' in a
    if len(a) >= 6 and a[3] != '--keygreen':
        ow, oh = int(a[3]), int(a[4])
        ox, oy = int(a[5]), int(a[6]) if len(a) >= 7 else 0
    else:
        ow, oh, ox, oy = w, H, 0, 0
    save(pre, w, H, pal, rows, ox, oy, ow, oh, kw)


if __name__ == '__main__':
    main()
