#!/usr/bin/env python3
import argparse
import binascii
import os
import pathlib
import shutil
import sys
from argparse import RawTextHelpFormatter
from itertools import permutations

DEFAULT_GLOBAL_BUSSIZES = [1, 2, 4]


def masher(filedata, bit, allperms, flipped, output):
    if allperms:
        permlist = []
        for i in range(len(filedata)):
            permlist.append(i)
        if flipped != "FLIP" or bit != 1:
            for permutation in permutations(permlist):
                permutation_str = "_".join(str(num) for num in permutation)
                bitsize = (bit * 8) * (len(filedata) // 2)
                filename = f"{output}/permutationmashed_{permutation_str}_bit{bitsize*2}{flipped}.bin"
                mode = "ab"
                with open(filename, mode) as permout:
                    for i in range(0, len(filedata[0]), bit):
                        for item in permutation:
                            data = filedata[item][i : i + bit]
                            if flipped == "FLIP":
                                data = data[::-1]
                            permout.write(data)
    else:
        bitsize = (bit * 8) * (len(filedata) // 2)
        filename = f"{output}/mashed{flipped}{bitsize*2}.bin"
        mode = "ab"
        with open(filename, mode) as dataoutput:
            for i in range(0, len(filedata[0]), bit):
                for j in range(len(filedata)):
                    data = filedata[j][i : i + bit]
                    if flipped == "FLIP":
                        data = data[::-1]
                    dataoutput.write(data)


def callmashers(filedata, bussize, reverse, allperms, flipped, output, clobber):
    if not clobber:
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)
    else:
        clobberctr = 1
        while os.path.exists(output):
            output = f"{output}{clobberctr}"
            clobberctr += 1
        os.makedirs(output)
    if reverse == True:
        filedata = [element[::-1] for element in filedata]
    for string in flipped:
        if bussize == 0:
            for i in DEFAULT_GLOBAL_BUSSIZES:
                masher(filedata, i, allperms, string, output)
        elif bussize != 0:
            masher(filedata, bussize, allperms, string, output)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        prog="python3 flashmash.py",
        description="""Toolkit to smash flash dumps together to find valid data. Default is all 3 bus sizes byte order flipped and non flipped.
        Needs 2 or 4 vaid dumps as arguments.""",
        epilog="""Examples:

        python3 flashmash.py bindump1.bin bindump2.bin -r -p
            reverse and all permutations
        ./flashmash.py bindump1.bin bindump2.bin bindump3.bin bindump4.bin -f Y
            flipped only byteorder on 4 dumps""",
    )
    parser.add_argument(
        "input_files",
        nargs="+",
        type=argparse.FileType("rb"),
        default=sys.stdin,
        help="input files for parsing. Either 2 or 4 dumps.",
    )
    parser.add_argument(
        "-b",
        "--bussize",
        default="0",
        type=int,
        help="Specify the bus size of ONE flash chip IE 8,16,32",
    )
    parser.add_argument(
        "-f",
        "--flipped",
        nargs="+",
        default=["FLIP", "NOFLIP"],
        help="Flip byte order. DEFAULT = FLIP && NOFLIP.",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Scan input files from end of file. Go in reverse. Useful for backward dumps or flipped busses.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        nargs=1,
        default="MashedFlash",
        help="To change directory to output data to. Default = MashedFlash/",
    )
    parser.add_argument(
        "-p",
        "--allpermutations",
        action="store_true",
        help="Produces all permutations of file combinations. \n***WARNING*** 4 input files will produce 48 files!",
    )
    parser.add_argument(
        "-cp",
        "--noclobber",
        action="store_true",
        help="Will write to incremental directory rather than overwriting current directory",
    )
    args = parser.parse_args()
    num_files = len(args.input_files)
    if (
        num_files not in [2, 4]
        or 0 != args.bussize % 8
        or -1 >= args.bussize
        or args.bussize > 32
    ):
        parser.error("Improper use of parameters. Use -h to see usage of flaShMASH.")
        exit(-1)
    filedata = []
    for file in args.input_files:
        filedata.append(file.read())
    callmashers(
        filedata,
        args.bussize // 8,
        args.reverse,
        args.allpermutations,
        args.flipped,
        args.output,
        args.noclobber,
    )


if __name__ == "__main__":
    main()
