# ------------------------------------------------------------------------------
# Author: Charsarg
# Date Created: 2024-08-07
# Current Version: Alpha 1
# Current Revision: 2024-08-08
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


#from pysembler.pysembler_core import *
import pysembler.pysembler_core
import pysembler.pysembler_debug as pysembler_debug
import pysembler.pysembler_formatter as pysembler_formatter


def MOV(ram, currentParameters):
    if len(currentParameters) == 2:
        ram.set_value(currentParameters[0], currentParameters[1])
    else:
        print("Invalid number of parameters")


def BL(ram, currentParameters,CurrentLocation,functions,LocationLayers=[]):
    ram.set_value("r14",ram.get_value('r15'))
    R14 = CurrentLocation
    IncrementLineNumberNormally = False
    if len(currentParameters) == 1:
        LocationLayers.append(CurrentLocation)
        CurrentLocation = [functions[currentParameters[0]][0],0]
        return IncrementLineNumberNormally,{"R14":R14,"CurrentLocation":CurrentLocation,"Error":None}
    return IncrementLineNumberNormally,{"Error":"WrongParams"}


    