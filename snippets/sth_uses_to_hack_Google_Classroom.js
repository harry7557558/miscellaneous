// something uses to hack Google Classroom
// refresh the page before running this

(function() {
    var teachers = document.getElementsByClassName("ycbm1d");
    var students = document.getElementsByClassName("d6CWTd");

    console.log("There are " + teachers.length + " teacher(s) in this classroom.");
    var s = "They are: \n";
    for (var i = 0; i < teachers.length; i++) {
        var n = teachers[i].innerText;
        n = n.replace(/\t/g, "").replace(/\n/g, "");
        if (n.match("Remove"))
            n = n.substr(0, n.search("Remove"));
        if (n.match("Email"))
            n = n.substr(0, n.search("Email"));
        s += n;
        try {
            var t = teachers[i].getElementsByTagName("a")[0].getAttribute("aria-label");
            t = t.substring(6, t.length);
            s += " (" + t + ")";
        } catch (e) {}
        if (i != teachers.length - 1)
            s += ", \n";
    }
    console.log(s);

    var c = 0;
    var s = "They are: \n";
    for (var i = 0; i < students.length; i++) {
        var n = students[i].innerText;
        if (!n.match("(invited)")) {
            n = n.replace(/\t/g, "").replace(/\n/g, "");
            s += n;
            try {
                var t = students[i].getElementsByTagName("a")[0].getAttribute("aria-label");
                t = t.substring(6, t.length);
                s += " (" + t + ")";
            } catch (e) {}
            if (i != students.length - 1)
                s += ", \n";
            c++;
        }
    }
    console.log("There are " + c + " student(s) in this classroom. (excluding yourself)");
    console.log(s);

}
)();
