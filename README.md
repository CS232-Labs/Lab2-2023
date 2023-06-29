# Lab 2 - VHDL

## Setup
### Windows: 
- Use any IDE for VHDL programming
- Install ModelSim Altera from this [link](https://www.intel.com/content/www/us/en/software-kit/750637/modelsim-intel-fpgas-standard-edition-software-version-20-1.html). Do not forget to switch to the windows section.
- Follow the installation setup for ModelSim
Watch posted tutorials for coding in VHDL and using ModelSim

### Linux:
- We will be using GHDL and GTKWave
- Install them using the command : ``` sudo apt-get install ghdl gtkwave```
- [Here](https://www.youtube.com/watch?v=j9hya97kRJA) is a simple tutorial for GHDL

### Mac:
- We will use GHDL and GTKWave
- Install them using the commands : </br>
``` brew install --cask ghdl ``` and 
```brew install --cask gtkwave ```

Here is a [link](https://youtube.com/playlist?list=PLw6vmiIQrilSa4Xznu9Zh1ag3klXBscSZ) to tutorials in VHDL. 

-----

## Question 1 (20 marks)
a) Design basic 2-input logic gates in VHDL. Define their entity and architecture. The gates which you have to code are: AND, OR & NOT. Generate a wave-form for the inputs and outputs using a simulation tool (modelsim or GTKWave). Take a screenshot of the wave-form.

b) Design a 4 x 2 multiplexer and a 4 x 2 encoder using the basic gates that you have designed above. Do not use the built-in keywords ‘and’, ‘or’, ‘not’ etc. You must use your designed basic gates in part a) as components. Generate a wave-form for the inputs and outputs using a simulation tool (modelsim or GTKWave). Take a screenshot of the waveform.

Use the following entity definitions:
```
entity AND_Gate is
    port(x1: in std_logic;
    x2: in std_logic;
    y: out std_logic);
end entity;
```
```
entity OR_Gate is
    port(x1: in std_logic;
    x2: in std_logic;
    y: out std_logic);
end entity;
```
```
entity NOT_Gate is
    port(x: in std_logic;
    y: out std_logic);
end entity;
```
```
entity mux4x2 is
    port(D: in std_logic_vector (3 downto 0);
    S: in std_logic_vector(1 downto 0);
    Y: out std_logic);
end entity; 
```
```
entity encoder4x2 is
    port(I: in std_logic_vector (3 downto 0);
    Y: out std_logic_vector(1 downto 0));
end entity;
```

Please make sure you use this exact naming convention for entities as well as ports.

## Question 2 (30 marks)
In this question you'll be designing a 4x16 decoder using 2x4 decoders. Once again this must be designed without sequential coding of any sorts. The goal is to modularize your code as much as possible. Use the following entity definition. 
```
entity decoder4x16 is
    port(a, b, c, d, enable: in std_logic;
    dec: out std_logic_vector(15 downto 0));
end entity;
```
Write a testbench for the same showcasing all 16 decodes.

## Question 3 (50 marks)
In this question you will be designing a musical chord encoder. It converts individual notes of either a three note or a four note chord into its chord name. The circuit receives a fresh byte every posisitve transition of an external clock cycle. Every note is either one or two bytes represented by its name in ascii (for example G is 01000111 as ASCII for G is 71) followed by either a sharp (ascii 31 for #) or a flat (we'll use the ascii for the small letter, for example A flat is "a" which is 01100001).

For reference, this is the order of notes

C, C# = d, D, D# = e, E = f, F, F# = g, G, G# = a, A, A# = b, B = c, B# = C
and follow cyclically.</br> In essence, the sharp of a note is the flat of the next one with the exception of E and B and similarly a flat is the sharp of a predecessor with the exception of f and c. So we will be using these interchangably. 

- We'll encode 4 types chords: majors, minors and suspended triads as well as 7th chords
- The rules of the chords are as follows
    - Major triads (M) are formed by a key, followed by the 4th note after it, followed by the third one after that. For example, C M is formed by C, E and G. F# M is formed by F#, A# and C#.
    - Minor triads (m) are formed by a key, followed by the third note after it, followed by the fourth note after that. For example C m is formed by C, e, G. b m is formed by b, C# and F.
    - Suspended triads (s) are formed by a key, followed by the 5th note after it, followed by the 2nd note after that. For example, C s is formed by C, F and G. g s is formed by g, B and C#.
    - 7ths, also called dominant 7ths (7) are formed by a major triad plus the third note after the last note of the major. For example, C 7 is formed by C, F, G and A#. e 7  is formed by e, G, b and d.
- The circuit will read an input file and output to an output file. The reading and writing has been done in the testbench given. You can modify it as per your needs. 
- The input file will have the following constraints:
    - Each line will be an 8 bit binary number representing a note or a part of it as mentioned above. 
    - The file will not have more than 32 bytes (i.e, 32 characters)
- The output must be as follows:
    - The testbench will read the output from your circuit and print it to an output file. It will print only one character (8 bits) per line. 
    - Notice that since the output of your circuit is only 1 byte wide, it cannot output 2 or 3 bytes at once. Only 1 byte is output per clock cycle and whenever a byte is being output, the Data Valid output line must go from low to high.
    - The rules for printing a chord are as follows:
        - Major chords are to be printed with the note name followed by a capital M on the next line. For example C# major is to be printed as
          ```
          01000011
          00011111
          01001101
          ```
          or
          ```
          01100100
          01001101
          ```
          Because C# is d. Note that 01001101 is M which stands for major.
        - Similarly for minor chords print a small m after the note
        - For suspended chords print a small s after the note
        - For dominant 7ths print the ASCII value of 7 after the note (which is 55)


**Need for a buffer** : Fresh data is inputted at every rising edge of the clock. You will need to wait to see what the chord is for atleast 2 clock cycles before coming to a conclusion on the chord name. Since the output data rate may be less than or equal to or greater than the input data rate over short periods, provision must be made for buffering the input data and providing a data valid output line which becomes 1 in a clock cycle in which valid data is being output. Decide on a safe buffer size based on the constraints of the input file size mentioned above (Another approach is that you can choose whatever buffer size you want but then there should be a mechanism in your circuit for handling the situation when the buffer gets full).

**Note**</br>
- There may be notes which do not form chords. In such cases just print those notes as they are in the input
- Although obvious, preference is to be given from the left. For example, if the input is C, E, G, B, D, there could be 2 chord combinations:
    - (C, E, G) forming C M, followed by (B and D) forming no triad chord.
    - (C and E) forming no triad, followed by (G, B, D) forming G M.</br>
    In such cases, the first one is correct because the leftmost chord should be completed first.
- Preference is to be given to dominant 7th chords. For example, if the input is C, E, G, A#, D, F; 2 possible chord combinations could be :</br>
    - (C, E, G) forming C M followed by (A#, D, F) forming A# M and
    - (C, E, G, A#) forming C 7 followed by (D and F) forming no triad chord.</br>
In such cases, the second one is correct because you are to complete a dominant 7th if it exists.


Use the following entity definition:
```
entity CHORD_Encoder is
    	port(clk, rst: in std_logic;
    	a: in std_logic_vector(7 downto 0);
    	data_valid: out std_logic;
    	z: out std_logic_vector(7 downto 0));
end entity;
```
REPORT?

Place the input and output files in the same directory as the vhdl files. Read input from the file: test.txt and write output to the file: out.txt (that is, do not change the input and output file names and positions)

If you are using ghdl, you will need to add the -fsynopsys option while compiling. We will verify your output using the command ```diff -Bw true_output.txt out.txt```

Further, for Q3, note that the input may get processed completely whilst your output has not been completed yet. In that case you need to pump extra clock ticks to get the complete output. We will run the simulation for 1000 ns.


## Important Notes
- You are not to use sequential coding anywhere other than the testbenches in Q1 and Q2
- You should use sequential coding in Q3
- Q1 will have binary grading. Q2 will be graded based on how modularized your code is. Q3 will be graded on the code and the report.

## Submission
```
roll_number
├── Q1
    ├── and.vhd  and_tb.vhd  or.vhd  or_tb.vhd not.vhd  not_tb.vhd  and_wave.jpg  or_wave.jpg not_wave.jpg  mux4x2.vhd  enc4x2.vhd  mux4x2_tb.vhd enc4x2_tb.vhd mux4x2_wave.jpg enc4x2_wave.jpg
├── Q2
    ├── decoder4x16.vhd  tb.vhd  wave.jpg  *.vhd
├── Q3
    ├── CHORD.vhd  tb.vhd  wave.jpg report.pdf  *.vhd

```
Compress this directory using</br>
` zip -r roll_number.zip roll_number` and submit roll_number.zip. </br>
__Incorrect submission formats will result in NO marks.__



