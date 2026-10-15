#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCR 디스어셈블러 (Farland Tactics 3/4)

확실한 부분 (로더/VM 디스어셈블로 검증됨)
  1) 컨테이너: "EV"(UTF-16LE) + u32 fileSize + u32 vars[256] + 코드스트림(0x408~)
  2) 텍스트  : FE <len> <CP949 문자열>  (발화자/대사 후보)
  3) 오피코드 범위: 0x01..0x28 (1차 VM), 0x40..0xBE (2차 VM)
  4) 1차 VM 명령 크기(부분 실측): op0x01=3, op0x02=3, op0x03=6, op0x10..0x1F=3 등

주의
  코드 영역은 단일 고정길이 명령 스트림이 아니다(stride 검정 결과 정렬 없음).
  → 구조화 데이터 + 텍스트 혼합. 명령 단위 전개는 VM 실행 추적이 필요하다.
  이 도구는 텍스트/변수/구조 덤프와 '잠정' 명령 해석까지 제공한다.

사용법:
  python scr_disasm.py <scr파일> [--hex] [--vars] [--text] [--insn] [--all]
"""
import struct, sys

SIZE1 = {op: 3 for op in range(1, 0x29)}
SIZE1.update({0x01: 3, 0x02: 3, 0x03: 6, 0x04: 3, 0x05: 3, 0x06: 4, 0x07: 4,
              0x08: 4, 0x09: 4, 0x0A: 3, 0x0B: 3, 0x27: 1})


def parse(path):
    d = open(path, 'rb').read()
    if d[:4] != b'E\x00V\x00':
        raise ValueError('EV 시그니처 아님')
    size = struct.unpack_from('<I', d, 4)[0]
    vars_ = list(struct.unpack_from('<256I', d, 8))
    code = d[0x408:]
    return d, size, vars_, code


def show_vars(vars_):
    nz = [(i, v) for i, v in enumerate(vars_) if v]
    print('[vars] 0이 아닌 항목 %d / 256' % len(nz))
    for i, v in nz[:40]:
        print('   vars[%3d] = %-12d (0x%X)' % (i, v, v))
    if len(nz) > 40:
        print('   ... (%d개 더)' % (len(nz) - 40))


def show_text(code):
    print('[text] FE <len> <CP949> 패턴')
    n = 0
    i = 0
    while i < len(code) - 2:
        if code[i] == 0xFE:
            ln = code[i + 1]
            if 2 <= ln <= 200 and i + 2 + ln <= len(code):
                try:
                    s = code[i + 2:i + 2 + ln].decode('cp949')
                    if sum(1 for c in s if '\uac00' <= c <= '\ud7a3') >= 2:
                        print('   0x%06X  len=%-3d  %s' % (i, ln, s.replace('\n', '\\n')))
                        n += 1
                        i += 2 + ln
                        continue
                except Exception:
                    pass
        i += 1
    print('   총 %d개' % n)


def show_hex(code, limit=4096):
    print('[hex] 코드 영역 (CP949 열 포함)')
    lim = min(len(code), limit)
    for o in range(0, lim, 16):
        c = code[o:o + 16]
        h = ' '.join('%02X' % b for b in c)
        a = ''.join(chr(b) if 32 <= b < 127 else '.' for b in c)
        try:
            k = ''.join(ch if '\uac00' <= ch <= '\ud7a3' else '.'
                        for ch in c.decode('cp949', 'replace'))
        except Exception:
            k = '.' * len(c)
        print('  %06X  %-47s  %-16s %s' % (o, h, a, k))


def _load_specs():
    import importlib.util, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'scr_specs_dict.py')
    p = os.path.abspath(p)
    if not os.path.exists(p):
        return {}
    spec = importlib.util.spec_from_file_location('specs', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return getattr(m, 'SPECS', {})


def show_insn(code, limit=300):
    """SPECS(핸들러 분석 결과)를 이용한 명령 단위 디스어셈블"""
    SPECS = _load_specs()
    print('[insn] 명령 디스어셈블 (SPECS %d개 오피코드)' % len(SPECS))
    if not SPECS:
        print('   (scr_opspec2.py 를 먼저 실행해 docs/scr_specs_dict.py 를 생성하세요)')
        return
    ip = 0
    n = 0
    while ip < len(code) and n < limit:
        op = code[ip]
        if op == 0x00:
            print('   %06X  00                ; padding' % ip)
            ip += 1
            n += 1
            continue
        sp = SPECS.get(op)
        if not sp:
            print('   %06X  %02X                ; UNKNOWN' % (ip, op))
            ip += 1
            n += 1
            continue
        ops, mode = sp
        cur = 1
        parts = []
        for kind, w in ops:
            if kind == 'str':
                if ip + cur >= len(code):
                    break
                ln = code[ip + cur]
                cur += 1
                raw = code[ip + cur:ip + cur + ln]
                cur += ln
                try:
                    parts.append('"%s"' % raw.decode('cp949'))
                except Exception:
                    parts.append('"%s"' % raw.hex())
            elif kind == 'tagged':
                tag = code[ip + cur] if ip + cur < len(code) else 0
                cur += 1
                v = int.from_bytes(code[ip + cur:ip + cur + w], 'little')
                cur += w
                parts.append('vars[%d]' % v if tag == 0 else str(v))
            else:
                v = int.from_bytes(code[ip + cur:ip + cur + w], 'little')
                cur += w
                parts.append(str(v))
        print('   %06X  %02X  %-4s %s' % (ip, op, '', ', '.join(parts)))
        ip += max(cur, 1)
        n += 1


def main():
    path = sys.argv[1]
    d, size, vars_, code = parse(path)
    print('== %s ==' % path)
    print('[hdr] sig=EV  fileSizeField=%d  실제=%d  코드영역=%d 바이트' % (size, len(d), len(code)))
    flags = sys.argv[2:]
    if not flags or '--all' in flags or '--vars' in flags:
        show_vars(vars_)
    if not flags or '--all' in flags or '--text' in flags:
        show_text(code)
    if '--hex' in flags or '--all' in flags:
        show_hex(code)
    if '--insn' in flags or '--all' in flags:
        show_insn(code)


if __name__ == '__main__':
    main()
