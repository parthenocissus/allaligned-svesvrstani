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
import json
from copy import copy, deepcopy


class InputDataUtil:

    def __init__(self, default_rules, input_ponders, raw_input,
                 domain=(-1, 1), range=(-3, 5)):

        self.raw_input = [d for d in deepcopy(raw_input) if d['value'] != 0]
        self.rules = default_rules
        self.input_ponders = input_ponders
        self.domain = domain
        self.range = range
        self.particular_colors = self.list_particular_colors()

        self.rule_keys = ["layout", "colors", "symbols", "direct_rules", "particular_colors"]
        self.data = {}

        self.process_raw_input()

    # Simple proportional mapping, from one range to another
    @staticmethod
    def map_range(n, domain, range):
        return ((n - domain[0]) / (domain[1] - domain[0])) * (range[1] - range[0]) + range[0]

    # Specially designed exponential function
    # For mapping a pondered input value
    # Onto a factor in default rules
    def exponential_map(self, value, ponder, domain=None, range=None):
        if domain is None:
            domain = self.domain
        if range is None:
            range = self.range
        half_range = (range[1] - range[0]) / 2
        zero = range[1] - half_range
        pondered_range = (zero - ponder * half_range, zero + ponder * half_range)
        value = InputDataUtil.map_range(value, domain, pondered_range)
        result = math.exp(value) / math.e
        return result

    # Append particular colors
    # (granular ones within primary color groups)
    def list_particular_colors(self):
        particular_colors = []
        for primary in self.rules['colors']:
            for color in primary['variations']:
                particular_colors.append(color)
        return particular_colors

    # Check if inverse applies
    # Inverse value if ponder is negative
    def check_value(self, value, ponder):
        if ponder < 0:
            inverse = (self.domain[1], self.domain[0])
            return InputDataUtil.map_range(value, self.domain, inverse)
        else:
            return value

    # Adjust bipolar values from domain (-1, 1) onto range (0, 1)
    def adjust_to_half_range(self, value, type):
        if type == 'bipolar':
            half_range = (0, self.domain[1])
            return InputDataUtil.map_range(value, self.domain, half_range)
        else:
            return value

    # Get all symbols by tags
    def tags2symbols(self, tags):
        symb = {}
        # print(tags)
        for t in tags:
            # print(t)
            # print(tags[t])
            symbol_rules = [r for r in self.rules['symbols'] if t in r['tags']]
            # print(symbol_rules)
            for sr in symbol_rules:
                value = tags[t]
                if sr['name'] in symb:
                    value = symb[sr['name']] if symb[sr['name']] > tags[t] else tags[t]
                symb[sr['name']] = value
        return symb

    # Create a pool of new filters
    # Getting ponders from input-ponders
    # for every record in raw data input
    def process_raw_input(self):
        for r in self.raw_input:
            ponders = self.input_ponders[r['key']]

            # new tag-based system for calculating symbol probability distributions
            if 'symbols' in ponders:
                ponders['symbols'] = self.tags2symbols(ponders['symbols'])
            # print(ponders['symbols'])

            ponder_keys = [k for k in ponders.keys() if k != "meta_data"]
            for pk in ponder_keys:
                for name in ponders[pk].keys():
                    v = self.check_value(r['value'], ponders[pk][name])
                    p = abs(ponders[pk][name])
                    if (pk, name) not in self.data:
                        self.data[(pk, name)] = {
                            'value': v,
                            'ponder_total': p,
                            'ponder_count': 1,
                            'type': r['type']
                        }
                    else:
                        vd = self.data[(pk, name)]['value']
                        ptd = self.data[(pk, name)]['ponder_total']
                        pc = self.data[(pk, name)]['ponder_count']
                        self.data[(pk, name)] = {
                            'value': (vd * ptd + v * p) / (ptd + p),
                            'ponder_total': ptd + p,
                            'ponder_count': pc + 1,
                            'type': r['type']
                        }

    # Calculating ponders for each rule
    def update_rules(self):
        for k in self.data.keys():
            key, name = k
            v = self.data[k]['value']
            p = self.data[k]['ponder_total'] / self.data[k]['ponder_count']
            if key == 'direct_rules':
                t = self.data[k]['type']
                v = self.adjust_to_half_range(v, t)
                self.rules[key][name] = v * p
            elif key == 'particular_colors':
                rule = [r for r in self.particular_colors if r['name'] == name][0]
                factor = self.exponential_map(v, p)
                rule['weight'] *= factor
            else:
                rule = [r for r in self.rules[key] if r['name'] == name][0]
                factor = self.exponential_map(v, p)
                rule['weight'] *= factor

        print(self.rules)
        return self.rules


if __name__ == '__main__':
    rules_path = 'conf/flag-rules.json'
    symbols_path = 'conf/flag-symbols.json'
    rules = json.load(open(rules_path))
    symbols = json.load(open(symbols_path))
    rules['symbols'] = symbols['symbols']

    input_ponders_path = 'conf/input-ponders.json'
    input_ponders = json.load(open(input_ponders_path, encoding="utf8"))

    # dummy_input = [
    #     {"key": "warm", "value": 0.5, "type": "bipolar"},
    #     {"key": "complex", "value": 0.8, "type": "bipolar"},
    #     {"key": "anarchist", "value": 0, "type": "unipolar"},
    #     {"key": "african", "value": 0, "type": "unipolar"},
    #     {"key": "slavic", "value": 1, "type": "unipolar"},
    #     {"key": "corporate", "value": 0, "type": "unipolar"}
    # ]
    # dummy_input = [
    #     # {"key": "serbian", "value": 1, "type": "unipolar"},
    #     # {"key": "yugoslav", "value": 1, "type": "unipolar"},
    #     {"key": "anarchist", "value": 1, "type": "unipolar"}
    # ]
    dummy_input = [
        # {"key": "serbian", "value": 1, "type": "unipolar"},
        # {"key": "yugoslav", "value": 1, "type": "unipolar"},
        {"key": "warm", "value": 1, "type": "bipolar"}
    ]

    iu = InputDataUtil(default_rules=rules, input_ponders=input_ponders, raw_input=dummy_input)
    iu.update_rules()
    # iu.process_raw_input()
    # iu.update_rules()
