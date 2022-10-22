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

import random
import time
from datetime import datetime
from itertools import groupby


def project(flatpages, lang, name):
    prj = flatpages.get_or_404('{}/{}'.format(lang.dir(), name))
    prj.meta["img_term"] = lang.img_term(prj)
    return prj


def note(flatpages, lang, name):
    nt = flatpages.get_or_404('{}/{}'.format(lang.ntdir(), name))
    nt.meta["proper_date"] = lang.note_date(nt)
    return nt


def note_tmp(flatpages, lang, name):
    nt = flatpages.get_or_404('{}/{}'.format(lang.ntdir_tmp(), name))
    nt.meta["proper_date"] = lang.note_date(nt)
    return nt


def teaching(flatpages, lang):
    page = flatpages.get_or_404('{}/{}'.format(lang.pgdir(), "teaching"))
    params = lang.params()
    workshops = "workshop"
    by = "category"
    projs = [p for p in flatpages if p.path.startswith(lang.dir())]
    workshop_projs = list(filter(lambda x: (workshops in map(lambda d: d["id"], x[by])), projs))
    workshop_projs.sort(key=lambda item: (item['date'], item['featured']), reverse=True)
    data = {
        "link": params["menu_items"][3]["link"],
        "title": params["menu_items"][3]["title"],
        "langlink": params["pages_captions"]["teaching_lang_link"],
        "projects": [0, 0, workshop_projs]
    }
    return page, data


def speaking(flatpages, lang):
    page = flatpages.get_or_404('{}/{}'.format(lang.pgdir(), "speaking"))
    params = lang.params()
    data = {
        "link": params["menu_items"][4]["link"],
        "title": params["menu_items"][4]["title"],
        "langlink": params["pages_captions"]["speaking_lang_link"]
    }
    return page, data


def press(flatpages, lang):
    page = flatpages.get_or_404('{}/{}'.format(lang.pgdir(), "press"))
    params = lang.params()
    data = {
        "link": params["menu_items"][5]["link"],
        "title": params["menu_items"][5]["title"],
        "langlink": params["pages_captions"]["press_lang_link"]
    }
    return page, data


def writing(flatpages, lang):
    diglit = "digital-literature"
    bantu = "bantustan-book"
    tactical = "optimised-tactical-poetics"
    research = "research"
    by = "category"
    params = lang.params()
    page = flatpages.get_or_404('{}/{}'.format(lang.pgdir(), "writing"))

    projs = [p for p in flatpages if p.path.startswith(lang.dir())]
    bantu_page = flatpages.get_or_404('{}/{}'.format(lang.dir(), bantu))
    tactical_page = flatpages.get_or_404('{}/{}'.format(lang.dir(), tactical))

    prose_projects = [bantu_page]

    diglit_projs = list(filter(lambda x: (x["id"] != bantu) and (diglit in map(lambda d: d["id"], x[by])), projs))
    diglit_projs.sort(key=lambda item: (item['date'], item['featured']), reverse=True)

    # research_projs = list(filter(lambda x: (research in map(lambda d: d["id"], x[by])), projs))
    research_projs = list(
        filter(lambda x: (x["id"] != tactical) and (research in map(lambda d: d["id"], x[by])), projs))
    research_projs.sort(key=lambda item: (item['date'], item['featured']), reverse=True)

    date_format = "%d/%m/%Y"
    note_list = [p for p in flatpages if p.path.startswith(lang.ntdir())]
    note_list.sort(key=lambda item: (__timeof(item['date'], date_format)), reverse=True)

    data = {
        "link": params["menu_items"][2]["link"],
        "title": params["menu_items"][2]["title"],
        "langlink": params["pages_captions"]["writing_lang_link"],
        "projects": [diglit_projs, prose_projects, research_projs],
        "notes": note_list[0:6]
    }
    return page, data


def about(flatpages, lang):
    page = flatpages.get_or_404('{}/{}'.format(lang.pgdir(), "about"))
    project_list = [p for p in flatpages if p.path.startswith(lang.dir())]
    project_list.sort(key=lambda item: (item['date'], item['featured']), reverse=True)
    timeline_data = [{"year": y, "projects": len(list(i))}
                     for y, i in groupby(project_list, lambda item: item['date'])]
    data = {
        "timeline": timeline_data
    }
    return page, data


def projects(flatpages, lang):
    lang_params = lang.params()
    project_list = [p for p in flatpages if p.path.startswith(lang.dir())]
    project_list.sort(key=lambda item: (item['date'], item['featured']), reverse=True)
    project_list_grouped = [{"year": y, "projects": list(i)}
                            for y, i in groupby(project_list, lambda item: item['date'])]
    timeline_data = [{"year": y, "projects": len(list(i))}
                     for y, i in groupby(project_list, lambda item: item['date'])]
    data = {
        "pictoid": "general",
        "lang_link_path": "",
        "tag_title": lang_params["tag_titles"]["all"],
        "name_title": lang_params["tag_titles"]["all_title"],
        "description": lang.categories_html(),
        "timeline": timeline_data
    }
    return project_list_grouped, data


def projects_by_category(flatpages, lang, by, criteria):
    lang_params = lang.params()
    pictoid = "general"
    project_pages = [p for p in flatpages if p.path.startswith(lang.dir())]
    filtered_projects = list(filter(lambda x: (criteria in map(lambda d: d["id"], x[by])), project_pages))
    filtered_projects.sort(key=lambda item: (item['date'], item['featured']), reverse=True)
    project_list_grouped = [{"year": y, "projects": list(i)} for y, i in
                            groupby(filtered_projects, lambda item: item['date'])]
    timeline_data = [{"year": y, "projects": len(list(i))}
                     for y, i in groupby(filtered_projects, lambda item: item['date'])]
    if by == "role":
        desc = lang.roles_html()
        name_title = lang.get_tag_name("roles", criteria)
    elif by == "medium":
        desc = lang.mediums_html()
        name_title = lang.get_tag_name("mediums", criteria)
    else:
        desc = "<div class='text'>" + lang.get_category_description(criteria) + "</div>"
        name_title = lang.get_tag_name("pictodata", criteria)
        pictoid = criteria
    data = {
        "pictoid": pictoid,
        "lang_link_path": by + "/" + criteria,
        "tag_title": lang_params["tag_titles"][by],
        "name_title": name_title,
        "description": desc,
        "timeline": timeline_data
    }
    return project_list_grouped, data


def note_list(flatpages, lang):
    date_format = "%d/%m/%Y"

    note_list = [p for p in flatpages if p.path.startswith(lang.ntdir())]
    note_list.sort(key=lambda item: (__timeof(item['date'], date_format)), reverse=True)

    for nt in note_list:
        nt.meta["proper_date"] = lang.note_date_short(nt)

    timeline_data = [{"year": y, "projects": len(list(i))}
                     for y, i in groupby(note_list, lambda item: (__yearof(item['date'], date_format)))]

    return {
        "timeline": timeline_data,
        "projects": note_list
    }


def __timeof(date, date_format):
    element = datetime.strptime(date, date_format)
    return time.mktime(element.timetuple())


def __yearof(date, date_format):
    return datetime.strptime(date, date_format).year


# Bantustan Interactive Atlas

def bntstn_home(flatpages, lang, name="_home"):
    page = flatpages.get_or_404(f'{lang.get_bntstn_atlas_dir()}/{name}')
    return __add_map_data(flatpages, lang, page)


def bntstn_map(flatpages, lang, name):
    map = flatpages.get_or_404(f'{lang.get_bntstn_atlas_dir()}/{name}')
    return __add_map_data(flatpages, lang, map)


def __add_map_data(flatpages, lang, page_data):
    maps = [m for m in flatpages if m.path.startswith(lang.get_bntstn_atlas_dir())]
    other_maps, chapter_maps, map_list = [], [], []
    for m in maps:
        if m["title"]["chapter"] != "page_type":
            other_maps.append(m) if m["title"]["chapter"] == "other" else chapter_maps.append(m)
            map_list.append({"id": m["id"],
                             "index": m["index"],
                             "title": m["title"]["name"],
                             "chapter": m["title"]["chapter"]})

    chapter_maps.sort(key=lambda item: item["index"], reverse=False)
    other_maps.sort(key=lambda item: item["index"], reverse=False)
    page_data.meta["chapter_maps"] = chapter_maps
    page_data.meta["other_maps"] = other_maps

    if page_data.meta["title"]["chapter"] != "page_type":
        page_data = __find_prev_and_next(page_data, map_list, lang.params())

    map_list.sort(key=lambda item: item["id"], reverse=True)
    page_data.meta["map_list"] = map_list

    return page_data


def __find_prev_and_next(page_data, map_list, lp):
    map_list.sort(key=lambda item: item["index"], reverse=False)
    index = page_data.meta["index"]
    last = len(map_list) - 1

    if index == map_list[0]["index"]:
        page_data = __set_prev_next(page_data, map_list, lp, last, 1)
    elif index == map_list[last]["index"]:
        page_data = __set_prev_next(page_data, map_list, lp, last - 1, 0)
    else:
        for i in range(1, last):
            if index == map_list[i]["index"]:
                page_data = __set_prev_next(page_data, map_list, lp, i - 1, i + 1)
                break

    return page_data


def __set_prev_next(page_data, map_list, lp, prev, next):
    def set_one(mapid, k):
        m = map_list[mapid]
        key = f"open_{k}_txt"
        title = lp["bntstn"][key] + m["title"]
        if m["chapter"] != "other":
            title += ", " + lp["bntstn"]["chapter"] + " " + m["chapter"]
        return {
            "id": m["id"],
            "title": title
        }

    page_data.meta["prev"] = set_one(prev, "prev")
    page_data.meta["next"] = set_one(next, "next")
    return page_data


# Svesvrstani / All-Aligned


def svesvrstani_page(flatpages, lang, name):
    return flatpages.get_or_404(f'{lang.get_svesvrstani_dir()}/{name}')


def svesvrstani_exhibition(flatpages, lang, name):
    return flatpages.get_or_404(f'{lang.get_svesvrstani_dir_ext("/exhibitions")}/{name}')


def svesvrstani_essay(flatpages, lang, name):
    return flatpages.get_or_404(f'{lang.get_svesvrstani_dir_ext("/essays")}/{name}')


def svesvrstani_exhibition_list(flatpages, lang, type):
    # lang_params = lang.params()
    page_params = flatpages.get_or_404(f'{lang.get_svesvrstani_dir()}/{type}')
    lang_dir = lang.get_svesvrstani_dir_ext(f'/{type}') + '/'
    page_list = [p for p in flatpages if p.path.startswith(lang_dir)]
    page_list.sort(key=lambda item: int(item['year']), reverse=False)
    page_list_grouped = {"first": [], "second": []}
    for p in page_list:
        print(p)
        if p['importance'] == "first":
            page_list_grouped['first'].append(p)
        else:
            page_list_grouped['second'].append(p)
    print(page_list_grouped)
    return page_params, page_list_grouped
