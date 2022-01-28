"use strict";

// return the name of the slider, or empty string if not a valid slider
function getSliderName(expr) {
    // get varname and value
    let latex = expr.latex;
    if (typeof (latex) != "string")
        return "";
    let equations = latex.replace(/\\ /g, '').split('=');
    if (equations.length != 2)
        return "";
    var varname = equations[0].trim();
    var value = equations[1].trim();
    // must be a valid value
    if (value == "" || value == ".")
        return "";
    if (!(/^\-?[0-9]*\.?[0-9]*$/.test(value)))
        return "";
    // must be a valid variable name
    if (varname == "\\pi")
        return "";
    var GREEK = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega", "varphi", "varpi", "varrho", "vartheta", "varepsilon"];
    var varname1 = varname;
    for (var i = 0; i < GREEK.length; i++) {
        var gl = GREEK[i];
        varname1 = varname1.replaceAll("\\" + gl, "Ω");
        if (gl.substring(0, 3) != "var") {
            gl = gl[0].toLocaleUpperCase() + gl.substring(1, gl.length);
            varname1 = varname1.replaceAll("\\" + gl, "Ω");
        }
    }
    varname1 = varname1.replace(/\s/g, '');
    if (!(/^[A-Za-zΩ](_\{[A-Za-z0-9]+\})?$/).test(varname1))
        return "";
    return varname;
}

// get a list of slider objects
function getSliders() {
    let expressions = Calc.getExpressions();
    var sliders = [];
    for (var i = 0; i < expressions.length; i++) {
        let expr = expressions[i];
        if (expr.type != "expression")
            continue;
        let varname = getSliderName(expr);
        if (varname != "") {
            sliders.push(expr);
        }
    }
    return sliders;
}

// set the value of a list of sliders with animation variable 0<=t<1
function setSliders(sliders, t) {
    for (var i = 0; i < sliders.length; i++) {
        var slider = sliders[i];
        var sliderBounds = slider.sliderBounds;
        if (sliderBounds == null)
            continue;
        var sliderMin = Number(String(sliderBounds.min));
        var sliderMax = Number(String(sliderBounds.max));
        if (isNaN(sliderMax - sliderMin)) {
            console.warn("Fail to parse slider bounds. Note that slider bounds must be numerical values.");
        }
        if (isNaN(sliderMin))
            sliderMin = -10.0;
        if (isNaN(sliderMax))
            sliderMax = 10.0;
        var sliderStep = Number(String(sliderBounds.step));
        if (isNaN(sliderStep))
            sliderStep = 0.0;
        var varname = getSliderName(slider);
        var value = sliderMin + (sliderMax - sliderMin) * t;
        if (sliderStep > 0.0) {
            value = sliderMin + Math.round((value - sliderMin) / sliderStep) * sliderStep;
        }
        slider.latex = varname + "=" + value;
        Calc.setExpression(slider);
    }
}

function displayImages(images) {
    var div = document.createElement("div");
    for (var i = 0; i < images.length; i++) {
        let image = images[i];
        var img = document.createElement("img");
        img.src = image;
        img.style.width = IMAGE_SIZE + "px";
        div.appendChild(img);
    }
    //document.write(div.innerHTML);
    console.log(div.innerHTML);
}

// get frames
function getFrames(framen, framei=0) {
    var t = (framei + 0.5) / framen;
    if (++framei > framen) {
        displayImages(frames);
        return;
    }
    console.log("Frame " + framei + "/" + framen);
    setSliders(sliders, t);
    Calc.asyncScreenshot({
        width: IMAGE_SIZE,
        height: IMAGE_SIZE
    }, function(data) {
        frames.push(data);
        requestAnimationFrame(function() {
            getFrames(framen, framei);
        });
    });
}

const IMAGE_SIZE = 512;
const FRAME_COUNT = 40;
let sliders = [getSliders()[0]];
var frames = [];

for (var i = 0; i < sliders.length; i++)
    console.log(sliders[i].latex);

getFrames(FRAME_COUNT);
