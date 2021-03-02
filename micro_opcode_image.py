import sys

HLT = 0b1000000000000000 # halt
MI  = 0b0100000000000000 # input to RAM
MO  = 0b0010000000000000 # output from RAM
MA  = 0b0001000000000000 # input RAM address
AI  = 0b0000100000000000 # input to register A
AO  = 0b0000010000000000 # output from register A
BI  = 0b0000001000000000 # input to register B
FI  = 0b0000000100000000 # refresh flag register
SO  = 0b0000000010000000 # sum register output
SB  = 0b0000000001000000 # substract
CE  = 0b0000000000100000 # PC register enable
CO  = 0b0000000000010000 # PC register output
J   = 0b0000000000001000 # jmp(input to PC register)
OI  = 0b0000000000000100 # input to output register 
IO  = 0b0000000000000010 # output from instruction register
II  = 0b0000000000000001 # input to instruction register

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

_NOP = 0b0000
_LDA = 0b0001
_ADD = 0b0010
_SUB = 0b0011
_STA = 0b0100
_LDI = 0b0101
_JMP = 0b0110
_LDB = 0b0111
_JZ  = 0b1000
_JC  = 0b1001
_OUT = 0b1110
_HLT = 0b1111

SEQ_NUM = 4

SEQ_NUM_BITS = 0
n = SEQ_NUM-1
while n:
    n=n>>1
    SEQ_NUM_BITS += 1

# address format for micro_op_seq
# (0/1)       (0/1)        (0/1)      (xxxx)   (x*SEQ_NUM_BITS)
# (low/high) (zero flag) (carry flag) (opcode) (sequence index)
IMG_SIZE = 2**(1+1+1+4+SEQ_NUM_BITS)
micro_op_seq = [ 0 for i in range(IMG_SIZE)]

def set_seq_withflag(opcode,index,seq,flag):
    low = seq & 0xff
    high = (seq >> 8) & 0xff
    address_low = ((opcode&0b1111|((flag&0b11|0b000)<<4))<<SEQ_NUM_BITS)|index
    address_high = ((opcode&0b1111|((flag&0b11|0b100)<<4))<<SEQ_NUM_BITS)|index
    micro_op_seq[address_low] = low
    micro_op_seq[address_high] = high

def set_seq(opcode,index,seq):
    set_seq_withflag(opcode,index,seq,0b00)
    set_seq_withflag(opcode,index,seq,0b01)
    set_seq_withflag(opcode,index,seq,0b10)
    set_seq_withflag(opcode,index,seq,0b11)

# common fetch instruction phase
for i in range(16):
    # output PC to memory address reg
    set_seq(i,0,CO|MA)
    # output instruction code from memory to instruction reg, also inc PC
    set_seq(i,1,MO|II|CE)


# NOP

# LDA
# output address from instruction reg to memory address reg
set_seq(_LDA,2,IO|MA)
# output data from memory to reg A
set_seq(_LDA,3,MO|AI)

# ADD
#######################!!!!!!!#######################
# contention when simulating in proteus.
# ben eater is using 'SO | FI | AI' 
# But if 'SO | AI' is little ahead of 'FI', register A will reset with new value immediately after 'SO | AI',
# which will always reset zero and carry singal and you wont catch them
# So I worked around with 'FI' ahead
#######################!!!!!!!#######################
set_seq(_ADD,2,FI)
# output sum result from sum reg to reg A, also refresh flag reg
set_seq(_ADD,3,SO|AI)

# SUB
#######################!!!!!!!#######################
# similar bug in proteus simulation.
# also 'SB' must be setting in the two phases
#######################!!!!!!!#######################
# set substract flag
set_seq(_SUB,2,SB|FI)
# output substract result from sum reg to reg A, also refresh flag reg
set_seq(_SUB,3,SB|SO|AI)

# STA
# output address from instruction reg to memory address reg
set_seq(_STA,2,IO|MA)
# output data from reg A to memory
set_seq(_STA,3,AO|MI)

# LDI
# output immediate number from instruction reg to reg A
set_seq(_LDI,2,IO|AI)

# JMP
# output address from instruction reg to PC reg
set_seq(_JMP,2,IO|J)

# LDB
# output address from instruction reg to memory address reg
set_seq(_LDB,2,IO|MA)
# output data from memory to reg B
set_seq(_LDB,3,MO|BI)

# JZ
# output address from instruction reg to PC reg if zero flag is on
set_seq_withflag(_JZ,2,IO|J,0b10)
set_seq_withflag(_JZ,2,IO|J,0b11)

# JC
# output address from instruction reg to PC reg if carry flag is on
set_seq_withflag(_JC,2,IO|J,0b01)
set_seq_withflag(_JC,2,IO|J,0b11)

# OUT
# output data from reg A to output reg
set_seq(_OUT,2,AO|OI)

# HLT
# set halt flag on
set_seq(_HLT,2,HLT)


# print("opcode\t0\t1\t2\t3\t\n")
# for i in range(16):
#     j0 = ((i & 0b1111)<<SEQ_NUM_BITS)|0
#     j1 = ((i & 0b1111)<<SEQ_NUM_BITS)|1
#     j2 = ((i & 0b1111)<<SEQ_NUM_BITS)|2
#     j3 = ((i & 0b1111)<<SEQ_NUM_BITS)|3
#     s = "{:02X}\t{:02X}\t{:02X}\t{:02X}\t{:02X}\t".format(i,micro_op_seq[j0],micro_op_seq[j1],micro_op_seq[j2],micro_op_seq[j3])
#     print(s)
# print("-----------------------------------------------\n")
# for i in range(16):
#     j0 = ((i&0b1111|(1<<4))<<SEQ_NUM_BITS)|0
#     j1 = ((i&0b1111|(1<<4))<<SEQ_NUM_BITS)|1
#     j2 = ((i&0b1111|(1<<4))<<SEQ_NUM_BITS)|2
#     j3 = ((i&0b1111|(1<<4))<<SEQ_NUM_BITS)|3
#     s = "{:02X}\t{:02X}\t{:02X}\t{:02X}\t{:02X}\t".format(i,micro_op_seq[j0],micro_op_seq[j1],micro_op_seq[j2],micro_op_seq[j3])
#     print(s)


# print("\n=============================================\n")
# i = 0 
# while i < IMG_SIZE:
#     s = "\t"
#     for j in range(4):
#         s = s+"{:02X}\t".format(micro_op_seq[i])
#         i += 1
#     print(s)

sys.stdout.buffer.write(bytes(micro_op_seq))