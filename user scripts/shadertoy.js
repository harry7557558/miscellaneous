function customizeTable() {
    const max = Math.max
      , min = Math.min;
    var toString = function(r, g, b, a) {
        return "rgba(" + Math.floor(255 * r) + "," + Math.floor(255 * g) + "," + Math.floor(255 * b) + "," + a + ")";
    }
      , gradientToString = function(c1, c2) {
        return "linear-gradient(to right, " + c1 + ", " + c2 + ")";
    }
      , stepToString = function(c1, c2, a) {
        // repeating-linear-gradient(#74ABDD, #74ABDD 49.9%, #498DCB 50.1%, #498DCB 100%)
        var al = " " + 100 * a + "%, ";
        return "repeating-linear-gradient(to right, " + c1 + "," + c1 + al + c2 + al + c2 + "100%)";
    }
      , getTime = function(s) {
        var y = Number(s.substr(0, 4)) - 2000;
        var m = Number(s.substr(5, 2)) - 1;
        var d = Number(s.substr(8, 2)) - 1;
        return 365 * y + 30 * m + d;
        // Er...
    };

    //openTab('Shaders');
    //refreshShadersTable();

    var allshaders = document.getElementById("divShadersTable");
    var shaders = allshaders.getElementsByTagName("tr");
    var n = shaders.length;

    // get shader data
    var cells = [shaders[0].getElementsByTagName("td")], cell;
    var url = [""]
      , name = [""]
      , status = [""]
      , date = [NaN]
      , views = [NaN]
      , likes = [NaN]
      , comments = [NaN]
      , ratio = [0];
    var totViews = 0
      , totLikes = 0
      , totComments = 0
      , totViewsPub = 0
      , totLikesPub = 0;
    var minDate = 1e+8
      , maxDate = 0
      , maxViews = 0
      , maxLikes = 0
      , maxComments = 0
      , maxRatio = 0;
    for (var i = 1; i < n; i++) {
        cell = shaders[i].getElementsByTagName("td");
        cells.push(cell);
        url.push(cell[0].getElementsByTagName("a")[0].href);
        name.push(cell[2].innerText);
        status.push(cell[7].innerText);
        // date
        date.push(getTime(cell[3].innerText));
        maxDate = max(date[i], maxDate),
        minDate = min(date[i], minDate);
        // views
        views.push(Number(cell[4].innerText));
        totViews += views[i];
        maxViews = max(views[i], maxViews);
        // likes
        likes.push(Number(cell[5].innerText));
        totLikes += likes[i];
        maxLikes = max(likes[i], maxLikes);
        // comments
        comments.push(Number(cell[6].innerText));
        totComments += comments[i];
        maxComments = max(comments[i], maxComments);
        // ratio of likes to views
        ratio.push(likes[i] / views[i]);
        if (isNaN(ratio[i]))
            ratio[i] = 0;
        maxRatio = max(ratio[i], maxRatio);
        if (status[i] == "public" || cell[6].style.color == "rgb(0, 160, 0)") {
            totViewsPub += views[i];
            totLikesPub += likes[i];
        }
    }

    shaders[0].style.height = "30px";
    cells[0][4].innerHTML = "Views <b style='color:#500;'>(" + totViews + ")</b>";
    cells[0][5].innerHTML = "Likes <b style='color:#030;'>(" + totLikes + ")</b>";
    cells[0][6].innerHTML = "Comments <b style='color:#005;'>(" + totComments + ")</b>";
    cells[0][7].innerHTML = "Status <b style='color:#530;'>(" + (100 * totLikesPub / totViewsPub).toFixed(2) + "%&hearts;)</b>";
    for (var i = 1; i < n; i++) {
        shaders[i].style.backgroundImage = "linear-gradient(white, aliceblue)";
        var cell = cells[i];
        // views, red
        col = toString(1, 0, 0, 1.0 - Math.exp(-0.005 * views[i]));
        cell[4].style.backgroundColor = col;
        cell[4].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", views[i] / max(100, 50 * Math.ceil((maxViews + 1) / 50)));
        // likes, green
        col = toString(0, 1, 0, 1.0 - Math.exp(-0.05 * likes[i]));
        cell[5].style.backgroundColor = col;
        cell[5].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", likes[i] / max(10, 5 * Math.ceil((maxLikes + 1) / 5)));
        // comments, blue
        col = toString(0, 0, 1, 1.0 - Math.exp(-0.05 * comments[i]));
        cell[6].style.backgroundColor = col;
        cell[6].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", comments[i] / max(5, maxComments + 1));
        // status, yellow
        col = toString(1, 0.6, 0, 1.0 - Math.exp(-5.0 * ratio[i]));
        cell[7].style.backgroundColor = col;
        cell[7].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", ratio[i] / 0.3);
        var str = (100 * ratio[i]).toFixed(2) + "% like";
        if (str.length < 11)
            str = "0" + str;
        cell[7].innerText = str;
    }
}

setTimeout(customizeTable, 1000);

window.addEventListener("keydown", function(event) {
    if (event.keyCode == 112) {
        event.preventDefault();
        customizeTable();
    }
});
