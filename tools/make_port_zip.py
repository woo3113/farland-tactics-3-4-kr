#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PortMaster autoinstall zip builder

- zip 내부 경로 구분자를 항상 '/' 로 기록 (7-Zip/Compress-Archive 의 '\\' 문제 회피)
- 비-ASCII 파일명은 UTF-8 플래그로 기록
- .sh 파일은 LF 로 정규화해서 저장
- 게임 데이터(data/)는 포함하지 않음 (사용자가 직접 복사)

사용법:
  python make_port_zip.py <프로젝트루트> <포트폴더명> [outdir]
  예) python make_port_zip.py F:\\FarlandPort FarlandTactics3
"""
import json
import os
import sys
import zipfile


def norm_bytes(b):
    return b.replace(b'\r\n', b'\n')


def build(root, port, outdir='dist'):
    src = os.path.join(root, 'portmaster', port)
    jf = os.path.join(src, 'port.json')
    if not os.path.isfile(jf):
        raise SystemExit('port.json 없음: %s' % jf)
    with open(jf, encoding='utf-8') as fp:
        meta = json.load(fp)
    zipname = meta.get('name') or (port + '.zip')
    items = meta.get('items') or []

    os.makedirs(os.path.join(root, outdir), exist_ok=True)
    dst = os.path.join(root, outdir, zipname)
    if os.path.exists(dst):
        os.remove(dst)

    n_files = 0
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for it in items:
            p = os.path.join(src, it)
            if not os.path.exists(p):
                print('  ! 항목 없음:', it)
                continue
            if os.path.isdir(p):
                walked = False
                for dirpath, _dirnames, filenames in os.walk(p):
                    rel = os.path.relpath(dirpath, src).replace('\\', '/')
                    z.writestr(rel + '/', b'')      # 디렉터리 엔트리
                    walked = True
                    for fn in filenames:
                        full = os.path.join(dirpath, fn)
                        arc = rel + '/' + fn
                        with open(full, 'rb') as fp:
                            data = fp.read()
                        if fn.lower().endswith('.sh'):
                            data = norm_bytes(data)
                        z.writestr(arc, data)
                        n_files += 1
                if not walked:
                    z.writestr(it + '/', b'')
            else:
                with open(p, 'rb') as fp:
                    data = fp.read()
                if it.lower().endswith('.sh'):
                    data = norm_bytes(data)
                z.writestr(it, data)
                n_files += 1

    mb = os.path.getsize(dst) / 1048576.0
    print('created: %s  (%.2f MB, %d files)' % (dst, mb, n_files))
    print('')
    print('install folder (autoinstall):')
    print('  ROCKNIX/AmberELEC : /roms/ports/PortMaster/autoinstall/')
    print('  ArkOS             : /roms/tools/PortMaster/autoinstall/')
    print('  muOS              : /mmc/MUOS/PortMaster/autoinstall/')
    print('  Knulli            : /userdata/roms/ports/autoinstall')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(0)
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'dist')
