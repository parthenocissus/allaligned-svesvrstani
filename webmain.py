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

import sys
import json
from flask import Flask, render_template, send_file, redirect, request
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import utils
import random
from langutil import LangUtilEn, LangUtilSh
from bin.allaligned.allaligned_facade import MyFlagFacadeUtil


app = Flask(__name__)

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'

app = Flask(__name__)
fp = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

en = LangUtilEn(fp)
sh = LangUtilSh(fp)


# _________________________
# SVESVRSTANI / ALL-ALIGNED
# a special web app for generating flags


mf = MyFlagFacadeUtil()


@app.route("/svesvrstani")
@app.route("/svesvrstani/home")
def svesvrstani():
    lp, params = mf.flag_mappings("sr")
    return render_template('svesvrstani/svesvrstani-main.html', params=params, lp=lp)


@app.route("/")
@app.route("/all-aligned")
@app.route("/all-aligned/home")
def allaligned():
    lp, params = mf.flag_mappings("en")
    return render_template('svesvrstani/svesvrstani-main.html', params=params, lp=lp)


@app.route("/svesvrstani/generator")
def svesvrstani_generator():
    lp, params = mf.flag_mappings("sr")
    return render_template('svesvrstani/svesvrstani-generator.html', params=params, lp=lp)


@app.route("/all-aligned/generator")
def allaligned_generator():
    lp, params = mf.flag_mappings("en")
    return render_template('svesvrstani/svesvrstani-generator.html', params=params, lp=lp)


@app.route("/svesvrstani/concept")
def svesvrstani_concept():
    page = utils.svesvrstani_page(fp, sh, "concept")
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("sr"))


@app.route("/all-aligned/concept")
def allaligned_concept():
    page = utils.svesvrstani_page(fp, en, "concept")
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("en"))


@app.route("/svesvrstani/code")
def svesvrstani_code():
    page = utils.svesvrstani_page(fp, sh, "code")
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("sr"))


@app.route("/all-aligned/code")
def allaligned_code():
    page = utils.svesvrstani_page(fp, en, "code")
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("en"))


@app.route("/svesvrstani/support")
def svesvrstani_support():
    page = utils.svesvrstani_page(fp, sh, "support")
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("sr"))


@app.route("/all-aligned/support")
def allaligned_support():
    page = utils.svesvrstani_page(fp, en, "support")
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("en"))


@app.route('/svesvrstani/exhibitions/<name>/')
def svesvrstani_exhibition_page(name):
    page = utils.svesvrstani_exhibition(fp, sh, name)
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("sr"))


@app.route('/all-aligned/exhibitions/<name>/')
def allaligned_exhibition_page(name):
    page = utils.svesvrstani_exhibition(fp, en, name)
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("en"))


@app.route('/svesvrstani/essays/<name>/')
def svesvrstani_essay_page(name):
    page = utils.svesvrstani_essay(fp, sh, name)
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("sr"))


@app.route('/all-aligned/essays/<name>/')
def allaligned_essay_page(name):
    page = utils.svesvrstani_essay(fp, en, name)
    return render_template('svesvrstani/svesvrstani-regular-page.html', params={}, page=page, lp=mf.lp("en"))


@app.route('/svesvrstani/exhibitions')
def svesvrstani_exhibitions():
    params, plist = utils.svesvrstani_exhibition_list(fp, sh, "exhibitions")
    return render_template('svesvrstani/svesvrstani-list-page.html', params=params, list=plist, lp=mf.lp("sr"))


@app.route('/all-aligned/exhibitions')
def allaligned_exhibitions():
    params, plist = utils.svesvrstani_exhibition_list(fp, en, "exhibitions")
    return render_template('svesvrstani/svesvrstani-list-page.html', params=params, list=plist, lp=mf.lp("en"))


@app.route('/svesvrstani/essays')
def svesvrstani_essays():
    params, plist = utils.svesvrstani_exhibition_list(fp, sh, "essays")
    return render_template('svesvrstani/svesvrstani-list-page.html', params=params, list=plist, lp=mf.lp("sr"))


@app.route('/all-aligned/essays')
def allaligned_essays():
    params, plist = utils.svesvrstani_exhibition_list(fp, en, "essays")
    return render_template('svesvrstani/svesvrstani-list-page.html', params=params, list=plist, lp=mf.lp("en"))


# Svesvrstani Other Apps


@app.route("/svesvrstani-instalacija")
def svesvrstani_instalacija():
    lp, params = mf.flag_mappings("sr")
    return render_template('svesvrstani/svesvrstani-instalacija.html', params=params, lp=lp)


@app.route("/svesvrstani-app")
def svesvrstani_app():
    lp, params = mf.flag_mappings("sr")
    return render_template('svesvrstani/svesvrstani-home.html', params=params, lp=lp)


@app.route("/all-aligned-app")
def allaligned_app():
    lp, params = mf.flag_mappings("en")
    return render_template('svesvrstani/svesvrstani-home.html', params=params, lp=lp)


# Svesvrstani API


@app.route('/_myflagsave', methods=['POST'])
def myflagsave():
    print(request.form['vector'])
    mf.save_data(request.form['vector'])
    return json.dumps({"info": "success"})


@app.route('/_myflagdelete')
def myflagdelete():
    mf.delete_data(request.args.get('vector'))
    return json.dumps({"info": "success"})

@app.route('/_myflagdeleteall')
def myflagdeleteall():
    mf.delete_all_data()
    return json.dumps({"info": "success"})


@app.route('/_myflaggenerate')
def myflaggenerate():
    svg = mf.generate_flag(request.args.get('vector'))
    return json.dumps({"svg": svg})


@app.route('/_generate_flags')
def generate_flags():
    svg_data = mf.get_flag_random(request)
    return json.dumps(svg_data)


@app.route('/svesvrstani/_generate_flags')
@app.route('/all-aligned/_generate_flags')
def generate_flags_website():
    svg_data = mf.get_flag_random_viewbox(request, 16)
    return json.dumps(svg_data)


@app.route('/_generate_flags_clean')
def generate_flags_clean():
    svg_data = mf.get_flag_random_clean(request)
    return json.dumps(svg_data)


@app.route('/_get_flags_from_database')
def get_flags_from_database():
    svg_data = mf.get_flag_from_database(request)
    return json.dumps(svg_data)


# MAIN
# starting app

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        # app.run(host='0.0.0.0', debug=True)
        app.run(host='127.0.0.1', debug=True)
        # app.run(host='0.0.0.0')
