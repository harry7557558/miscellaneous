// https://github.com/DMOJ/online-judge/blob/master/judge/comments.py#L47
$(document).ready(function() {
    document.getElementById("new-comment").remove();
});

// show problem type on problem page
$(document).ready(function() {
    if (document.URL.match("problem/")) {
        document.getElementById("problem-types").childNodes[1].click();
    }
});

// get the username on the current page
function getUsername() {
    var url = window.location.href
      , username = "";
    if (url.match("https://dmoj.ca/user/"))
        username = url.substring(21, url.length);
    if (url.match("https://dmoj.ca/submissions/user/"))
        username = url.substring(33, url.length);
    if (username.length == 0)
        username = document.getElementById("user-links").getElementsByTagName("b")[0].innerText;
    if (username.match("\/"))
        username = username.substring(0, username.search("\/"));
    return username;
}

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

// customize problem solved page
$(function() {
    if (document.URL.match("dmoj.ca/user/" && document.URL.match("/solved"))) {
        // load all problems
        var username = getUsername();
        var request = new XMLHttpRequest();
        request.open("GET", "https://dmoj.ca/user/" + username + "/solved/ajax?start=0&end=100", false);
        request.send();
        var str = request.responseText;
        str = str.replace('{"results": "', '').replace('", "has_more": false}', '');
        eval("document.getElementById('submissions-table').innerHTML = \"" + str + "\"");
        var ele = document.getElementById("pp-load-link-wrapper");
        if (ele != null)
            ele.remove();
        return;
        // expand all solved problems
        var ss = document.getElementsByClassName("user-problem-group");
        for (var i = 0; i < ss.length; i++) {
            ss[i].getElementsByClassName("toggle")[0].click();
        }
    }
});

// DMOJ Point Calculator
// Press F1 to calculate the points your earned points after solving certain problem(s)
// Press F2 to generate a table
$(function() {

    var pointcalc_pnts, pointcalc_ac, solved_problem_list = [];
    var getPointData = function(username) {
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
                    if (ac) {
                        solved_problem_list.push(prob);
                        AC++;
                    }
                    prob = Subs[i][0],
                    pp = Subs[i][1],
                    ac = Subs[i][2];
                }
            }
            Points.push(pp),
            AC += Number(ac);
            pointcalc_pnts = Points;
            pointcalc_ac = AC;
        }
        request.send();
        console.log("getPointData('" + username + "');");
        return true;
    };
    $(document).ready(getPointData(getUsername()));

    document.body.onkeydown = function(event) {

        var calcPoint = function(added=[]) {
            // DMOJ Point System: https://dmoj.ca/post/103-point-system-rework
            var Points = pointcalc_pnts;
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
            var AC = pointcalc_ac;
            var B = 150 * (1.0 - Math.pow(0.997, AC + added.length));
            return P + B;
        };

        if (event.keyCode == 112) {
            // F1: point calculator
            event.preventDefault();
            var oldpoint = calcPoint();
            if (oldpoint == 0.0 || 0.0 * oldpoint != 0.0) {
                alert("ERROR: Please restart this script");
                getPointData(getUsername());
                return;
            }
            var app = prompt("User " + getUsername() + "\nEnter comma-separated problem weight:", "10");
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
        } else if (event.keyCode == 113) {
            // Output a table and an svg graph
            const pc = [1, 3, 4, 5, 6, 7, 8, 10, 12, 15, 17, 20, 25, 30, 35, 40, 50];
            var p0 = calcPoint()
              , p1 = [];
            var s = "User " + getUsername() + '\n';
            s += "Problem $     Earned $        Problem $     Earned $        \n";
            var svg = "M0," + (calcPoint([0]) - p0).toFixed(2);
            for (var i = 0; i < pc.length; i++) {
                p1.push(calcPoint([pc[i]]) - p0);
                svg += "L" + pc[i] + "," + p1[i].toFixed(2);
            }
            var ml = Math.ceil(pc.length / 2);
            for (var i = 0; i < ml; i++) {
                s += String(pc[i]).padEnd(14) + p1[i].toFixed(2).padEnd(16);
                if (ml + i < pc.length) {
                    s += String(pc[ml + i]).padEnd(14) + p1[ml + i].toFixed(2).padEnd(16) + '\n';
                }
            }
            alert(s);
            console.log(s);
            console.log('<path id="' + getUsername() + '" style="" transform="" d="' + svg + '" vector-effect="non-scaling-stroke"></path>');
        }

    }
    ;

});

// hack (potentially) malicious links
$(function() {
    var whitelist = ["javascript", "dmoj.ca", "github.com", ".github.io", ".wikipedia.org", "keybase.io", "codeforces.com", "wcipeg.com", ".uwaterloo.ca", ".algome.me"];
    var blacklist = ["youtube", "goo.gl", "bit.ly", "gg.gg", "vimeo", "mailto:", "docs.google.com", "olympiads.ca", "www.timeanddate.com"];
    var s = document.getElementsByTagName("a");
    for (var i = 0; i < s.length; i++) {
        var url = s[i].href;
        if (url == "" || url == "#")
            continue;
        var ok = false;
        for (var j = 0; j < whitelist.length; j++)
            if (url.match(whitelist[j]))
                ok = true;
        var bad = false;
        for (var j = 0; j < blacklist.length; j++)
            if (url.match(blacklist[j]))
                bad = true;
        //if (s[i].firstElementChild != null && s[i].firstElementChild.tagName == "IMG") ok = false;
        if (!ok && url[0] != '/') {
            s[i].style.color = bad ? "red" : "blue";
            s[i].style.fontWeight = 600;
            s[i].style.textDecoration = "underline";
            if (bad) {
                s[i].href = "javascript:alert('" + url + "')";
                console.log("Link blocked: " + url);
            } else {
                s[i].target = "_blank";
                console.log("Link suspected: " + url);
            }
        }
    }

    // highlight natural-looking links inside text
    s = document.getElementsByClassName("rate-none");
    for (var i = 0; i < s.length; i++) {
        s[i].style.textDecoration = "underline";
    }
});
