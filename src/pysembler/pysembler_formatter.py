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


def ensure_tabs(assembly_code):
    assembly_code = "\t".join(assembly_code.split("    "))
    return assembly_code
