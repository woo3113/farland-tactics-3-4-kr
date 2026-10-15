#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXE/DLL 안의 CP949 한글(및 ASCII) 문자열에서 레지스트리 관련 메시지를 찾는다."""
import re
import sys


def hangeul_runs(data, minchars=4):
    out = []
    i = 0
    n = len(data)
    while i < n - 1:
        b = data[i]
        if 0xB0 <= b <= 0xC8 and 0xA1 <= data[i + 1] <= 0xFE:
            s = i
            j = i
            while j < n - 1:
                b1, b2 = data[j], data[j + 1]
                if (0xB0 <= b1 <= 0xC8 and 0xA1 <= b2 <= 0xFE) or (0xA1 <= b1 <= 0xFE and 0xA1 <= b2 <= 0xFE):
                    j += 2
                else:
                    break
            if (j - s) // 2 >= minchars:
                try:
                    txt = data[s:j].decode('cp949')
                except Exception:
                    txt = ''
                if txt:
                    out.append((s, txt))
            i = j
        else:
            i += 1
    return out


KEYWORDS = ['레지스트', '등록', '설치', '시디', 'CD', '경로', '없습니다', '실행']


def main(paths):
    for p in paths:
        data = open(p, 'rb').read()
        print('== %s (%d bytes) ==' % (p, len(data)))
        hits = [(o, t) for o, t in hangeul_runs(data) if any(k in t for k in KEYWORDS)]
        for o, t in hits[:25]:
            print('   0x%06X  %s' % (o, t[:100]))
        if not hits:
            print('   (해당 키워드 한글 문자열 없음)')
        # ASCII 로 registry/Software 관련
        ascii_hits = re.findall(rb'[ -~]{5,}\x00', data)
        reg = [s[:-1].decode('latin-1') for s in ascii_hits
               if re.search(rb'Software|TGL|irori|inmm|Registry', s, re.I)]
        if reg:
            print('   --- ASCII(registry 관련) 상위 ---')
            for s in sorted(set(reg))[:12]:
                print('     %s' % s[:90])
        print()


if __name__ == '__main__':
    main(sys.argv[1:])
