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

    let sliderHtml = (key, label, type, data) => {
        return `<div id="slider-group"><div class="slider-div"><input type="range" ` +
            `id="${key}" name="${key}" min="${data.min}" max="${data.max}" ` +
            `value="${data.value}" step="${data.step}" data-input-type="${type}">` +
            `<label for="warm">${label}</label></div></div>`;
    };

    let selectHtml = (key, label) => {
        return `<option value="${key}">${label}</option>`;
    };

    let chosen = $(".chosen");
    let sliderGroup = $('#slider-group');
    let sliderHeader = $('#slider-header');

    for (let key in flagMappings) {
        $("#choose-params").append(selectHtml(key, flagMappings[key]["label"]));
        // console.log(flagMappings[key]["label"]);
    }

    chosen.chosen({max_selected_options: 7})
        .change(function () {
            sliderGroup.empty();
            let keys = $(this).val();
            let visible = (keys.length > 0) ? "visible" : "hidden";
            sliderHeader.css("visibility", visible);
            keys.forEach(key => {
                let type = flagMappings[key]["type"];
                let label = flagMappings[key]["label"];
                let data = flagMappings[key]["data"];
                sliderGroup.append(sliderHtml(key, label, type, data));
            });
        });

    chosen.bind("chosen:maxselected", () => {
        alert("Max parameters limit reached.");
    });

});