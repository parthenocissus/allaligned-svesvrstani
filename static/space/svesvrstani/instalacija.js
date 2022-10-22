/*
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
 */

$(document).ready(function () {

    // const genAPI = "_myflaggenerate";
    // const fromDatabaseAPI = "_myflagfromdatabase";

    const genAPI = "_generate_flags_clean";
    const fromDatabaseAPI = "_get_flags_from_database";

    let generate = (api) => {
        console.log("generating...");
        let flg = $("#flag");

        let genParams = {"n": 1};

        const urlGen = $SCRIPT_ROOT + api;

        $.getJSON(urlGen, genParams, (result) => {
            flg.empty();
            // flg.append(result.svg);
            flg.append(result[0]);
            let flagSvg = $("#flag-svg");
            flagSvg.removeAttr("width");
            flagSvg.removeAttr("height");
            flg.show();
            window.scrollTo(0, flg.offset().top - 70);
        }).done(() => {
            console.log("flag generated.");
            let svgH = $('#flag-svg').height();
            let viewportH = window.innerHeight;
            let svgTop = -(svgH - viewportH) / 2;
            $("#flag").css({top: svgTop + 'px'});
        });
    };

    setInterval(function () {
        let api = (Math.random() > .4) ? genAPI : fromDatabaseAPI;
        // let api = genAPI;
        // let api = fromDatabaseAPI;
        generate(api);
    }, 5000);

});