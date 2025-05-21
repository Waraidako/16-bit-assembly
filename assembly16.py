#!/bin/python3
import sys
import os


# Get the original file's location
if (len(sys.argv) == 2):
    target_file = sys.argv[1]
    if (target_file[0] != '/'):
        target_file = os.getcwd() + '/' + target_file
    print('Original file: ' + target_file, flush=True)
else:
    print('Error: invalid number of arguments', flush=True)
    sys.exit()

# Open the original file
original_contents = []
with open(target_file, 'r') as f:
    # Read all the contents
    for line in f:
        original_contents.append(line)

# Process all the contents
assembled_contents = []
for line in original_contents:
    binary = process_line(line)
    assembled_contents.append(binary)

# Write into assembled file next to original
filepath_no_extension = '.'.join(target_file.split('.')[:-1])
with open(filepath_no_extension + '.hex', 'w') as f:
    for line in assembled_contents:
        f.write(line)
with open(filepath_no_extension + '.bin', 'w') as f:
    for line in assembled_contents:
        f.write(line)

# Profit 👍



def process_line(line):
    basic_commands = [
        'add',
        'or',
        'xor',
        'nand',
        'xnor',
        'add',
        'sub',
        'cmp',
        'jmp',
        'je',
        'jz',
        'jg',
        'jnle',
        'jge',
        'jnl',
        'jl',
        'jnge',
        'jle',
        'jng',
        'jc',
        'call',
        'push',
        'pop',
    ]
    other_commands = [
        'mov',
        'and',
        'return',
        'shr',
        'shr a',
        'shl',
        'shl a',
        'inc a',
        'inc c',
        'dec a',
        'dec c'
    ]
    res = ''

    return res