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


# find previous head and next head
def find_indent_section(lines, negindent_line):
    n = negindent_line
    while not re.search("\\\.*section\\[", lines[n]):
        n -= 1
    start_head = n
    n = negindent_line
    while not re.search("\\\.*section\\[", lines[n]):
        n += 1
    stop_section = n
    return(start_head, stop_section)


# function to find smaller lines
def find_smaller(lines):
    smaller_lines = []
    for i in range(0, len(lines)):
        if re.search("<-smaller->", lines[i]):
            smaller_lines.append(i)
    return(smaller_lines)


# find next head
def find_next_head(lines, smaller_line):
    n = smaller_line
    while (not re.search("\\\.*section\\[", lines[n]) and not
            re.search('\\\stoptext', lines[n])):
        n += 1
    stop_section = n
    return(stop_section)

# read tex file
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

# find negindent tags
negindent_lines = find_negindent(lines)

# find bits to negindent
start_heads = []
stop_sections = []
for negindent in negindent_lines:
    start_head, stop_section = find_indent_section(lines, negindent)
    start_heads.append(start_head)
    stop_sections.append(stop_section)

# set the negindents: starts first, then stops
for head in start_heads:
    lines[head] = '{\startnegindent\n\n' + lines[head]
for head in stop_sections:
    lines[head] = '\stopnegindent\n\n}\n\n' + lines[head]

# remove negindent tags
for negindent in negindent_lines:
    lines[negindent] = ''

# find smaller sections
smaller_lines = find_smaller(lines)
smaller_stops = []
for smaller in smaller_lines:
    smaller_stops.append(find_next_head(lines, smaller))

# change body font for smaller sections
for smaller in smaller_lines:
    lines[smaller] = '{\switchtobodyfont[small]\n\n'
for smaller in smaller_stops:
    lines[smaller] = '}\n\n' + lines[smaller]

print(''.join(lines))
