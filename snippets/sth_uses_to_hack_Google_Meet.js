// get all chat messages in a Google meet
// open Google meet sidebar, execute this script and copy HTML from debug console

"use strict";

(function() {
    // get chatbox element
    var matchedElements = [];
    var isMatch = function(ele) {
        var attr = ele.attributes;
        if (attr == undefined || !(attr.length > 0))
            return false;
        if (attr.hasOwnProperty('aria-live'))
            return true;
        return false;
    }
    function recur(ele) {
        var s = ele.childNodes;
        for (var i = 0; i < s.length; i++) {
            if (isMatch(s[i]))
                matchedElements.push(s[i]);
            else
                recur(s[i]);
        }
    }
    recur(document.body);
    if (!(matchedElements.length > 0))
        return;
    var chat = matchedElements[0].cloneNode(true);
    var messages = chat.childNodes;

    // get chat messages
    function escapeHTML(str) {
        var p = document.createElement("p");
        p.appendChild(document.createTextNode(str));
        return p.innerHTML.replace(/\n/g,'<br/>');
    }
    function getMessage(msg) {
        var nodes = msg.childNodes;
        var info = nodes[0].childNodes;
        var user = info[0].innerHTML;
        var time = info[1].innerHTML;
        var content = nodes[1].childNodes;
        var msgs = [];
        for (var i = 0; i < content.length; i++) {
            var c = content[i].childNodes;
            var s = "";
            for (var j = 0; j < c.length; j++) {
                // text: add text content
                if (c[j].nodeType == 3)
                    s += escapeHTML(c[j].textContent);
                // URL: add hyperlink
                if (c[j].nodeType == '1')
                    s += "<a href=\"" + c[j].innerHTML + "\" target='_blank'>" + c[j].innerHTML + "</a>";
            }
            msgs.push(s);
        }
        var s = "<div class='chat'><div class='info'>";
        s += "<div class='user'>" + user + "</div>";
        s += "<div class='time'>" + time + "</div>";
        s += "</div><div class='messages'>";
        for (var i = 0; i < msgs.length; i++)
            s += "<div class='text'>" + msgs[i] + "</div>";
        s += "</div></div>";
        return s;
    }
    var html = "";
    for (var i = 0; i < messages.length; i++)
        html += getMessage(messages[i]);

    // write html
    var before = "<!doctype html><html><head><title>" + document.title + " Chats</title></head>";
    before += "<body id='" + window.location.pathname.replace('/', '') + "'>";
    // modified Google's stylesheet
    before += "<style>.chat{display:block;padding:10px;font-family:'Roboto',arial,sans-serif;}.info{display:block;}.user{color:#202124;display:inline-block;font-size:13px;font-weight:500;line-height:19px;padding-right:8px;}.time{color:#5f6368;display:inline-block;font-size:12px;}.messages{display:inline-block;max-width:100%;}.text{color:#202124;font-size:13px;line-height:20px;padding-top:0;white-space:pre-wrap;}a{color:#3367d6;font-size:13px;text-decoration:underline;}</style>";
    var after = "</body></html>";
    console.log(before + html + after);
}
)();
