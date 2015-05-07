from idc import *

file_dest = AskFile(1,"*.", "Where do you want the generate the c file?")
script_dest = AskFile(1, "*.", "Where do you want to generate the lds script?")
f = open(file_dest, "w+")
f2 = open(script_dest, "w+")
string = "asm(\n"
lengths = []
function_starts = []


def find_lengths(function_starts, lengths):
    ea = ScreenEA()
    for function_ea in Functions(SegStart(ea), SegEnd(ea)):
        function_starts.append(function_ea)
        lengths.append(FindFuncEnd(function_ea) - function_ea)
        
find_lengths(function_starts, lengths)
count = 0

for addr_counter in range(len(function_starts)):
    string += "\"" + GetFunctionName(function_starts[addr_counter]) + ":\"\n"
    for i in range(lengths[count]-1):
        if(i == 0):
            string += "\""
        string += "nop;"
    string += "nop;\"\n"
    
    if(addr_counter < len(function_starts)-1 and function_starts[addr_counter+1] - FindFuncEnd(function_starts[addr_counter]) > 1):
        string += "\"unk"+str(count)+":\"\n"
        count += 1
        for i in range(function_starts[addr_counter+1] - FindFuncEnd(function_starts[addr_counter])):
            if(i == 0):
                string += "\""
            string += "nop;"
        string += "nop;\"\n"
    

string += ");\n"
for addr_counter in range(len(function_starts)):
    string += "int " + GetFunctionName(function_starts[addr_counter]) + "();\n"

f.write(string)
f.close()

string = ""
string += "SECTIONS\n" + "{\n" + "  . = 0x%x" % function_starts[0]
string += ";\n"
string += "  .text : { *(.text) }\n" + "}"

f2.write(string)
f2.close()
