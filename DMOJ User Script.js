$(function() {

    // Customize user table
    // Addd a scale to Points and Problems in user table,
    // and add an Average Point Per Problem column.

    $(function() {
        var table = document.getElementById("users-table");
        if (table == null)
            return;

        // calculate scale upper bound
        var maxpnt = 0
          , maxprb = 0
          , maxppp = 0;
        if (table.rows[0].cells.length > 6)
            return;
        for (var i = 0; i < table.rows.length; i++) {
            if (table.rows[i].cells.length < 6)
                table.rows[i].insertCell(table.rows[i].cells.length);
            var k = table.rows[i].cells;
            if (i == 0) {
                k[3].style.minWidth = k[4].style.minWidth = k[5].style.minWidth = "80px";
                k[5].outerHTML = k[5].outerHTML.replace(/td/g, "th");
                k[5].innerText = "APPP";
                k[5].title = "Average Point Per Problem";
            } else {
                var points = Number(k[3].title);
                var problems = Number(k[4].innerText);
                var ratio = points / problems;
                if (isNaN(ratio)) {
                    k[5].innerText = "#";
                } else {
                    k[5].innerText = ratio.toFixed(2);
                    k[5].title = ratio.toFixed(3);
                    maxpnt = Math.max(maxpnt, points);
                    maxprb = Math.max(maxprb, problems);
                    maxppp = Math.max(maxppp, ratio * (1 - Math.exp(0.1 * (1 - problems))));
                }
            }
        }

        // set table element style
        var toString = function(r, g, b, a) {
            return "rgba(" + Math.floor(255 * r) + "," + Math.floor(255 * g) + "," + Math.floor(255 * b) + "," + a + ")";
        }
          , gradientToString = function(c1, c2) {
            return "linear-gradient(to right, " + c1 + ", " + c2 + ")";
        }
          , stepToString = function(c1, c2, a) {
            var al = " " + 100 * a + "%, ";
            return "repeating-linear-gradient(to right, " + c1 + "," + c1 + al + c2 + al + c2 + "100%)";
        };
        for (var i = 1; i < table.rows.length; i++) {
            var k = table.rows[i].cells;
            var points = Number(k[3].title);
            var problems = Number(k[4].innerText);
            var ratio = points / problems;

            col = toString(1, 0.2, 0.2, 1.0 - Math.exp(-0.001 * points));
            k[3].style.backgroundColor = col;
            k[3].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", points / maxpnt);

            col = toString(0.2, 1, 0.2, 1.0 - Math.exp(-0.001 * problems));
            k[4].style.backgroundColor = col;
            k[4].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", problems / maxprb);

            col = toString(0.2, 0.2, 1, 1.0 - Math.exp(-0.08 * ratio));
            k[5].style.backgroundColor = col;
            k[5].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", ratio / maxppp);
        }
    });

    // DMOJ Point Calculator
    // Press F1 to calculate the points your earned points after solving certain problem(s)

    document.body.onkeydown = function(event) {

        var getUsername = function() {
            var url = window.location.href
              , username = "";
            if (url.match("https://dmoj.ca/user/"))
                username = url.substring(21, url.length);
            if (username.length == 0)
                username = document.getElementById("user-links").getElementsByTagName("b")[0].innerText;
            if (username.match("\/"))
                username = username.substring(0, username.search("\/"));
            return username;
        }
        var username = getUsername();

        var getPointData = function(username) {
            if (document.getElementById("pointcalc") == null) {
                document.body.innerHTML += "<div id='pointcalc' style='display:none'><div id='pointcalc-pnts'></div><div id='pointcalc-ac'></div></div>";
                var request = new XMLHttpRequest();
                request.open("GET", "https://dmoj.ca/api/user/submissions/" + username);
                request.onload = function() {
                    var data = JSON.parse(this.response);
                    var dat = request.responseText.replace(/[\{\}]/g, '').split(", ");
                    var Subs = [];
                    for (var i = 0; i < dat.length; i += 7) {
                        // problem, time, memory, points, language, status, result
                        var s = dat[i];
                        s = s.substring(s.search('"problem": "') + 12, s.length - 1);
                        var p = Number(dat[i + 3].substring(10, dat[i + 3].length));
                        if (p > 0) {
                            var res = dat[i + 6].substring(11, dat[i + 6].length - 1);
                            Subs.push([s, p, res == 'AC']);
                        }
                    }
                    Subs.sort();
                    var AC = 0;
                    var Points = [];
                    var prob = Subs[0][0]
                      , pp = Subs[0][1]
                      , ac = Subs[0][2];
                    for (var i = 1; i < Subs.length; i++) {
                        if (Subs[i][0] == prob) {
                            pp = Math.max(pp, Subs[i][1]);
                            ac |= Subs[i][2];
                        } else {
                            Points.push(pp);
                            AC += Number(ac);
                            prob = Subs[i][0],
                            pp = Subs[i][1],
                            ac = Subs[i][2];
                        }
                    }
                    Points.push(pp),
                    AC += Number(ac);
                    document.getElementById("pointcalc-pnts").innerHTML = Points;
                    document.getElementById("pointcalc-ac").innerHTML = AC;
                }
                request.send();
                return true;
            }
            return false;
        };

        var calcPoint = function(added=[]) {
            // DMOJ Point System: https://dmoj.ca/post/103-point-system-rework
            var Points = document.getElementById("pointcalc-pnts").innerText.split(',');
            Points = Points.concat(added);
            Points.sort(function(a, b) {
                return b - a;
            });
            var P = 0;
            for (var i = 0, w = 1.0; i < Points.length; i++) {
                P += w * Number(Points[i]);
                w *= 0.95;
                if (i == 99)
                    break;
            }
            var AC = document.getElementById("pointcalc-ac").innerHTML;
            var B = 150 * (1.0 - Math.pow(0.997, Number(AC) + added.length));
            return P + B;
        };

        var pointCalculator = function() {
            var oldpoint = calcPoint();
            if (oldpoint == 0.0 || 0.0 * oldpoint != 0.0) {
                alert("ERROR: Please restart this script");
                return;
            }
            var app = prompt("User " + username + "\nEnter comma-separated problem weight:", "10");
            if (app == null || app == "")
                return;
            app = app.replace(/ /g, "").split(",");
            for (var i = 0; i < app.length; i++) {
                if (isNaN(app[i] = Number(app[i]))) {
                    alert("ERROR: Invalid Input");
                    return;
                }
            }
            var newpoint = calcPoint(app);
            var dif = newpoint - oldpoint;
            alert("Current Point: " + oldpoint.toFixed(2) + "\nAfter Solving: " + newpoint.toFixed(2) + "\nPoint Earned: " + dif.toFixed(2));
        };

        if (event.keyCode == 112) {
            event.preventDefault();
            setTimeout(pointCalculator, getPointData(username) ? 500 : 0);
        }

    }
    ;

});
