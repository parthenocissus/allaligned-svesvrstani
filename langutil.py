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
import json
import time
from datetime import date, datetime


class LangUtil:
    EN = "en"
    SH = "sh"

    def __init__(self, flatpages):
        self.flatpages = flatpages
        self.max_project_count = 0
        self.projects_dir = 'projects'
        self.pages_dir = 'pages'
        self.notes_dir = 'notes'
        self.notes_tmp_dir = 'tmp/en'
        self.bntstn_atlas_dir = 'bntstn_atlas/en'
        self.svesvrstani_dir = 'svesvrstani/en'
        self.data = None

        base_path = 'static/data/'
        multilang_path = base_path + "multilang.json"
        picto_path = base_path + 'pictograms.json'

        with open(multilang_path, encoding="utf8") as json_file:
            self.lang_data = json.load(json_file)
        with open(picto_path, encoding="utf8") as json_file:
            self.pictogram_data = json.load(json_file)
        for tag in self.pictogram_data:
            tag["projects"] = self.__project_count_by_category(tag["id"])

    def params(self):
        return self.data

    def dir(self):
        return self.projects_dir

    def get_bntstn_atlas_dir(self):
        return self.bntstn_atlas_dir

    def get_svesvrstani_dir(self):
        return self.svesvrstani_dir

    def get_svesvrstani_dir_ext(self, path_end):
        return self.svesvrstani_dir + path_end

    def pgdir(self):
        return self.pages_dir

    def ntdir(self):
        return self.notes_dir

    def ntdir_tmp(self):
        return self.notes_tmp_dir

    def get_category_description(self, category):
        category_item = [i for i in self.data["pictodata"] if i["id"] == category][0]
        return category_item["name"]["description"]

    def get_tag_name(self, key, id):
        item = [i for i in self.data[key] if i["id"] == id][0]
        name = item["title"] if key != "pictodata" else item["name"]["title"]
        return name

    def note_date(self, note):
        element = datetime.strptime(note.meta["date"], "%d/%m/%Y")
        date_time = datetime.fromtimestamp(time.mktime(element.timetuple()))
        return date_time.strftime("%d %B, %Y")

    def note_date_short(self, note):
        element = datetime.strptime(note.meta["date"], "%d/%m/%Y")
        date_time = datetime.fromtimestamp(time.mktime(element.timetuple()))
        return date_time.strftime("%m/%d/%Y")

    def categories_html(self):
        return self.__tag_html("pictodata", "category", "anchor")

    def roles_html(self):
        return self.__tag_html("roles", "role", "role-anchor")

    def mediums_html(self):
        return self.__tag_html("mediums", "medium", "medium-anchor")

    def __tag_html(self, key, tag, anchor):
        html = "<div class='list'>"
        l = len(self.data[key]) - 1
        for i, item in enumerate(self.data[key]):
            link = self.data["paths"]["projects"] + self.data["paths"][tag] + item["id"]
            slash = " / " if i < l else ""
            title = item["title"] if tag != "category" else item["name"]["title"]
            html += "<a id='" + item[
                "id"] + "-" + anchor + "' class='anchors' href='" + link + "'>" + title + "</a>" + slash
        html += "</div>"
        return html

    def __project_count_by_category(self, tag):
        project_pages = [p for p in self.flatpages if p.path.startswith(self.projects_dir)]
        projects_tagged = list(filter(lambda x: (tag in map(lambda d: d["id"], x["category"])), project_pages))

        projects_data = []
        birth_year = datetime.strptime("1984", "%Y").year
        now_year = date.today().year

        for year in range(birth_year, now_year + 1):
            i = year - birth_year
            count_by_year = len(list(filter(lambda x: (year == x["date"]), projects_tagged)))
            if count_by_year > self.max_project_count:
                self.max_project_count = count_by_year
            projects_data.insert(i, {"year": str(year), "projectCount": count_by_year})

        return projects_data


class LangUtilEn(LangUtil):

    def __init__(self, flatpages):
        super().__init__(flatpages)
        self.data = self.lang_data['en_params']
        self.data['pictodata'] = self.pictogram_data
        self.data['max'] = self.max_project_count

    def img_term(self, project):
        return "Images"


class LangUtilSh(LangUtil):

    def __init__(self, flatpages):
        super().__init__(flatpages)
        self.projects_dir = '_projects_s'
        self.pages_dir = '_pages_s'
        self.notes_dir = '_notes_s'
        self.notes_tmp_dir = 'tmp/sh'
        self.bntstn_atlas_dir = 'bntstn_atlas/rs'
        self.svesvrstani_dir = 'svesvrstani/rs'
        self.data = self.lang_data['sh_params']
        self.data['pictodata'] = LangUtilSh.__fix_sh_pictodata(self.pictogram_data)
        self.data['max'] = self.max_project_count

    def img_term(self, project):
        val = "slika"
        images_length = len(project.meta["img_data"])
        last_digit = images_length % 10
        spec_digits = [2, 3, 4]
        exceptions = [12, 13, 14]
        if ((last_digit in spec_digits) and (images_length not in exceptions)):
            val = "slike"
        return val

    def note_date(self, note):
        element = datetime.strptime(note.meta["date"], "%d/%m/%Y")
        month = self.month_map(element.month)
        date_time = datetime.fromtimestamp(time.mktime(element.timetuple()))
        return date_time.strftime("%d. MMM %Y.").replace("MMM", month)

    def note_date_short(self, note):
        element = datetime.strptime(note.meta["date"], "%d/%m/%Y")
        date_time = datetime.fromtimestamp(time.mktime(element.timetuple()))
        return date_time.strftime("%d.%m.%Y.")

    def month_map(self, n):
        switcher = {
            1: "januar",
            2: "februar",
            3: "mart",
            4: "april",
            5: "maj",
            6: "jun",
            7: "jul",
            8: "avgust",
            9: "septembar",
            10: "oktobar",
            11: "novembar",
            12: "decembar"
        }
        return switcher.get(n, "")

    @staticmethod
    def __fix_sh_pictodata(pictogram_data):
        new_data = copy.deepcopy(pictogram_data)
        for p in new_data:
            p['name'] = p['nameS']
        return new_data
