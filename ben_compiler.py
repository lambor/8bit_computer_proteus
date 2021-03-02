# compiler for ben eater's 8bit computer

import sys
import re

# NOP 0000 - no operation
# LDA xxxx - load data from address xxx to A register
# ADD 0000 - register A += register B
# SUB 0000 - register A -= register B
# STA xxxx - store data from register A to address xxxx
# LDI xxxx - load imidiate value to register A
# JMP xxxx - jmp to address xxxx
# LDB xxxx - load data from address xxx to B register
# JZ xxxx - jmp to address xxxx if zero flag on
# JC xxxx - jmp to address xxxx if carry flag on
# OUT 0000 - display A register value
# HLT 0000 - halt

#.BYTE xxxx - data byte

opcodes = {
    # 0000 NOP
    'NOP':0b0000,
    # 0001 LDA
    'LDA':0b0001,
    # 0010 ADD
    'ADD':0b0010,
    # 0011 SUB
    'SUB':0b0011,
    # 0100 STA
    'STA':0b0100,
    # 0101 LDI
    'LDI':0b0101,
    # 0110 JMP
    'JMP':0b0110,
    # 0111 LDB
    'LDB':0b0111,
    # 1000
    'JZ':0b1000,
    # 1001
    'JC':0b1001,
    # 1010
    # 1011
    # 1100
    # 1101
    # 1110 OUT
    'OUT':0b1110,
    # 1111 HLT
    'HLT':0b1111,
}

operands_num = [
    0,
    1,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    -1,
    -1,
    -1,
    -1,
    0,
    0
]

def compile(statements):
    result = []
    for s in statements:
        a = [word for word in re.split(r'\s+',s) if word]
        l = len(a)
        if l == 1 or l == 2:
            operator = a[0].upper()
            if operator.upper() == '.BYTE':
                result.append(0xff & eval(a[1]))
                continue
            code = opcodes[operator]
            if l != operands_num[code]+1:
                raise Exception('invalid operands number')
            code = (code << 4) | (0b0000 if l == 1 else (0b1111 & eval(a[1]) ))
            result.append(code & 0xff)
    return result


with open(sys.argv[1],'r') as f:
    codes = f.read().splitlines()
    codes = [s for s in codes if s]
    sys.stdout.buffer.write(bytes(compile(codes)))