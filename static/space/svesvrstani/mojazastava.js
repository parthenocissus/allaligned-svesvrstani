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

    /* Sliders */

    let sliderHtml = (key, label, type, data) => {
        return `<div class="slider-div"><input type="range" ` +
            `id="${key}" name="${key}" min="${data.min}" max="${data.max}" ` +
            `value="${data.value}" step="${data.step}" data-input-type="${type}">` +
            `<label for="warm">${label}</label></div>`;
    };

    let sliderGroup = $('#slider-group');
    // let flagMap = parameters["mappings"];
    let flagMap = parameters;

    for (let key in flagMap) {
        if ((appText.slider_label === "label_sr") && ((key === "croatian") || (key === "islamic"))) {
            // skip
        } else {
            let type = flagMap[key]["type"];
            let label = flagMap[key]["label"];
            // let labelSr = flagMappings[key]["label_sr"];
            let data = flagMap[key]["data"];
            sliderGroup.append(sliderHtml(key, label, type, data));
        }
    }

    /* Buttons */

    let genPrime = $("#gen-prime");
    genPrime.click(() => {
        genPrime.hide();
        $("#under-buttons").show();
        generate();
    });

    $("#gen-secundum").click(() => {
        generate();
    });

    let generate = () => {
        console.log("generating...");
        let flg = $("#flag");
        flg.empty();

        let spinner = $("#spinner");
        spinner.show();

        let data = [];
        $("input[type=range]").each(function () {
            let input = $(this);
            let d = {
                "value": +input.val(),
                "key": input.attr("name"),
                "type": input.attr("data-input-type")
            };
            data.push(d);
        });
        let genParams = {vector: JSON.stringify(data)};

        let genAPI = "_myflaggenerate";
        let urlGen = $SCRIPT_ROOT + genAPI;
        $.getJSON(urlGen, genParams, (result) => {
            flg.append(result.svg);
            let flagSvg = $("#flag-svg");
            flagSvg.removeAttr("width");
            flagSvg.removeAttr("height");
            spinner.hide();
            flg.show();
            window.scrollTo(0, flg.offset().top - 70);
        }).done(() => {
            console.log("flag generated.");
        });
    };

    $(".continue").click(() => {
        $("#continued").show();
        window.scrollTo(0, $(".continue").offset().top - 70);

        saveData("{rezerva}", "{rezerva}", "{rezerva}", "{rezerva}", $("#saglasan").is(":checked"));
    });

    let svg2pngDownloader = () => {
        let s = {w: 600, h: 400};

        let flagSvg = $("#flag-svg");
        flagSvg.attr({
            "width": "150px",
            "height": "100px"
        });

        // let svg = $("#flag").html();
        let svg = flagSvg.get(0).outerHTML;

        let canvas = document.createElement("canvas");
        canvas.width = s.w;
        canvas.height = s.h;
        let context = canvas.getContext('2d');

        let v = canvg.Canvg.fromString(context, svg, {
            ignoreDimensions: true,
            scaleWidth: s.w,
            scaleHeight: s.h,
            offsetX: 56.25,
            offsetY: 37.5
        });
        v.start();

        let img = canvas.toDataURL("image/png");
        const link = document.createElement('a');
        link.download = 'flag.png';
        link.target = "_blank";
        link.href = canvas.toDataURL("image/png");
        link.click();

        flagSvg.removeAttr("width");
        flagSvg.removeAttr("height");

    }

    let saveData = (a1, a2, a3, email, checked) => {
        // let a1 = $("#q1").val();
        // let a2 = $("#q2").val();
        // let a3 = $("#q3").val();
        // let email = $("#q4").val();
        // let checked = $("#saglasan").is(":checked");

        let flagSvg = $("#flag-svg");
        let svg = flagSvg.get(0).outerHTML;
        let dataPoint = {
            flag: svg, q1: a1, q2: a2, q3: a3, email: email, checked: checked
        };
        // let dataPoint = {
        //     q1: a1, q2: a2, q3: a3, email: email, checked: checked
        // };

        dataPoint = JSON.stringify(dataPoint);

        let saveAPI = "_myflagsave";
        let urlSave = $SCRIPT_ROOT + saveAPI;
        let saveParams = {vector: dataPoint};
        $.post(urlSave, saveParams, function (data, status) {
            console.log(data);
            console.log(status);
        }).done(() => {
            // $.getJSON(urlSave, saveParams).done(() => {
            console.log("flag saved.");
        });

    }

    $(".get-flag").click(() => {

        let failed = $(".failed");
        failed.hide();

        let valid = true;
        $(".required").each(function () {
            let element = $(this);
            if (element.val() === "") {
                valid = false;
            }
        });

        if (valid) {
            let a1 = $("#q1").val();
            let a2 = $("#q2").val();
            let a3 = $("#q3").val();
            let email = $("#q4").val();
            let checked = $("#saglasan").is(":checked");
            saveData(a1, a2, a3, email, checked);

            svg2pngDownloader();

        } else {
            failed.show();
        }

    });

});