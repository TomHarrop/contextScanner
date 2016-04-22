#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

# function to find negindent line
def find_negindent(lines):
    negindent_lines = []
    for i in range(0, len(lines)):
        if re.search("<-negindent->", lines[i]):
            negindent_lines.append(i)
    return(negindent_lines)

# function to find previous head
# walk backwards until find a *section
# then walk forwards until find a blankline
def find_previous_head(lines, negindent_line):
    print(lines[negindent_line])

# function to find smaller lines

# set matching variables. these will be toggled to on when a match is found
negindent = False
smaller = False

# read tex file
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

# find negindent calls
negindent_lines = find_negindent(lines)

# find header for negindent
for negindent_line in negindent_lines:
    print(negindent_line)
    find_previous_head(lines, negindent_line)
    find_previous_head(lines, negindent_line - 1)
    find_previous_head(lines, negindent_line - 2)


# for i in range(0, len(lines) - 2):
    # if not smaller and re.search("<-smaller->", lines[i]):
    #     smaller = True
    #     print("{\switchtobodyfont[small]")
    # if not negindent and re.search("<-negindent->", lines[i]):
    #     negindent = True
    #     print("\n\startnegindent\n")
    #     print(lines[i - 2].strip('\n\r'))
    # elif (negindent and not smaller and
    #         re.search("^\\\.*section\\[", lines[i])):
    #     negindent = False
    #     print("\stopnegindent\n")
    #     print(lines[i].strip('\n\r'))
    # # elif (smaller and not negindent and
    #         re.search("^\\\.*section\\[", lines[i])):
    #     smaller = False
    #     print("}\n")
    #     print(lines[i].strip('\n\r'))
    # elif (smaller and negindent and
    #         re.search("^\\\.*section\\[", lines[i])):
    #     negindent = False
    #     smaller = False
    #     print("\stopnegindent\n\n}\n")
    #     print(lines[i].strip('\n\r'))
#     if not re.search("<-negindent->", lines[i + 2]):
#         print(lines[i].strip('\n\r'))

# print(lines[len(lines) - 2].strip('\n\r'))
# print(lines[len(lines) - 1].strip('\n\r'))
