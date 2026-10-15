#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""추출 결과 검증: 시그니처 분포 + BMP 헤더 유효성"""
import os, struct, collections, sys


def main(d):
    files = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
    sig = collections.Counter()
    bmp_ok = 0
    bmp_bad = 0
    samples = []
    msa_ok = 0
    for f in sorted(files):
        p = os.path.join(d, f)
        b = open(p, 'rb').read(64)
        sig[b[:4]] += 1
        if f.lower().endswith('.bmp'):
            if b[:2] == b'BM':
                size, w, h = struct.unpack_from('<Iii', b, 2)[:3] if False else (None, 0, 0)
                fsz = struct.unpack_from('<I', b, 2)[0]
                w, h = struct.unpack_from('<ii', b, 18)
                bpp = struct.unpack_from('<H', b, 28)[0]
                pal = struct.unpack_from('<I', b, 46)[0]
                real = os.path.getsize(p)
                if 1 <= w <= 4096 and 1 <= h <= 4096 and bpp in (1, 4, 8, 16, 24, 32):
                    bmp_ok += 1
                    if len(samples) < 8:
                        samples.append((f, real, fsz, w, h, bpp, pal))
                else:
                    bmp_bad += 1
            else:
                bmp_bad += 1
        elif f.lower().endswith('.msa') and b[:4] == b'MSAF':
            msa_ok += 1
    print('디렉터리:', d)
    print('파일 수:', len(files))
    print('선두 시그니처 상위:', [(k.hex(' '), v) for k, v in sig.most_common(6)])
    print('BMP 정상: %d / 비정상: %d   MSA 정상: %d' % (bmp_ok, bmp_bad, msa_ok))
    print('샘플 (name, 실제크기, 헤더크기, w, h, bpp, palette):')
    for s in samples:
        print('   ', s)


if __name__ == '__main__':
    main(sys.argv[1])
