// DMOJ Point Calculator
// run as browser snippet on DMOJ website user page

document.body.onkeydown = function(event) {

    var getUsername = function() {
        var url = window.location.href, username = "";
        if (url.match("https://dmoj.ca/user")) username = url.substring(21, url.length);
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
        var app = prompt("User " + username + "\nEnter comma-separated added points", "10");
        if (app == null || app == "")
            return;
        app = app.replace(/ /g, "").split(",");
        for (var i = 0; i < app.length; i++) {
            if (isNaN(app[i] = Number(app[i]))) {
                alert("ERROR: Invalid Input");
                return;
            }
        }
        var oldpoint = calcPoint();
        if (oldpoint == 0.0 || 0.0 * oldpoint != 0.0) {
            alert("ERROR: Please restart this script");
            return;
        }
        var newpoint = calcPoint(app);
        var dif = newpoint - oldpoint;
        alert("Current Point: " + oldpoint.toFixed(2) + "\nAfter Adding: " + newpoint.toFixed(2) + "\nAdded Point: " + dif.toFixed(2));
    };

    if (event.keyCode == 112) {
        event.preventDefault();
        setTimeout(pointCalculator, getPointData(username) ? 500 : 0);
    }

}
;
