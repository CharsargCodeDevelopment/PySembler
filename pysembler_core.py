# ------------------------------------------------------------------------------
# Author: Charsarg
# Date Created: 2024-08-07
# Current Version: Alpha 1
# Current Revision: 2024-08-07
# Description: A Cortex-M3 assembly simulator, designed for learning and development 
#               purposes. Project Name: pysembler
# Copyright: (c) 2023 Charsarg. All rights reserved.
# License: This project is open source and available under the MIT license.
#           Users can view and use the code. Private modifications are allowed,
#           including the addition of new functions to the `main.py` file 
#           and modifications to other non-core files. Public release of 
#           modified code is permitted, but attribution to the original author 
#           is required. Modifications to the core files 
#           ("pysembler_*.py") are not permitted. 
# ------------------------------------------------------------------------------

def ExtractFunctions(assembly_code):
    functions = {}
    current_function = []
    current_function_name = ""
    isEntryBlock = False
    entryFunction = ""
    firstLineOfFunction = 0
    CurrentLine = 0
    for line in assembly_code.split('\n'):
        #print(ord(list(line)[0]))
        if len(list(line)) == 0:
            continue
        print(ord(list(line)[0]))
        print(ord('\t'))
        if list(line)[0] == '\t':
            print('CODE')
            if "ENTRY" in line:
                isEntryBlock = True
            current_function.append("".join(line.split("\t")))
        else:
            print('FunctionName')
            functions[current_function_name] = [
                firstLineOfFunction, (current_function)
            ]
            current_function = []
            firstLineOfFunction = CurrentLine
            line_list = line.split("\t")
            current_function_name = line_list.pop(0)
            if isEntryBlock:
                entryFunction = current_function_name
                isEntryBlock = False
            current_function.append("\t".join(line_list))
        CurrentLine += 1
    functions[current_function_name] = [
        firstLineOfFunction, (current_function)
    ]

    print(functions)
    print(entryFunction)
    return functions, entryFunction


commands = ["MOV", "BL", "ADD", "BX", "END","SUB","MUL","DIV","AND","OR","XOR","SHL","SHR","CMP","CMPR","LDRB"]


def get_command(line):

    line = line.strip()
    for command in commands:
        if command in line:
            return command, line.split(command)[1].strip()
    return None, None


def get_parameters(line):
    line = line.strip()
    for command in commands:
        if command in line:
            params = line.split(command)[1].strip()
            params = "".join(params.split(' '))
            params = params.split(",")
            return params

    return None, None


def substitute_parameters(parameters, ram, keep_first_value=False):
    print(parameters)
    startI = 0
    if keep_first_value:
        startI = 1
        parameters[0]
    for i in range(startI, len(parameters)):
        print(parameters[i])
        if parameters[i].startswith("#"):
            parameters[i] = int(parameters[i][1:])
        elif parameters[i].startswith("r"):
            parameters[i] = ram.get_value(parameters[i])
        elif parameters[i].startswith("@"):
            parameters[i] = int(parameters[i][1:])
        else:
            parameters[i] = ram.get_value(parameters[i])
            #parameters[i] = int(parameters[i])
    """
    if keep_first_value:
        return parameters[0], parameters[1:]
    """
    return parameters


def CreateStartLineToFunctionNameLibrary(functions):
    start_line_to_function_name = {}
    for function in functions:
        start_line_to_function_name[functions[function][0]] = function
    return start_line_to_function_name


class Ram:

    def __init__(self):
        self.memory = {}
        self.register = {}
        for i in range(0, 16):
            self.register["r" + str(i)] = 0x0
        self.translation_index = {"lr":"r14", "pc":"r15"}
        for i in range(0, 0xf):
            self.memory[i]=(0x0)
        
    def get_value(self, register):
        if register in self.translation_index:
            register = self.translation_index[register]
        if register in self.register:
            return self.register[register]
        else:
            return self.memory[int(register, 16)]

    def get_value_from_memory(self, base, offset):
        out = []
        for i in range(base,base+offset+1):
            out.append(self.memory[i])
        for i in range(len(out)):
            out[i] = str(out[i])
        int("".join(out))
        return int("".join(out))

    def set_value(self, register, value):
        if register in self.translation_index:
            register = self.translation_index[register]
        if register in self.register:
            self.register[register] = value
        else:
            self.memory[register] = value

    def print_ram(self):
        for register in self.register:
            print(f"{register}: {self.register[register]}")
        for register in self.memory:
            print(f"{register}: {self.memory[register]}")
