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

import copy
import math
from random import choices, random, randint, uniform, randrange
from svgpathtools import svg2paths, svg2paths2, wsvg
from xml.etree import ElementTree as ET


class FlagSymbol:

    def __init__(self, origin, flag, sym_data):
        self.genflag_origin = origin
        self.flag = flag
        self.symbol_data = sym_data
        self.fc = flag.fc
        self.w = flag.w
        self.h = flag.h
        self.origin_h = origin.h
        self.complexity = origin.complexity
        self.complex_factor = math.pow(self.complexity, 3)
        self.rndclr_chance = 0.8
        self.rules = flag.rules
        self.used_colors = flag.used_colors

        self.color_vector = []

        self.symbols = self.rules['symbols']
        self.symbol_chance = flag.symbol_chance
        self.symbol = None
        self.build_symbol = None

        self.set_symbol()
        self.change_alternating(1)
        self.colors_defined = False

    # Draw symbol
    def draw(self):
        if not self.colors_defined:
            self.define_colors()
        symbol = self.build_symbol(self.symbol_data)
        self.fc.add(symbol)

    # Copy object
    def copy(self, sym_data):
        symbol_copy = FlagSymbol(self.genflag_origin, self.flag, sym_data)
        # symbol_copy.use_color_vector = True
        symbol_copy.build_symbol = self.build_symbol
        return symbol_copy

    # Define colors
    def define_colors(self):
        self.change_alternating(1)
        if self.symbol is None:
            return

        f = self.choose_different_color()
        if 'color' in self.symbol and self.symbol['color'] == 'full':
            s = 'none'
            sw = 0
        else:
            s = self.choose_different_color() if random() < self.complex_factor else 'none'
            sw = self.h * 0.01 * randrange(2, 4)
        rnd = random()

        if 'paths' in self.symbol:
            for path in self.symbol['paths']:
                if 'fill' in path:
                    f = path['fill'] if rnd > self.rndclr_chance else self.choose_different_color()
                if 'stroke' in path:
                    s = path['stroke'] if rnd > self.rndclr_chance else self.choose_different_color()
                self.color_vector.append({"fill": f, "stroke": s, "stroke_width": sw})
        else:
            self.color_vector.append({"fill": f, "stroke": s, "stroke_width": sw})

        self.colors_defined = True

    # Set symbol
    def set_symbol(self):
        # Set symbol (eg. coat of arms, a circle, a star, etc)
        if random() < self.flag.symbol_chance:
            self.symbol = self.choose_symbol()
        else:
            self.build_symbol = self.empty_symbol

    # Choose a color
    def choose_different_color(self):
        return self.flag.choose_different_color()

    # Alternating color fix
    def change_alternating(self, unalternate=0.5):
        if self.flag.alternating and random() < unalternate:
            self.flag.choose_different_color = self.flag.choose_different_color_default
            self.flag.alternating = False

    # Build symbol from paths taken from a SVG file
    def build_symbol_from_paths(self, symbol_data):
        symbol_data_copy = copy.deepcopy(symbol_data)
        d = FlagSymbol.center_symbol(symbol_data_copy)
        return self.paths2symbol(d['pos'], d['scale'], d['rotate'], d['anchor_position'])

    # Recenter the symbol
    @staticmethod
    def center_symbol(symbol_data):
        x, y = symbol_data['pos']
        symbol_data['pos'] = (x - symbol_data['size'] / 2,
                              y - symbol_data['size'] / 2)
        return symbol_data

    # Create a single symbol from paths and put it in a group (<g> element)
    def paths2symbol(self, position=(0, 0), scale=1, rotation_angle=0, anchor_position=(50, 50)):
        x, y = position
        anchor_x, anchor_y = anchor_position
        t = f"translate({x}, {y}) scale({scale}) rotate({rotation_angle}, {anchor_x}, {anchor_y})"
        group = self.fc.g(transform=t)
        for i, path in enumerate(self.symbol['paths']):
            cv = self.color_vector[i]
            f = cv["fill"]
            s = cv["stroke"]
            sw = cv["stroke_width"]
            svg_path = self.fc.path(d=path['d'], fill=f, stroke=s, stroke_width=f'{sw}px')
            group.add(svg_path)
        return group

    # Choose a symbol (eg. coat of arms, a circle, a star, etc)
    def choose_symbol(self):
        distribution = [d['weight'] for d in self.rules['symbols']]
        symbol = choices(self.rules['symbols'], distribution)[0]
        if 'file_name' in symbol:
            try:
                symbol['paths'] = self.get_svg_paths(symbol['file_name'])
                self.build_symbol = self.build_symbol_from_paths
            except:
                print(symbol['file_name'])
        else:
            self.build_symbol = getattr(self, symbol['name'])
        return symbol

    # Empty symbol
    def empty_symbol(self, d):
        return self.fc.g(id="empty")

    # Open a SVG file and get all path-related data
    def get_svg_paths(self, file_name):
        path = f"{self.genflag_origin.symbols_typical_dir}{file_name}.svg"
        path_data = []
        paths, attrs, svg_attrs = svg2paths2(path)
        for p, a in zip(paths, attrs):
            path_object = {'d': p.d()}
            if 'fill' in a:
                path_object['fill'] = a['fill']
            if 'stroke' in a:
                path_object['stroke'] = a['stroke']
            path_data.append(path_object)
        return path_data

    # _________________________
    # SYMBOL DRAWING METHODS

    # Circle
    def circle(self, d):
        # d = self.symbol_data
        c = self.choose_different_color()
        return self.fc.circle(center=d['pos'], r=d['size'] * 0.4, fill=c, stroke='none')

    # Ring
    def ring(self, d):
        # d = self.symbol_data
        c = self.choose_different_color()
        r = d['size'] * 0.5
        sw = self.h * uniform(0.05, 0.15)
        return self.fc.circle(center=d['pos'], r=r, fill='none', stroke=c, stroke_width=f'{sw}px')

    # Random Star
    def random_star(self, d):
        # d = self.symbol_data
        c = self.choose_different_color()
        n = randint(5, 10)
        x, y = d['pos']
        rad1 = d['size'] / 2
        rad2 = rad1 * uniform(0.3, 0.9)
        angle = 2 * math.pi / n
        half_angle = angle / 2
        path_d = ""
        letter = "M"
        for i in range(n):
            a1 = angle * i
            a2 = a1 + half_angle
            x1, y1 = x + math.cos(a1) * rad1, y + math.sin(a1) * rad1
            x2, y2 = x + math.cos(a2) * rad2, y + math.sin(a2) * rad2
            path_d += f"{letter} {x1} {y1} L {x2} {y2} "
            letter = "L"
        path_d += "z"
        path = self.fc.path(d=path_d, fill=c, stroke='none')
        return path
