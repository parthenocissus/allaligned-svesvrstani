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

import json
from colour import Color


def list_colors():
    rules_path = 'conf/flag-rules.json'
    rules = json.load(open(rules_path))

    css_begin = '* {'
    css_end = '\n}'

    light_colors = '\n\n\t/* Light colors */'
    other_colors = '\n\n\t/* Mid-colors */'
    dark_colors = '\n\n\t/* Dark colors */'

    color_dict = {"particular_colors": {}}

    color_groups = rules['colors']
    for cg in color_groups:
        for v in cg['variations']:

            color = Color(v['value'])
            luminance = color.get_luminance()
            lum = "{:.2f}".format(luminance)
            css_color = f"\n\tcolor: {v['value']};  /* {v['name']}, {lum} */"

            if luminance < 0.4:
                dark_colors += css_color
                color_dict['particular_colors'][v['name']] = -1
            elif luminance > 0.5:
                light_colors += css_color
                color_dict['particular_colors'][v['name']] = 1
            else:
                other_colors += css_color



    css = css_begin + light_colors + other_colors + dark_colors + css_end
    with open('static/css/colors_list.css', 'w') as f:
        f.write(css)

    with open('media/tmp/colors_list.json', 'w') as f:
        json.dump(color_dict, f)


if __name__ == '__main__':
    list_colors()