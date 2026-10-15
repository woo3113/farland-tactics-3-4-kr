#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POC-B용: 원하는 크기의 BMP 후보 찾기 (PVR은 2의 거듭제곱 크기 필요)"""
import os, struct, glob, sys, collections


def info(p):
    b = open(p, 'rb').read(54)
    w, h = struct.unpack_from('<ii', b, 18)
    bpp = struct.unpack_from('<H', b, 28)[0]
    return w, h, bpp


def main(dirs):
    hist = collections.Counter()
    buckets = collections.defaultdict(list)
    for d in dirs:
        for f in glob.glob(os.path.join(d, '*.[bB][mM][pP]')):
            try:
                w, h, bpp = info(f)
            except Exception:
                continue
            hist[(w, h)] += 1
            if (w, h) in [(640, 480), (320, 240), (512, 512), (256, 256), (256, 224), (240, 320)]:
                buckets[(w, h)].append(os.path.basename(f))
    print('== 크기 상위 15 ==')
    for (w, h), c in hist.most_common(15):
        print('   %4dx%-4d %d개' % (w, h, c))
    print('== 관심 크기 샘플 ==')
    for k in sorted(buckets):
        print('   %s : %s' % (k, ', '.join(sorted(buckets[k])[:8])))


if __name__ == '__main__':
    main(sys.argv[1:] or [r'F:\DGGL\RE\extract\FT4_grp', r'F:\DGGL\RE\extract\FT3_grp', r'F:\DGGL\RE\extract\FT4_map'])
