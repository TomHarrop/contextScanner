#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re


# function to find key
def find_key(lines, key):
    matched_lines = []
    for i in range(0, len(lines) - 1):
        if re.search(key, lines[i]):
            matched_lines.append(i)
    return(matched_lines)


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


# find next head
def find_next_head(lines, smaller_line):
    n = smaller_line
    while (not re.search("\\\.*section\\[", lines[n]) and not
            re.search('\\\stoptext', lines[n])):
        n += 1
    stop_section = n
    return(stop_section)


# find end of references section
def find_ref_end(lines, refcut_line):
    n = refcut_line
    while (not re.search("^{$", lines[n]) and not
            re.search('\\\stoptext', lines[n])):
        n += 1
    ref_end = n
    return(ref_end)

# read tex file
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
# print(''.join(lines))

# find negindent tags
negindent_lines = find_key(lines, "<-negindent->")

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
smaller_lines = find_key(lines, "<-smaller->")
smaller_stops = []
for smaller in smaller_lines:
    smaller_stops.append(find_next_head(lines, smaller))

# change body font for smaller sections
for smaller in smaller_lines:
    lines[smaller] = '{\switchtobodyfont[small]\n\n'
for smaller in smaller_stops:
    lines[smaller] = '}\n\n' + lines[smaller]

# find refcuts (should only be one)
refcut_lines = find_key(lines, "<-refcut->")
if len(refcut_lines) > 0:
    refcut_line = refcut_lines[0]
    ref_end = find_ref_end(lines, refcut_line)

    # find refpaste (should only be one)
    refpaste_line = find_key(lines, "<-refpaste->")[0]

    # extract the references section 
    ref_sec = lines[refcut_line:ref_end]

    # remove tag
    ref_sec[0] = ''

    # convert refseq to itemised list
    for i in range(0, len(ref_sec) - 1):
        if re.search('\\\\reference', ref_sec[i]):
            ref_sec[i + 1] = re.sub(r'^(\d+)\.', r'\sym{\1.\hskip1em}', ref_sec[i + 1])
            ref_sec[i] = ''

    # add itemize keys
    ref_sec.insert(0, "{\setupitemize[each][packed][itemalign=flushright]\startitemize[n, packed]\n\n")
    ref_sec.append('\stopitemize}\n\n')

    # blank out the refcut area
    for i in range(refcut_line, ref_end):
        lines[i] = ''

    #insert ref_sec at ref_paste
    lines[refpaste_line] = ''.join(ref_sec)

# print(lines[refpaste_line])

# print(''.join(lines[refpaste_line]))

# print(''.join(ref_sec))

print(''.join(lines))
