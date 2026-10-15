#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Farland Tactics 3/4  PAC(IEL1) 디코더

sub_403ACF (FT4.EXE) 디스어셈블에서 복원한 고전 LZSS(Okumura LZSS.c) 변종:

  ring[4096], 초기값 ring[0 .. 4078-1] = 0x20, r = 4078
  flag = 0
  loop:
     if (flag & 0x100) == 0:  flag = 0xFF00 | *src++
     b = *src++;                        in_count++
     if in_count > dstlen: break
     if flag & 1:                       # 리터럴
         ring[r & 0xFFF] = b; *dst++ = b; r++
     else:                              # 매치
         c = *src++;                    in_count++
         if in_count > dstlen: break
         off  = ((c & 0xF0) << 4) | b   # 12비트
         n    = (c & 0x0F) + 3          # 3..18
         for _ in range(n):
             v = ring[off & 0xFFF]
             ring[r & 0xFFF] = v; *dst++ = v
             off++; r++
     flag >>= 1
"""
import os, struct, sys

MAGIC = b'PAC_FILE\x00'
CNT_OFF = 9
REC = 20
HDR = 13


def lzss_decompress(src, dstlen):
    ring = bytearray(b' ' * (4096 - 18)) + bytearray(18)
    r = 4096 - 18
    out = bytearray()
    flags = 0
    ip = 0
    n_in = 0
    n = len(src)
    while True:
        if (flags & 0x100) == 0:
            if ip >= n:
                break
            flags = 0xFF00 | src[ip]; ip += 1; n_in += 1
        if ip >= n:
            break
        b = src[ip]; ip += 1; n_in += 1
        if n_in > dstlen:
            break
        if flags & 1:
            ring[r & 0xFFF] = b
            out.append(b); r += 1
        else:
            if ip >= n:
                break
            c = src[ip]; ip += 1; n_in += 1
            if n_in > dstlen:
                break
            off = ((c & 0xF0) << 4) | b
            cnt = (c & 0x0F) + 3
            for _ in range(cnt):
                v = ring[off & 0xFFF]
                ring[r & 0xFFF] = v
                out.append(v); off += 1; r += 1
        flags >>= 1
        if len(out) >= dstlen:
            break
    return bytes(out)


def parse(path):
    data = open(path, 'rb').read()
    if data[:9] != MAGIC:
        raise ValueError('PAC_FILE 아님')
    count = struct.unpack_from('<I', data, CNT_OFF)[0]
    vals = []
    off = HDR
    for _ in range(count):
        raw = data[off:off + REC]
        name = raw[:16].split(b'\x00')[0].decode('cp949', 'replace')
        vals.append((name, struct.unpack_from('<I', raw, 16)[0]))
        off += REC
    entries = []
    for i, (name, v) in enumerate(vals):
        size = (vals[i + 1][1] - v) if i + 1 < count else (len(data) - v - 4)
        entries.append((name, size, v + 4))
    return data, entries


def decode_entry(data, size, start):
    blk = data[start:start + size]
    if blk[:4] == b'IEL1':
        dsize = struct.unpack_from('<I', blk, 4)[0]
        return lzss_decompress(blk[8:], dsize)
    return blk


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print('usage: pac_decode.py <pac> <outdir> [extfilter]')
        return
    pac, outdir = sys.argv[1], sys.argv[2]
    flt = sys.argv[3].lower() if len(sys.argv) > 3 else None
    data, entries = parse(pac)
    os.makedirs(outdir, exist_ok=True)
    ok = bad = 0
    for name, size, start in entries:
        if flt and not name.lower().endswith(flt):
            continue
        try:
            out = decode_entry(data, size, start)
        except Exception as e:
            print('  ! %s : %s' % (name, e)); bad += 1; continue
        safe = name.replace('/', '_').replace('\\', '_')
        open(os.path.join(outdir, safe), 'wb').write(out)
        ok += 1
    print('%s : %d개 해제 -> %s (실패 %d)' % (os.path.basename(pac), ok, outdir, bad))


if __name__ == '__main__':
    main()
