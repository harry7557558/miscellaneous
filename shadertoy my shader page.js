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
    var y = new Number(s.substr(0, 4)) - 2000;
    var m = new Number(s.substr(5, 2)) - 1;
    var d = new Number(s.substr(8, 2)) - 1;
    return 365 * y + 30 * m + d;
}

function Customize() {
    //openTab('Shaders');
    //refreshShadersTable();

    var allshaders = document.getElementById("divShadersTable");
    var shaders = allshaders.getElementsByTagName("tr");

    shaders[0].style.height = "30px";
    for (var i = 0; i < shaders.length; i++) {
        var cell = shaders[i].getElementsByTagName("td");
        if (i != 0) {
            //shaders[i].style.backgroundColor = "white";
            shaders[i].style.backgroundImage = "linear-gradient(white, aliceblue)";
        }
        //if (cell.length == 8) shaders[i].deleteCell(7);
    }

    for (var i = 1; i < shaders.length; i++) {
        var cell = shaders[i].getElementsByTagName("td");
        var preview = cell[0].getElementsByClassName("bigPreview")[0].src;
        var url = cell[0].getElementsByTagName("a")[0].href;
        var name = cell[1].innerText;
        var date = cell[2].innerText;
        var views = new Number(cell[3].innerText);
        var likes = new Number(cell[4].innerText);
        var comments = new Number(cell[5].innerText);
        var status = cell[6].innerText;

        col = toString(1, 0, 0, 1.0 - Math.exp(-0.005 * views));
        cell[3].style.backgroundColor = col;
        cell[3].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", views / 150);
        col = toString(0, 1, 0, 1.0 - Math.exp(-0.05 * likes));
        cell[4].style.backgroundColor = col;
        cell[4].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", likes / 12);
        col = toString(0, 0, 1, 1.0 - Math.exp(-0.05 * comments));
        cell[5].style.backgroundColor = col;
        cell[5].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", comments / 5);

        //var time = getTime(date) - getTime("2019-09-01");
        //time = 1.0 - Math.exp(-0.02 * time);
        //col = toString(1, 1, 0, 0.25*time);
        //cell[2].style.backgroundColor = col;
        //cell[2].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", time);
    }
}

Customize();
//document.getElementById("tabShaders").setAttribute("onClick", "javascript: Customize();");
