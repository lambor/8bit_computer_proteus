import sys

output = [0 for i in range(64*1024)]
decimals = [0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b]

# 0 ~ 255
for i in range(256):
    output[i|0x000] = decimals[i%10]
    output[i|0x100] = decimals[i//10%10]
    output[i|0x200] = decimals[i//100]

# -128 ~ 127
for i in range(-128,128):
    j = abs(i)
    output[(i&0xff)|0x400] = decimals[j%10]
    output[(i&0xff)|0x500] = decimals[j//10%10]
    output[(i&0xff)|0x600] = decimals[j//100]
    output[(i&0xff)|0x700] = 0x01 if i<0 else 0

sys.stdout.buffer.write(bytes(output))