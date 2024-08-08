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

import random

class RamManiplulator:
  def __init__(self, ram):
    self.ram=ram
  def set_ram_memory_value(self, register, value):
    self.ram.memory[register]=value
  def set_ram_register_value(self, register, value):
    self.ram.register[register]=value
  def get_ram_memory_value(self, register):
    return self.ram.memory[register]
  def get_ram_register_value(self, register):
    return self.ram.register[register]
  def clear_ram_register(self):
    for register in self.ram.register:
      self.ram.register[register]=0x0
  def clear_ram_memory(self):
    for register in self.ram.memory:
      self.ram.memory[register]=0x0
  def clear_ram(self):
    self.clear_ram_register()
    self.clear_ram_memory()
  def randomise_ram_register(self, lower_bounds=0x0, upper_bounds=0xf):
    for register in self.ram.register:
      self.ram.register[register] = random.randint(lower_bounds, upper_bounds)
  def randomise_ram_memory(self, lower_bounds=0x0, upper_bounds=0xf):
    for register in self.ram.memory:
      self.ram.memory[register] = random.randint(lower_bounds, upper_bounds)
  def randomise_ram(self, lower_bounds=0x0, upper_bounds=0xf):
    self.randomise_ram_register(lower_bounds, upper_bounds)
    self.randomise_ram_memory(lower_bounds, upper_bounds)

