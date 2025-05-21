#!/bin/python3
import sys
import os

# Get the original file's location
#if (len(sys.argv) == 2):
#    target_file = sys.argv[1]
#    if (target_file[0] != '/'):
#        target_file = os.getcwd() + '/' + target_file
#    print('Original file: ' + target_file, flush=True)
#else:
#    print('Error: invalid number of arguments', flush=True)
#    sys.exit()

target_file = 'hello.asm'

# Open the original file
original_contents = []
with open(target_file, 'r') as f:
    # Read all the contents
    for line in f:
        original_contents.append(line)

# Process all the contents


# After preprocessing - mov a, [a + 432] -> mov a,[a+432] (I hope at least lmao)
# Also                  shr a -> shr
def preprocess():
    for i in range(len(original_contents)):
        if (not original_contents[i] or original_contents[i].isspace()):
            continue
        original_contents[i] = original_contents[i].lower()
        if ('shr a' in original_contents[i]):
            original_contents[i] = 'shr'
            continue
        split_line = original_contents[i].split()
        if (len(split_line) > 1):
            original_contents[i] = ' '.join([split_line[0], ''.join(split_line[1:])])
        else:
            original_contents[i] = split_line[0]


basic_commands = {
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
other_commands = {
        'mov': '100010',
        'inc': '0000010',
        'dec': '0000011',
}
no_arg_commands = {
    'stop': '0000000000000000',
    'return': '0000000100000000',
    'shr': '0000001000000000',
    'shl': '0000001100000000'
}
    
line_counter = 1

def error():
    return f'Error on line {line_counter}\n'

def is_register(name):
    reg_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'sp', 'bp', 'ip', 'flags']
    return name in reg_names

def reg_code(name):
    reg_codes = {
        'a': '0000', 
        'b': '0001', 
        'c': '0010', 
        'd': '0011', 
        'e': '0100', 
        'f': '0101', 
        'g': '0110', 
        'sp': '0111', 
        'bp': '1000', 
        'ip': '1001', 
        'flags': '1010'
    }
    return reg_codes[name]

def process_line(line):
    no_comments = line.split(';')
    if (not no_comments or (not no_comments[0] or no_comments[0].isspace())):
        return ''
    res = ''
    full_command = no_comments[0]
    command_id = full_command.split()[0]
    
    # Check if command is valid
    if (not(command_id in basic_commands.keys() or command_id in other_commands.keys() or command_id in no_arg_commands.keys())):
        return error()
    
    # Check that if no arg the command is allowed to have no arg
    if (len(full_command.split()) == 1):
        if (command_id in no_arg_commands.keys()):
            return no_arg_commands[command_id]
        else:
            return error()
    
    # Get arguments
    args = full_command.split()[1]

    # Parse MOV
    if (command_id == 'mov'):
        args = args.split(',')
        if (len(args) != 2):
            return error()
        if (is_register(args[0])):
            if (is_register(args[1])):
                return f'10001001{reg_code(args[0])}{reg_code(args[1])}'                       # reg, reg
            if (args[1][0] != '['):
                try:
                    literal_address = str(bin(int(args[1])))[2:].zfill(16)
                    return f'10001000{reg_code(args[0])}0000{literal_address}'                 # reg, lit
                except:
                    return error()
            else:
                args[1] = args[1][1:-1]
                if (is_register(args[1])):
                    return f'10001011{reg_code(args[0])}{reg_code(args[1])}'
                else:
                    try:
                        literal_address = str(bin(int(args[1])))[2:].zfill(16)
                        return f'10001010{reg_code(args[0])}0000{literal_address}'             # reg, [lit]
                    except:
                        pass
                
                args[1] = args[1].split('+')
                if (len(args[1]) != 2):
                    return error()
                first_register_status = is_register(args[1][0])
                second_register_status = is_register(args[1][1])
                if (first_register_status and second_register_status):
                    return f'10001101{reg_code(args[0])}{reg_code(args[1][0])}000000000000{reg_code(args[1][1])}' # reg, [reg, reg]
                else:
                    if (first_register_status):
                        try:
                            literal_address = str(bin(int(args[1][1])))[2:].zfill(16)
                            return f'10001100{reg_code(args[0])}{reg_code(args[1][0])}{literal_address}'
                        except:
                            return error()
                    elif (second_register_status):
                        try:
                            literal_address = str(bin(int(args[1][0])))[2:].zfill(16)
                            return f'10001100{reg_code(args[0])}{reg_code(args[1][1])}{literal_address}'
                        except:
                            return error()
                    else:
                        return error()
        # [...], reg/lit case
        elif (args[0][0] == '['):
            # Second argument check
            second_arg_is_register = is_register(args[1])
            if (not second_arg_is_register):
                try:
                    literal = str(bin(int(args[1])))[2:].zfill(16)
                except:
                    return error()
            args[0] = args[0][1:-1]

            # [reg], reg/lit case
            if (is_register(args[0])):
                if (second_arg_is_register):
                    return f'10011001{reg_code(args[0])}{reg_code(args[1])}'
                else:
                    return f'10011000{reg_code(args[0])}0000{literal}'
            
            # [lit], reg/lit case
            try:
                literal_address = str(bin(int(args[0])))[2:].zfill(16)
                if (second_arg_is_register):
                    return f'100100010000{reg_code(args[1])}{literal_address}'
                else:
                    return f'1001000000000000{literal_address}{literal}'
            except:
                pass

            # [r+l], reg/lit case
            args[0] = args[0].split('+')
            if (len(args[0]) != 2):
                return error()
            first_register_status = is_register(args[0][0])
            second_register_status = is_register(args[0][1])
            if (first_register_status and second_register_status):
                if (second_arg_is_register):
                    return f'10101001{reg_code(args[0][0])}{reg_code(args[0][1])}000000000000{reg_code(args[1])}'
                else:
                    return f'10101000{reg_code(args[0][0])}{reg_code(args[0][1])}{literal}'
            else:
                if (first_register_status):
                    try:
                        literal_address = str(bin(int(args[0][1])))[2:].zfill(16)
                        reg_arg = reg_code(args[0][0])
                    except:
                        return error()
                elif (second_register_status):
                    try:
                        literal_address = str(bin(int(args[0][0])))[2:].zfill(16)
                        reg_arg = reg_code(args[0][1])
                    except:
                        return error()
                else:
                    return error()
                if (second_arg_is_register):
                    return f'10100001{reg_arg}{reg_code(args[1])}{literal_address}'
                else:
                    return f'10100000{reg_arg}0000{literal_address}{literal}'
        else:
            return error()

    # Parse basic commands
    if (command_id in basic_commands.keys()):
        # If address
        if (args[0] == '['):
            args = args[1:-1]
            # No sum case
            if (is_register(args)):
                return f'{basic_commands[command_id]}0110000{reg_code(args)}'             # [reg]
            else:
                try:
                    literal_address = str(bin(int(args)))[2:].zfill(16)
                    return f'{basic_commands[command_id]}01000000000{literal_address}'    # [lit]
                except:
                    pass
            
            # Possibly a sum
            args = args.split('+') # arg now an array
            if (len(args) != 2):
                return error()
            first_register_status = is_register(args[0])
            second_register_status = is_register(args[1])
            if (first_register_status and second_register_status):
                return f'{basic_commands[command_id]}101{reg_code(args[0])}{reg_code(args[1])}' # [r+r]
            else:
                if (first_register_status):
                    try:
                        literal_address = str(bin(int(args[1])))[2:].zfill(16)
                        return f'{basic_commands[command_id]}1000000{reg_code(args[0])}{literal_address}'
                    except:
                        return error()
                elif (second_register_status):
                    try:
                        literal_address = str(bin(int(args[0])))[2:].zfill(16)
                        return f'{basic_commands[command_id]}1000000{reg_code(args[1])}{literal_address}'
                    except:
                        return error()
                else:
                    return error()
        
        # Else - not address
        elif (is_register(args)):
            return f'{basic_commands[command_id]}0010000{reg_code(args)}' # reg
        else:
            try:
                literal_address = str(bin(int(args)))[2:].zfill(16)
                return f'{basic_commands[command_id]}00000000000{literal_address}' # lit
            except:
                return error()

    # Parse other
    if (command_id in other_commands):
        if (args == 'a'):
            variable_bit = '0'
        else:
            variable_bit = '1'
        return f'{other_commands[command_id]}{variable_bit}00000000'
    
    return error()

print('Assembling...')
assembled_contents = []
preprocess()
has_errors = False
for line in original_contents:
    binary = process_line(line)
    if ('Error' in binary):
        print(binary, flush=True, end='')
        has_errors = True
    if (binary):
        assembled_contents.append(binary)
    line_counter += 1

if (has_errors):
    sys.exit()

# Write into assembled file next to original
print('Writing into assembled files... ', flush=True, end='')
filepath_no_extension = '.'.join(target_file.split('.')[:-1])
#with open(filepath_no_extension + '.hex', 'w') as f:
#    for line in assembled_contents:
#        f.write(line)
#    print('.hex ... ', flush=True, end='')
with open(filepath_no_extension + '.bin', 'w') as f:
    for line in assembled_contents:
        f.write(line + '\n')
    print('.bin ...', flush=True, end='')
print(f'\nAssembled {target_file}')
# Profit 👍