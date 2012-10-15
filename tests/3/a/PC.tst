// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/03/a/PC.tst

load PC.hdl,
output-file PC.out,
compare-to PC.cmp,
output-list time%S1.4.1 in%D1.6.1 reset%B2.1.2 load%B2.1.2 inc%B2.1.2 out%D1.6.1;

// (I added 'set reset 1' to mostly mask logsim's divergence from
// TECS. The TECS HDL simulator makes all signals initially 0, while in
// logsim they're undetermined ('?'). By explicitly resetting the
// register at the start, we limit the difference in the trace to just
// that reset signal. TODO: something less hacky.)
set in 0,
set reset 1,
set load 0,
set inc 0,
tick,
output;

tock,
output;

set reset 0,    // (to undo the above hack)
set inc 1,
tick,
output;

tock,
output;

set in -32123,
tick,
output;

tock,
output;

set load 1,
tick,
output;

tock,
output;

set load 0,
tick,
output;

tock,
output;

tick,
output;

tock,
output;

set in 12345,
set load 1,
set inc 0,
tick,
output;

tock,
output;

set reset 1,
tick,
output;

tock,
output;

set reset 0,
set inc 1,
tick,
output;

tock,
output;

set reset 1,
tick,
output;

tock,
output;

set reset 0,
set load 0,
tick,
output;

tock,
output;

set reset 1,
tick,
output;

tock,
output;

set in 0,
set reset 0,
set load 1,
tick,
output;

tock,
output;

set load 0,
set inc 1,
tick,
output;

tock,
output;

set in 22222,
set reset 1,
set inc 0,
tick,
output;

tock,
output;
