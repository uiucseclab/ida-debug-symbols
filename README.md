How to run this:

First run gdb on main. You will see that when it crashes, it gives a nonsensical name and the address of the function. This makes it hard to add
breakpoints and in general debug. With this, you can open the binary in IDA and rename the functions, so that in gdb, you can actually see and break
at the new names you have given the functions.

In IDA Pro, open up the stripped binary and select the segment you want analyzed (probably .text). Then select and run python script "make_gen.py" within IDA.
This will generate two files based on which segment you're looking at. It will prompt you to give it two files to write to.
Below I call them gen.c and script.lds. The python script will iterate through each function in the segment and determine each start address and length. 
gen.c will contain function declarations and labels for each function as well as fill each function with nops the same length as the actual functions. 
All this is for is so that the compiler knows how long each function is, so it can generate symbols. Note that since we are creating gen.c from 
the function names in IDA, we can rename the functions and they will reflect as so in gen.c. If you look at the example main.c, you will notice
that it will segfault in func(). In IDA, rename this function into something else. script.lds is just a linker file to tell gdb where
the segment starts. To run the example, type the following...

gcc -g -o symb.o -c gen.c

ld -o symb symb.o -T script.lds

gdb -s symb -e main

If you run gdb and when it crashes, you do a backtrace, you should see the function it crashed in, and its name should be whatever you renamed
it as.

In the files given, in IDA, I renamed two functions, main and func1() and then generated gen.c and script.lds, so if you just run gdb -s symb -e main
you should see the renamed functions.
