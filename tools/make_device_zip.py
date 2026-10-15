#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
안드로이드 기기 배포용 zip 생성 (ASCII 경로 보장)

- 기기(/system/bin/unzip)에서 풀 때 한글 파일명 깨짐을 피하려고
  zip 내부 경로를 전부 ASCII 로 기록한다.
- zip 내부 최상위 폴더명을 지정할 수 있다 (예: FT3(K))
- 한글 파일명은 자동으로 ASCII 로 변환한다 (내용은 그대로 유지)

사용법:
  python make_device_zip.py <원본폴더> <출력zip> <내부루트명>
  예) python make_device_zip.py "F:\\DGGL\\Export\\파랜드택틱스3(K)" "F:\\DGGL\\Export\\FT3(K)_Winlator.zip" "FT3(K)"
"""
import os
import re
import sys
import zipfile

RENAME = {
    '_안드로이드_실행가이드.txt': '_READ_ME_KR.txt',
}

KOR = re.compile(r'[^\x20-\x7e]')


def ascii_name(name):
    if name in RENAME:
        return RENAME[name]
    if not KOR.search(name):
        return name
    # 한글 등 비ASCII → 안전한 ASCII 로
    base, ext = os.path.splitext(name)
    safe = re.sub(r'[^A-Za-z0-9._()\-]', '_', base)
    safe = re.sub(r'_+', '_', safe).strip('_') or 'file'
    return safe + ext


def build(src, dst, root_name):
    n = 0
    total = 0
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(src):
            rel = os.path.relpath(dirpath, src).replace('\\', '/')
            parts = [] if rel == '.' else rel.split('/')
            arc_dir = '/'.join([root_name] + [ascii_name(p) for p in parts])
            z.writestr(arc_dir + '/', b'')
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                arc = arc_dir + '/' + ascii_name(fn)
                with open(full, 'rb') as fp:
                    data = fp.read()
                z.writestr(arc, data)
                n += 1
                total += len(data)
    print('created: %s  (%d files, %.1f MB uncompressed, %.1f MB zip)'
          % (dst, n, total / 1048576.0, os.path.getsize(dst) / 1048576.0))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(0)
    build(sys.argv[1], sys.argv[2], sys.argv[3])
