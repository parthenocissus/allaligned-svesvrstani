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
import time
from os import listdir
from os.path import isfile, join

# import glob
import random
from random import randint
# from random import random

from flask import send_file

from bin.allaligned.flag_generator import GenFlag

from glob import glob, iglob
from io import BytesIO
from zipfile import ZipFile
import os


class MyFlagFacadeUtil:

    def __init__(self):
        self.input_ponders_path = 'static/space/svesvrstani/conf/input-ponders.json'
        self.lang_path = 'static/space/svesvrstani/conf/allaligned-multilang.json'
        self.database_path = 'static/space/svesvrstani/database/'
        self.database2_path = 'static/space/svesvrstani/database2/'
        self.database_final_path = 'static/space/svesvrstani/database_final/'
        self.selected_flags = 'static/space/svesvrstani/selected_flags/'
        self.current_flag_svg = ""
        self.n_flags = 35

        with open(self.lang_path, encoding="utf8") as json_file:
            self.lang = json.load(json_file)

    def generate_flag(self, data_txt):
        data = json.loads(data_txt)
        gf = GenFlag(raw_input=data, raw=True)
        svg = gf.svg_string()
        svg = f'{svg[:4]} id="flag-svg" viewBox="0 0 150 100" preserveAspectRatio="xMidYMid meet" {svg[5:]}'
        svg = svg.replace('height="100px"', '').replace('width="150px"', '')
        # self.current_flag_svg = svg
        return svg

    def get_flag_from_database(self, request):
        n = int(json.loads(request.args.get('n')))
        svg_data = []
        path = self.selected_flags
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for _ in range(n):
            file_name = random.choice(files)
            full_name = f"{path}/{file_name}"
            svg = open(full_name, "r").read()
            # svg = f'{svg[:4]} id="flag-svg" viewBox="0 0 150 100" preserveAspectRatio="xMidYMid meet" {svg[5:]}'
            svg = svg.replace('height="100px"', '').replace('width="150px"', '')
            svg = svg.replace('version="1.1"',
                              'id="flag-svg" viewBox="0 0 150 100" preserveAspectRatio="xMidYMid meet"')
            svg_data.append(svg)
        return svg_data

    def get_flag_random(self, request, n=0):
        # raw_input = json.loads(request.args.get('raw'))
        if n == 0:
            n = self.n_flags
        data_txt = request.args.get('vector')
        data = json.loads(data_txt)
        svg_data = []
        for i in range(n):
            gf = GenFlag(raw_input=data, raw=True)
            # gf = GenFlag()
            svg = gf.svg_string()
            svg = f'{svg[:4]} id="flag{i}" {svg[5:]}'
            # svg = f'{svg[:4]} id="flag-svg" viewBox="0 0 150 100" preserveAspectRatio="xMidYMid meet" {svg[5:]}'
            # svg = svg.replace('height="100px"', '').replace('width="150px"', '')
            svg_data.append(svg)
        return svg_data

    def get_flag_random_viewbox(self, request, n=0):
        # raw_input = json.loads(request.args.get('raw'))
        if n == 0:
            n = self.n_flags
        data_txt = request.args.get('vector')
        data = json.loads(data_txt)
        svg_data = []
        for i in range(n):
            gf = GenFlag(raw_input=data, raw=True)
            # gf = GenFlag()
            svg = gf.svg_string()
            # svg = f'{svg[:4]} id="flag{i}" {svg[5:]}'
            svg = f'{svg[:4]} id="flag{i}" viewBox="0 0 150 100" preserveAspectRatio="xMidYMid meet" {svg[5:]}'
            svg = svg.replace('height="100px"', '').replace('width="150px"', '')
            svg_data.append(svg)
        return svg_data

    def get_flag_random_clean(self, request):
        # raw_input = json.loads(request.args.get('raw'))
        n = json.loads(request.args.get('n'))
        # data_txt = request.args.get('vector')
        # data = json.loads(data_txt)
        svg_data = []
        for i in range(n):
            # gf = GenFlag(raw_input=data, raw=True)
            gf = GenFlag()
            svg = gf.svg_string()
            # svg = f'{svg[:4]} id="flag{i}" {svg[5:]}'
            svg = f'{svg[:4]} id="flag-svg" viewBox="0 0 150 100" preserveAspectRatio="xMidYMid meet" {svg[5:]}'
            svg = svg.replace('height="100px"', '').replace('width="150px"', '')
            svg_data.append(svg)
        return svg_data

    def save_data(self, data):
        data = json.loads(data)
        # data['flag'] = self.current_flag_svg
        time_stamp = time.strftime("%Y%m%d-%H%M%S") + "_" + str(time.time() * 1000)
        time_stamp = time_stamp + '_' + str(randint(100, 1000))
        file_name = self.database_path + time_stamp + '.json'
        file_name2 = self.database2_path + time_stamp + '.json'
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open(file_name2, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def delete_data(self, file_name):
        os.remove(file_name)

    def delete_all_data(self):
        path = self.database_path + "*"
        for file_name in iglob(path):
            os.remove(file_name)

    def read_data(self):
        path = self.database_path + "*"
        db = []
        for file_name in iglob(path):
            d = open(file_name, "r", encoding="utf8").read()
            d = json.loads(d)
            d["file_name"] = file_name
            d = json.dumps(d)
            db.append(d)
        db.sort()
        return db

    def read_data_final(self):
        path = self.database_final_path + "*"
        db = []
        for file_name in iglob(path):
            d = open(file_name, "r", encoding="utf8").read()
            d = json.loads(d)
            d["file_name"] = file_name
            d = json.dumps(d)
            db.append(d)
        db.sort()
        return db

    def download_data(self):
        stream = BytesIO()
        target = self.database2_path  # database_path
        with ZipFile(stream, 'w') as zf:
            for file in glob(os.path.join(target, '*.json')):
                zf.write(file, os.path.basename(file))
        stream.seek(0)
        return send_file(stream, as_attachment=True, attachment_filename='archive.zip')

    def lp(self, language):
        lang_key = language + "_params"
        return self.lang[lang_key]["myflag"]

    def flag_mappings(self, language):
        lang_key = language + "_params"
        lp = self.lang[lang_key]["myflag"]
        with open(self.input_ponders_path, encoding="utf8") as json_file:
            input_ponders = json.load(json_file)
        mappings = {}

        def data_for_type(t):
            if t == "unipolar":
                return {"min": 0, "max": 1, "step": 0.1, "value": 0}
            else:
                return {"min": -1, "max": 1, "step": 0.2, "value": 0}

        for p in input_ponders:
            md = input_ponders[p]['meta_data']
            mappings[p] = {
                # "label": md['label'],
                # "label_sr": md['label_sr'],
                "label": md[lp["slider_label"]],
                "type": md['type'],
                "data": data_for_type(md['type'])
            }

        return lp, json.dumps(mappings)
