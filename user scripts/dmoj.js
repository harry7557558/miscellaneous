/*
 * My (handle:[secret]) DMOJ user script
 * You are free to use it with or without the author's knowledge
 * If you are a developer of DMOJ, you are free to implement/improve a feature that has already been implemented here
 
 * One note:
 * If you just want to copy-paste all of the following,
 * you may Google "Javascript minifier"
 
 * Enjoy ~~
 
*/

"use strict";

// so you can fix when something goes wrong
if (document.URL.match('/edit/profile') && document.URL.match('#')) {
    throw new Error("User script aborted.");
}

// hmmm...
$(function() {
    if (document.URL.match('/edit/profile')) {
        document.getElementById('id_about').oninput = function() {
            // this shows a pop-up when you click "update profile"
            // if you cancel it, that button will stop working
            // may be fixed by making that button invisible and use a controllable one instead
            window.onbeforeunload = function(e) {
                return e;
            }
        }
    }
});

// small UI modifications

// being quiet is good
$(function() {
    var s = document.getElementById("new-comment");
    if (s != null)
        s.remove();
});

// automatically expand problem type on problem pages
$(function() {
    var s = document.getElementById("problem-types");
    if (s != null) {
        s.childNodes[1].click();
        console.log(s.innerText.replace('\n', ': '));
    }
});

// add a "view raw source" button on submission pages
$(function() {
    if (document.URL.match("submission/")) {
        var s = document.getElementById("content-body");
        if (s != null) {
            var raw = document.createElement('div');
            raw.innerHTML = s.children[1].innerHTML;
            var a = raw.getElementsByTagName('a')[0];
            a.href += '/raw';
            a.innerText = 'View raw source';
            s.insertBefore(raw, s.children[2]);
            console.log("Raw source: " + a.href);
        }
    }
});

// making links look different from normal text
$(function() {
    var s = document.getElementsByClassName("rate-none");
    for (var i = 0; i < s.length; i++) {
        s[i].style.textDecoration = "underline";
    }
});

// show hidden comments, use at own risk
$(function() {
    var bc = document.getElementsByClassName("bad-comment");
    var count = 0;
    for (var i = 0; i < bc.length; i++) {
        var id = bc[i].getElementsByClassName('comment-link')[0].hash.replace(/[^0-9]/g, '');
        comment_show_content(Number(id));
        count++;
    }
    if (count != 0)
        console.log(count + " comment(s) unhid.");
    $(".bad-comment").css({
        opacity: "0.5",
        color: "#555"
    });
    // prevents unintentionally clicking user profile photo link
    // may not work in some browsers
    $(".gravatar-main").css({
        height: 'min-content'
    });
});

// https://github.com/DMOJ/online-judge/commit/396df0ebfeadcc3e20da9167d69c8c9d1d15fd63#commitcomment-41962688
$(function() {
    $(".contest-sort-link").css({
        color: 'white'
    });
});

// refer an user on contest ranking page when clicking a contest link on the rating history chart of a user's profile
$(function() {
    // the chart on users' profiles is an HTML5 canvas (seems to be rendered with a third-party tool)
    // change the URL hash on contest rating page instead
    if (document.URL.match('/contest') && document.URL.match('/ranking')) {
        var s = document.referrer;
        var d = s.indexOf('/user/');
        if (d != -1) {
            s = s.substring(d + 6, s.length);
            console.log(s);
            window.location.hash = '!' + s;
            console.log("Refer user " + s);
        }
    }
    // on profile pages: a small English language bug
    var s = document.getElementsByClassName('user-sidebar')[0];
    if (s != null) {
        s.innerHTML = s.innerHTML.replace("1 contests written", "1 contest written");
    }
});

// point/ranking related

// a sketchy function that returns the user handle on the current page
function getUsername() {
    var path = window.location.pathname;
    var paths = path.split('/').filter(value=>value !== '');
    var d = paths.indexOf('user');
    if (d != -1 && d + 1 < paths.length)
        return paths[d + 1];
    d = paths.indexOf('submissions');
    if (d != -1 && d + 1 < paths.length)
        return paths[d + 1];
    return document.getElementById("user-links").getElementsByTagName("b")[0].innerText;
}
// debug
$(function() {
    console.warn(getUsername());
});

// User table tools
// Add a graphics scale to Points and Problems in user lists/tables,
// and add an Average Point Per Problem (APPP) column.
$(function() {
    // there are 2 user tables on DMOJ: leaderboard and organization user list
    // columns: rank, rating, username, points, problems, [APPP]
    var table = document.getElementById("users-table");
    if (table == null)
        return;
    var trs = table.rows;
    if (trs[0].cells.length > 6)
        return;

    // modify stuffs + calculate scale upper bounds
    var maxpnt = 0
      , maxprb = 0
      , maxppp = 0;
    for (var i = 0; i < trs.length; i++) {
        if (trs[i].cells.length < 6)
            trs[i].insertCell(trs[i].cells.length);
        var k = trs[i].cells;
        if (i == 0) {
            k[3].style.minWidth = k[4].style.minWidth = k[5].style.minWidth = "80px";
            k[5].outerHTML = k[5].outerHTML.replace("td", "th");
            k[5].innerHTML = "Average";
            k[5].title = "Average point earned for each problem solved";
        } else {
            var points = Number(k[3].title);
            var problems = Number(k[4].textContent);
            var ratio = points / problems;
            if (isNaN(ratio)) {
                k[5].innerHTML = "#";
            } else {
                k[5].innerHTML = ratio.toFixed(2);
                k[5].title = ratio.toFixed(3);
                maxpnt = Math.max(maxpnt, points);
                maxprb = Math.max(maxprb, problems);
                maxppp = Math.max(maxppp, ratio * (1 - Math.exp(0.1 * (1 - problems))));
            }
        }
    }

    // add the graphics scale to table cells
    function toString(r, g, b, a) {
        return "rgba(" + Math.floor(255 * r) + "," + Math.floor(255 * g) + "," + Math.floor(255 * b) + "," + a + ")";
    }
    function gradientToString(c1, c2) {
        return "linear-gradient(to right," + c1 + "," + c2 + ")";
    }
    function stepToString(c1, c2, a) {
        var al = 100 * a + "%,";
        return "repeating-linear-gradient(to right, " + c1 + "," + c1 + al + c2 + al + c2 + "100%)";
    }
    for (var i = 1; i < table.rows.length; i++) {
        var k = table.rows[i].cells;
        var points = Number(k[3].title);
        var problems = Number(k[4].textContent);
        var ratio = points / problems;
        // points column, red
        var col = toString(1, .2, .2, 1 - Math.exp(-.001 * points));
        k[3].style.backgroundColor = col;
        k[3].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", points / maxpnt);
        // problems column, green
        col = toString(.2, 1, .2, 1 - Math.exp(-.001 * problems));
        k[4].style.backgroundColor = col;
        k[4].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", problems / maxprb);
        // APPP column, blue
        col = toString(.2, .2, 1, 1 - Math.exp(-.08 * ratio));
        k[5].style.backgroundColor = col;
        k[5].style.backgroundImage = stepToString(col, "rgba(0,0,0,0)", ratio / maxppp);
    }

    // use Javascript sorting when database sorting is not available (eg. organization user list)
    if (trs[0].getElementsByTagName('a').length == 0) {
        // https://stackoverflow.com/a/19947532
        var s = table.tHead.getElementsByTagName('th');
        for (var i = 1; i < s.length; i++) {
            if (i != 2) {
                s[i].style.cursor = 'pointer';
            }
        }
        $('th').click(function() {
            var id = $(this).index();
            if (id == 0 || id == 2)
                return;
            var table = $(this).parents('table').eq(0);
            var rows = table.find('tr:gt(0)').toArray().sort(comparer(id));
            this.asc = this.asc == null ? false : !this.asc;
            if (!this.asc)
                rows = rows.reverse();
            for (var i = 0; i < rows.length; i++) {
                rows[i].firstElementChild.textContent = String(i + 1);
                table.append(rows[i]);
            }
            var s = table[0].tHead.getElementsByTagName('th');
            for (var i = 1; i < s.length; i++) {
                s[i].innerHTML = s[i].innerHTML.replace(/[▴▾]/, '').trim();
                if (i == id)
                    s[i].innerHTML += this.asc ? ' ▴' : ' ▾';
            }
        })
        function comparer(index) {
            return function(a, b) {
                var valA = getCellValue(a, index)
                  , valB = getCellValue(b, index)
                return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
            }
        }
        function getCellValue(row, index) {
            var ele = $(row).children('td').eq(index)[0];
            return ele.title ? ele.title : ele.innerText;
        }
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
            // F2: Output a table and an svg graph
            const pc = [1, 3, 4, 5, 6, 7, 8, 10, 12, 15, 17, 20, 25, 30, 35, 40, 50];
            var p0 = calcPoint()
              , p1 = [];
            var s = "User " + getUsername() + ' (' + p0.toFixed(2) + ')\n';
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

// modify links on the current page based on personal preference
// without explicit UI change
$(function() {
    function modifyLink(ele) {
        // potentially "malicious" domains (eg. rickrolling link)
        // and "unnecessary" links that are often clicked unintentionally
        var disablelist = ["youtube", "goo.gl", "bit.ly", "vimeo", "www.timeanddate.com", "www.facebook.com", "translate.dmoj.ca"];

        var message = [];
        var s = ele.getElementsByTagName("a");
        for (var i = 0; i < s.length; i++) {
            var proto = s[i].protocol;
            if (typeof (proto) != 'string' || proto.indexOf('http') != 0)
                continue;
            var domain = s[i].host;
            var url = s[i].href;
            // disable links with matched domain
            // or links with only image contents
            for (var j = 0; j < disablelist.length; j++) {
                var children = Array.from(s[i].childNodes).filter(function(e) {
                    return e.nodeType == 1 || (e.nodeType == 3 && e.textContent.trim() != '');
                });
                var imgLink = (children.length == 1 && String(children[0].tagName).toLocaleLowerCase() == 'img');
                if (domain.match(disablelist[j]) || (imgLink && !(domain.match("dmoj.ca")))) {
                    s[i].setAttribute("onclick", "return confirm('Are you sure you want to open this link?\\n" + url + "')");
                    message.push(url);
                    break;
                }
            }
            // optional: open all non-DMOJ links in new tab
            if (!(domain.match("dmoj.ca") || domain.match('.algome.me'))) {
                s[i].setAttribute("target", "_blank");
            }
        }
        if (message.length > 0)
            console.log("disabled links:\n" + message.join('\n'));
    }

    modifyLink(document);

    // link modification should be applies to comment history
    // not sure if this makes slower
    var comment_area = document.getElementById("comments");
    if (comment_area != null) {
        const observer = new MutationObserver(list=>{
            const evt = new CustomEvent('dom-changed',{
                detail: list
            });
            comment_area.dispatchEvent(evt)
        }
        );
        observer.observe(comment_area, {
            attributes: false,
            childList: true,
            subtree: true
        });
        comment_area.addEventListener("dom-changed", function() {
            modifyLink(comment_area);
        });
    }

});
