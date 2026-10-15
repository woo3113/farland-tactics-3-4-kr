#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAC 엔트리 실제 레이아웃 정정판 (FT4.EXE 로더 실측 반영)

  data_start(i) = index[i].value + 4          (로더가 fseek(pos+4) 함)
  size(i)       = index[i+1].value - index[i].value
                  (마지막: filesize - index[i].value - 4)

블록 내용:
  'IEL1' + u32 decompressedSize + 압축스트림   -> sub_403ACF 로 해제
  그 외                                        -> raw 복사
"""
import os, struct, sys

MAGIC = b'PAC_FILE\x00'
CNT_OFF = 9
REC = 20
HDR = 13


def parse(path):
    data = open(path, 'rb').read()
    if data[:9] != MAGIC:
        raise ValueError('PAC_FILE 아님')
    count = struct.unpack_from('<I', data, CNT_OFF)[0]
    vals = []
    off = HDR
    for i in range(count):
        raw = data[off:off + REC]
        name = raw[:16].split(b'\x00')[0].decode('cp949', 'replace')
        vals.append((name, struct.unpack_from('<I', raw, 16)[0]))
        off += REC
    entries = []
    for i, (name, v) in enumerate(vals):
        if i + 1 < count:
            size = vals[i + 1][1] - v
        else:
            size = len(data) - v - 4
        start = v + 4
        entries.append((name, size, start))
    return data, entries


def block_info(data, name, size, start):
    b = data[start:start + size]
    if b[:4] == b'IEL1':
        dsize = struct.unpack_from('<I', b, 4)[0]
        return 'IEL1', dsize, b[8:]
    return 'RAW', size, b


def cmd_info(path):
    data, entries = parse(path)
    kinds = {}
    for name, size, start in entries:
        k, dsize, _ = block_info(data, name, size, start)
        kinds[k] = kinds.get(k, 0) + 1
    print('%s : %d entries  %s' % (os.path.basename(path), len(entries), kinds))
    for name, size, start in entries[:8]:
        k, dsize, payload = block_info(data, name, size, start)
        print('  %-16s block=%-6d %s dsize=%-8d payload=%s'
              % (name, size, k, dsize, payload[:12].hex(' ')))


def cmd_extract(path, outdir):
    data, entries = parse(path)
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for name, size, start in entries:
        k, dsize, payload = block_info(data, name, size, start)
        safe = name.replace('/', '_').replace('\\', '_')
        with open(os.path.join(outdir, safe + ('.' + k.lower() if k == 'IEL1' else '')), 'wb') as f:
            f.write(payload)
        n += 1
    print('extracted %d -> %s' % (n, outdir))


if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'info':
        cmd_info(sys.argv[2])
    elif m == 'extract':
        cmd_extract(sys.argv[2], sys.argv[3])
