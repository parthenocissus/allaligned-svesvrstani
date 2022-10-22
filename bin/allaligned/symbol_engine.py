"""
All-Aligned
Svesvrstani

https://krcadinac.com/all-aligned

The All-Aligned is a digital art project by Uroš Krčadinac.
An open source AI system for automated vexillology,
it visualises the fractal-like fragmentary nature
of our digital condition and raises questions about
the society where identity creation is mediated by Big Tech.

Copyright (C) 2022.  Uroš Krčadinac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import math
from random import choices, random, randint, uniform, randrange
from svgpathtools import svg2paths, svg2paths2, wsvg
from xml.etree import ElementTree as ET

from bin.allaligned.flag_symbol import FlagSymbol
from bin.allaligned.flag_symbol_config import FlagSymbolConfig


class SymbolEngine:

    def __init__(self, origin, flag, recursive_level):

        self.origin = origin
        self.flag = flag

        scale_baseline = 1 / (2 ** recursive_level)
        scale_factor = 0.5 * scale_baseline
        self.symbol_data = {
            "pos": (flag.w / 2, flag.h / 2),
            "scale": scale_factor,
            "size": flag.origin_h * scale_factor,
            "rotate": 0,
            "anchor_position": (flag.h / 2, flag.h / 2),
            "scale_baseline": scale_baseline
        }

        self.symbol_vector = []

        single_symbol = FlagSymbol(origin, flag, self.symbol_data)
        self.symbol_vector.append(single_symbol)

        self.flag_symbol_config = FlagSymbolConfig(origin, self, flag.w, flag.h)

    def draw(self):
        for symbol in self.symbol_vector:
            symbol.draw()
        # self.flag_symbol.draw()

    def multisymbol_vector(self):
        self.flag.symbol_chance = 1
        self.symbol_vector = []

    def add_symbol(self, sym_data):
        s = FlagSymbol(self.origin, self.flag, sym_data)
        self.symbol_vector.append(s)

    def create_main_symbol_for_data(self, sym_data):
        return FlagSymbol(self.origin, self.flag, sym_data)

    def create_main_symbol(self):
        return FlagSymbol(self.origin, self.flag, self.symbol_data)

    def add_symbol_directly(self, symbol):
        self.symbol_vector.append(symbol)
