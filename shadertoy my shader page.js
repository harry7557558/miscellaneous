function max(a, b) {
    return a > b ? a : b;
}
function min(a, b) {
    return a < b ? a : b;
}

function toString(r, g, b, a) {
    return "rgba(" + Math.floor(255 * r) + "," + Math.floor(255 * g) + "," + Math.floor(255 * b) + "," + a + ")";
}
function gradientToString(c1, c2) {
    return "linear-gradient(to right, " + c1 + ", " + c2 + ")";
}
function stepToString(c1, c2, a) {
    // repeating-linear-gradient(#74ABDD, #74ABDD 49.9%, #498DCB 50.1%, #498DCB 100%)
    var al = " " + 100 * a + "%, ";
    return "repeating-linear-gradient(to right, " + c1 + "," + c1 + al + c2 + al + c2 + "100%)";
}
function getTime(s) {
    var y = Number(s.substr(0, 4)) - 2000;
    var m = Number(s.substr(5, 2)) - 1;
    var d = Number(s.substr(8, 2)) - 1;
    return 365 * y + 30 * m + d;    // Er...
}

function Customize() {
    //openTab('Shaders');
    //refreshShadersTable();

    var allshaders = document.getElementById("divShadersTable");
    var shaders = allshaders.getElementsByTagName("tr");
    var n = shaders.length;

    // get shader data
    var cells = [shaders[0].getElementsByTagName("td")], cell,
        url = [""], name = [""], status = [""],
        date = [NaN], views = [NaN], likes = [NaN], comments = [NaN], ratio = [0];
    var minDate = 1e+8, maxDate = 0, maxViews = 0, maxLikes = 0, maxComments = 0, maxRatio = 0;
    for (var i = 1; i < n; i++) {
        cell = shaders[i].getElementsByTagName("td");
        cells.push(cell);
        url.push(cell[0].getElementsByTagName("a")[0].href);
        name.push(cell[1].innerText);
        status.push(cell[6].innerText);
        // date
        date.push(getTime(cell[2].innerText));
        maxDate = max(date[i], maxDate), minDate = min(date[i], minDate);
        // views
        views.push(Number(cell[3].innerText));
        maxViews = max(views[i], maxViews);
        // likes
        likes.push(Number(cell[4].innerText));
        maxLikes = max(likes[i], maxLikes);
        // comments
        comments.push(Number(cell[5].innerText));
        maxComments = max(comments[i], maxComments);
        // ratio of likes to views
        ratio.push(likes[i] / views[i]);
        if (isNaN(ratio[i])) ratio[i] = 0;
        maxRatio = max(ratio[i], maxRatio);
    }

    shaders[0].style.height = "30px";
    for (var i = 1; i < n; i++) {
        shaders[i].style.backgroundImage = "linear-gradient(white, aliceblue)";
        var cell = cells[i];
        // views, red
        col = toString(1, 0, 0, 1.0 - Math.exp(-0.005 * views[i]));
        cell[3].style.backgroundColor = col;
        cell[3].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", views[i] / max(100, 50 * Math.ceil((maxViews + 1) / 50)));
        // likes, green
        col = toString(0, 1, 0, 1.0 - Math.exp(-0.05 * likes[i]));
        cell[4].style.backgroundColor = col;
        cell[4].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", likes[i] / max(10, 5 * Math.ceil((maxLikes + 1) / 5)));
        // comments, blue
        col = toString(0, 0, 1, 1.0 - Math.exp(-0.05 * comments[i]));
        cell[5].style.backgroundColor = col;
        cell[5].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", comments[i] / max(5, maxComments + 1));
        // status, yellow
        col = toString(1, 0.6, 0, 1.0 - Math.exp(-5.0 * ratio[i]));
        cell[6].style.backgroundColor = col;
        cell[6].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", ratio[i] / 0.3);
        var str = (100 * ratio[i]).toFixed(2) + "% like";
        if (str.length < 11) str = "0" + str;
        cell[6].innerText = str;
    }
}

Customize();
//document.getElementById("tabShaders").setAttribute("onClick", "javascript: Customize();");
