# ------------------------------------------------------------------------------
# Author: Charsarg
# Date Created: 2024-08-08
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


from pysembler_core import *
import pysembler_debug
import pysembler_formatter
assembly_code = """
		ENTRY
start	MOV r0, #10
		MOV r1, #4
		BL doadd
		MOV r2, #10
		MOV r3, #4
		BL dosub
		LDRB r5, #0, #5
doadd	ADD r0, r1
		BX lr
dosub	SUB r2, r3
		BX lr
		END
"""

with open("assembly.code") as code_file:
    assembly_code = code_file.read()

#Format the assembly code
assembly_code = pysembler_formatter.format_assembly_code(assembly_code)
"""
assembly_code = "\t".join(assembly_code.split("    "))
functions,entryFunction = ExtractFunctions(assembly_code)
"""
#print(functions)
#print(entryFunction)
ram = Ram()

ramAlterer = pysembler_debug.RamManiplulator(ram)

ramAlterer.randomise_ram_memory(upper_bounds=9)
#ramAlterer.set_ram_memory_value(0x0, 0x3)

#print(get_command("MOV r0, #10"))
#print(get_parameters("MOV r0, #10"))

#print(substitute_parameters(get_parameters("MOV r0, #10"),ram))

Running = True
LocationLayers = []
CurrentLocation = [functions[entryFunction][0],0]
#LocationLayers.append()
start_line_to_function_name = CreateStartLineToFunctionNameLibrary(functions)
print(start_line_to_function_name)
R14 = CurrentLocation
while Running == True:
    currentFunction = start_line_to_function_name[CurrentLocation[0]]
    ram.set_value("r15",functions[currentFunction][0]+CurrentLocation[1])
    ram.print_ram()
    try:
        print(CurrentLocation)
        print(functions[currentFunction][1][CurrentLocation[1]])
        currentLine = functions[currentFunction][1][CurrentLocation[1]]
    except IndexError as e:
        raise e
        print(e)
        Running = False
        continue
    print(currentLine)
    currentCommand,_ = get_command(currentLine)
    currentParameters = get_parameters(currentLine)
    if currentCommand in ['MOVR','MOV','BL',"ADD","SUB","LDRB"]:
        currentParameters = substitute_parameters(currentParameters,ram,keep_first_value=True)
    else:
        print(currentFunction)
        currentParameters = substitute_parameters(currentParameters,ram)
    
    #print(currentCommand)
    print(currentParameters)
    #Run command logic
    IncrementLineNumberNormally = True
    if currentCommand == "MOV":
        if len(currentParameters) == 2:
            ram.set_value(currentParameters[0], currentParameters[1])
        else:
            print("Invalid number of parameters")
    if currentCommand == 'BL':
        ram.set_value("r14",ram.get_value('r15'))
        R14 = CurrentLocation
        IncrementLineNumberNormally = False
        if len(currentParameters) == 1:
            LocationLayers.append(CurrentLocation)
            CurrentLocation = [functions[currentParameters[0]][0],0]
    if currentCommand == 'BX':
        if len(currentParameters) == 1:
            if currentParameters[0] == "lr":
                #LocationLayers.pop()
                print(LocationLayers)
                CurrentLocation = LocationLayers[-1]
                CurrentLocation = R14
                LocationLayers.pop(-1)
            else:
                #LocationLayers.pop()
                print(LocationLayers)
                CurrentLocation = LocationLayers[-1]
                LocationLayers.pop(-1)
        else:
            print("Invalid number of parameters")
    if currentCommand == 'ADD':
        if len(currentParameters) == 2:
            if 'r' in str(currentParameters[0]):
                value1 = ram.get_value(currentParameters[0])
            else:
                value1 = currentParameters[0]
            if 'r' in str(currentParameters[1]):
                value2 = ram.get_value(currentParameters[1])
            else:
                value2 = currentParameters[1]
            ram.set_value(currentParameters[0], value1 + value2)
        else:
            print("Invalid number of parameters")
    if currentCommand == 'SUB':
        if len(currentParameters) == 2:
            if 'r' in str(currentParameters[0]):
                value1 = ram.get_value(currentParameters[0])
            else:
                value1 = currentParameters[0]
            if 'r' in str(currentParameters[1]):
                value2 = ram.get_value(currentParameters[1])
            else:
                value2 = currentParameters[1]
            ram.set_value(currentParameters[0], value1 - value2)
        else:
            print("Invalid number of parameters")
    if currentCommand == 'LDRB':
        if len(currentParameters) == 3:
            destination = currentParameters[0]
            base = currentParameters[1]
            offset = currentParameters[2]
            data = ram.get_value_from_memory(base,offset)
            ram.set_value(destination,data)
        else:
            print("Invalid number of parameters")
            
    if IncrementLineNumberNormally:
        CurrentLocation[1] += 1
    print(LocationLayers,CurrentLocation)
    
    
    
    