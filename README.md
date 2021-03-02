# 8bit_computer_proteus
ben eater's 8bit computer simulation in proteus

### image files for eproms in project

`python decimal_display_image.py > decimal_display.BIN`

*decimal_display.BIN* is the image file for the 27C64 eprom 'U16'.
You can find it in 'Output Display' section.

`python micro_opcode_image.py > micro.BIN`

*micro.BIN* is the image file for the 27C64 eprom 'MICRO_OP1' and 'MICRO_OP2'.
You can find them in 'Control Logic & Microcode' section.

`python ben_compiler.py test.bc > test.BIN`

*test.BIN* is the test program for this computer. It must be set in the 27C64 eprom 'U1' which is embedded in the 'Memory Programmer'.
Right click on 'Memory Programmer' and 'Goto Child Sheet', you will find the eprom.

*test.BIN* will be written to this computer's 'RAM' during simulation by hand.
You should set the 'Bus/Manual(0/1) switch' and set the 'Reset' switch before simulation to enable the 'Memory Programmer',
then 'test.BIN' will be written to 'RAM' initially in simulation.

When the write is finished (the 'manual write signal input' is not flashing), you can unset the 'Bus/Manual(0/1) switch' to enable the 'RAM',
and unset 'Reset' to let the computer run (if the clock is working).
