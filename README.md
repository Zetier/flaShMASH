# FlaShMASH 
## A Flashdump combining tool - Created by Zetier

While inspecting an ECG from spacelabs (specifically the 90496) I ran into a little issue. Upon dumping the firmware, it appeared that there were no valid strings! I dumped both flash chips and inspected them thoroughly for any valid words, both UTF-8 and UTF-16. After looking at the board for hours on end, I finally broke out my multimeter in curiosity. Flipped it into continuity mode and started probing. What I found next unraveled the next week of figuring all of this out and producing flaShMASH. A deeper dive into the tool is located [here](https://zetier.com/flashmash).

## Enough about the ECG! We want the tool!

Flashmash is a tool that has the ability to permutate byte orders of flash dumps to find valid data. I have seen numerous reddit threads and stack overflow pages with questions about this issue of trying to resolve valid data from mixed and "meshed" flash chips. If you are just here for the tool, stay here. Those who want a deeper understanding go to our blog post located [here](https://zetier.com/flashmash) and return. Like 99% of you dont read the whole thing anyway. I dont either.

### FlaShMASH in action

To use flashmash, you simply need to feed it eithur 2 or 4 flash memory dumps. The defualt flags on the dumps fed are all flipping and all bitsize. It will not perform any permutations without the -p flag. Using the -h flag will display the menu for the user. Run `chmod +x flashmash.py` to make the script an executable if python3 is located at `/usr/bin/env`. This script can also just run with `python3 flashmash.py [params]`. 

>usage: python3 flashmash.py [-h] [-b BUSSIZE] [-f FLIPPED [FLIPPED ...]] [-r]
>                            [-o OUTPUT] [-p] [-cp]
>                            input_files [input_files ...]
>
>Toolkit to smash flash dumps together to find valid data. Default is all 3 bussizes byte order flipped and non flipped.
>        Needs 2 or 4 vaid dumps as arguments.
>
>positional arguments:
>  input_files           input files for parsing. Either 2 or 4 dumps.
>
>optional arguments:
>  -h, --help            show this help message and exit
>  -b BUSSIZE, --bussize BUSSIZE
>                        Specify the bus size of ONE flash chip IE 8,16,32
>  -f FLIPPED [FLIPPED ...], --flipped FLIPPED [FLIPPED ...]
>                        Flip byte order. DEFAULT = FLIP && NOFLIP.
>  -r, --reverse         Scan input files from end of file. Go in reverse. Useful for backward dumps or flipped busses.
>  -o OUTPUT, --output OUTPUT
>                        To change directory to output data to. Default = MashedFlash/
>  -p, --allpermutations
>                        Produces all permutations of file combinations.
>                        ***WARNING*** 4 input files will produce 48 files!
>  -cp, --noclobber      Will write to incremental directory rather than overwriting current directory
>

### Examples

>`./flashmash.py dump1.bin dump2.bin` will run default settings of all flips and all bitsizes supported 
>
>`./flashmash.py dump1.bin dump2.bin dump3.bin dump4.bin -p` will output all permutations
>
> `./flashmash.py dump2.bin dump1.bin -r` will read the files in reverse, then do the bit mashing
>

### Finding the data

After mashing data, a user can then run grep against all output files to start finding valid strings. Common hardware strings such as `password`,`abcdef`, or the part numbers/microcontroller can be found in the output files by running `grep -r [searchstring]`. For example after navigating to the output directory and running `grep -r password` the file. 

You can then run strings on this file and see if it is actually legit. In this case, I ran strings against my dump and it was in fact all valid data. This tool currently supports up to 4 flash chips with 32 bit data busses totalling 128 bit operations and down to 16 bit operations. In this case, the flip version was the valid data.

