#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""특정 오피코드의 핸들러(스텁→본체)와 그 본체가 부르는 리더 호출을 보여준다.
   사용: python scr_opshow.py <exe> <op(hex)> [op...]"""
import struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

R_FIELD, R_STR, R_U16, R_U32, R_VAR = 0x416441, 0x4175B0, 0x655C1C, 0x655C53, 0x655C89
NAMES = {R_FIELD: 'READ_FIELD(len,width)', R_STR: 'READ_STRING', R_U16: 'read_u16',
         R_U32: 'read_u32', R_VAR: 'read_var/u32'}


def sec_for(pe, va):
    rva = va - pe.OPTIONAL_HEADER.ImageBase
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s
    return None


def at(pe, va, n):
    s = sec_for(pe, va)
    if s is None:
        return None
    off = s.PointerToRawData + (va - pe.OPTIONAL_HEADER.ImageBase - s.VirtualAddress)
    return pe.__data__[off:off + n]


def main(path, ops):
    pe = pefile.PE(path, fast_load=True)
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    idx = at(pe, 0x656113, 40)
    tbl1 = [struct.unpack('<I', at(pe, 0x6560BB + i * 4, 4))[0] for i in range(22)]
    tbl2 = [struct.unpack('<I', at(pe, 0x416FF9 + i * 4, 4))[0] for i in range(0x7F)]

    for o in ops:
        op = int(o, 0)
        if op <= 0x28:
            stub = tbl1[idx[op - 1]]
        else:
            stub = tbl2[op - 0x40]
        print('=' * 70)
        print('op 0x%02X  스텁 0x%X' % (op, stub))
        code = at(pe, stub, 0x40)
        if not code:
            print('   (스텁 없음)'); continue
        target = None
        arg = None
        for i in md.disasm(code, stub):
            print('   %08X  %-7s %s' % (i.address, i.mnemonic, i.op_str))
            if i.mnemonic == 'push' and i.operands and i.operands[0].type == X86_OP_IMM:
                arg = i.operands[0].imm
            if i.mnemonic == 'call' and i.operands and i.operands[0].type == X86_OP_IMM:
                t = i.operands[0].imm
                if t not in NAMES:
                    target = t
                    break
        if not target:
            continue
        print('   --- 본체 0x%X (arg=%s) ---' % (target, arg))
        body = at(pe, target, 0x400)
        for i in md.disasm(body, target):
            note = ''
            if i.mnemonic == 'call' and i.operands and i.operands[0].type == X86_OP_IMM:
                t = i.operands[0].imm
                if t in NAMES:
                    note = '   <<< ' + NAMES[t]
            print('   %08X  %-7s %-42s%s' % (i.address, i.mnemonic, i.op_str, note))
            if i.mnemonic == 'ret':
                break


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
