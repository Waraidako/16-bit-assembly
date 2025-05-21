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

line_counter = 1

def error():
    return f'Error on line {line_counter}'

def process_line(line):
    basic_commands = [
        'and',
        'or',
        'xor',
        'nand',
        'nor',
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
    basic_commands_codes = {
        'and': '00001',
        'or': '00010',
        'xor': '00011',
        'nand': '00100',
        'nor': '00101',
        'xnor': '00110',
        'add': '00111',
        'sub': '01000',
        'cmp': '01001',
        'jmp': '01010',
        'je': '01011',
        'jz': '01011',
        'jg': '01100',
        'jnle': '01100',
        'jge': '01101',
        'jnl': '01101',
        'jl': '01110',
        'jnge': '01110',
        'jle': '01111',
        'jng': '01111',
        'jc': '11000',
        'call': '11001',
        'push': '11010',
        'pop': '11011',
    }
    other_commands = [
        'stop',
        'mov',
        'and',
        'return',
        'shr',
        'shl',
        'inc',
        'dec',
    ]
    no_arg_commands = {
        'stop': '0000000000000000',
        'return': '0000000100000000'
    }
    line = line.lower()
    no_comments = line.split(';')
    if (not no_comments or (not no_comments[0] or no_comments[0].isspace())):
        return ''
    res = ''
    full_command = no_comments[0]
    command_id = full_command.split()[0]
    
    # Check if command is valid
    if (not(command_id in basic_commands or command_id in other_commands)):
        return error()
    
    # Check that if no args the command is allowed to have no args
    if (len(full.command.split()) == 1):
        if (command_id in no_arg_commands.keys):
            return no_arg_commands[command_id]
        else:
            return error()
    
    # Get arguments
    args = ''.join(full_command.split()[1:])

    # Parse MOV
    if (command_id == 'mov'):
        return 'its a mov'

    # Parse basic commands
    if (command_id in basic_commands):
        return 'its a basic command'

    # Parse other
    if (command_id in other_commands):
        return 'its an "other" command'

    line_counter += 1
    return res

print('Assembling...')
assembled_contents = []
for line in original_contents:
    binary = process_line(line)
    if ('Error' in binary):
        print(binary, flush=True, end='')
        sys.exit()
    assembled_contents.append(binary)

# Write into assembled file next to original
print('Writing into assembled files... ', flush=True, end='')
filepath_no_extension = '.'.join(target_file.split('.')[:-1])
with open(filepath_no_extension + '.hex', 'w') as f:
    for line in assembled_contents:
        f.write(line)
    print('.hex ... ', flush=True, end='')
with open(filepath_no_extension + '.bin', 'w') as f:
    for line in assembled_contents:
        f.write(line)
    print('.bin ...', flush=True, end='')

# Profit 👍