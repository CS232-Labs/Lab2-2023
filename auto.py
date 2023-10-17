import os
import pandas as pd

map1 ={
    "01000101": "01100110",  # E
    "01000010": "01100011",  # B
}

map = {
    "01000011": "01100100",  # C#
    "01000100": "01100101",  # D#  
    "01000101": "01000110",  # E#
    "01000110": "01100111",  # F#
    "01000111": "01100001",  # G#
    "01000001": "01100010",  # A#
    "01000010": "01000011",  # B#
}

def convert_to_bin(list):
    out = []
    for i in list:
        if i == "#":
            out.append("00011111")
        else:
            x = bin(ord(i)).replace("b", "")
            if len(x) == 7:
                x="0"+x
            out.append(x)
    return out

def write_to_test(list):
    file = open("test.txt", 'w')
    write_buf = []
    for i in list:
        write_buf.append(f"{i}\n")
    file.writelines(write_buf)
    file.close()

    

def convert_to_flat():
    out_txt = open("out.txt", "r")
    lines = out_txt.readlines()
    lines = [i[0:8] if i!="\n" else "" for i in lines] #strip newline
    lines.append("X")
    lines_new = []
    temp = ""
    temp1= ""
    for i in lines:
        if i == "":
            continue
        elif i == "00011111":
            lines_new.append(map[temp])
            temp1 = ""
        elif i == "01000101" or i == "01000010":
            if temp1 != "":
                lines_new.append(temp1)
                temp1 = ""
            elif temp != "":
                lines_new.append(temp)
            temp1 = map1[i]
            temp = i
        else:
            if temp1 != "":
                lines_new.append(temp1)
                temp1 = ""
            elif temp != "":
                lines_new.append(temp)
                temp1 = ""
            temp = i
    return lines_new

tests = [["C", "D", "E", "F", "G", "A", "B", "C"], 
         ["C", "E", "G", "A", "#", "D", "F", "A"],
         ["C", "E", "G", "B", "D", "#", "g", "A", "C", "E", "G", "B", "D", "#", "g", "A", 
          "C", "E", "G", "B", "D", "#", "g", "A", "C", "E", "G", "B", "D", "#", "g", "A"],
         ["c", "C", "F", "G"],
         ["C"]]

true_outputs = [["C", "D", "f", "F", "G", "A", "c", "C"], 
                ["C", "7", "D", "m"],
                ["C", "M", "c", "7", "C", "M", "c", "7", "C", "M", "c", "7", "C", "M", "c", "7"],
                ["c", "C", "s"],
                ["C"]]
###########################################################################################################

marks = 0

open("out.txt", 'w+')
os.system("ghdl -a --ieee=synopsys q3_CHORD.vhd q3_tb.vhd")
os.system("ghdl -e --ieee=synopsys ASCII_Read_test")
for i in range(len(tests)):
    write_to_test(convert_to_bin(tests[i]))
    os.system("ghdl -r --ieee=synopsys ASCII_Read_test --stop-time=1000ns --wave=hello.ghw")
    code_out = convert_to_flat()
    if code_out == convert_to_bin(true_outputs[i]):
        marks+=10
        print(f"Test case {i} passed.")
print(f"Marks : {marks}/50")
