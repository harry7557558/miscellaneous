// go to https://www.shadertoy.com/slideshow?playlist=[PLAYLIST_ID]
// and run this script

function loadShaders(gShaderIDs) {
    var httpReq = new XMLHttpRequest();
    httpReq.addEventListener('load', function(event) {
        var jsnShader = event.target.response;
        if (jsnShader === null || typeof(jsnShader) != "object" || jsnShader.length === 0) {
            console.log("Failed to load shaders.");
            return;
        }
        console.log(JSON.stringify(jsnShader));
    }, false);
    httpReq.addEventListener('error', function() {
        console.log("Error loading shaders.");
    }, false);

    httpReq.open("POST", "/shadertoy", true);
    httpReq.responseType = "json";
    httpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    var str = "{ \"shaders\": " + JSON.stringify(gShaderIDs) + " }";
    str = "s=" + encodeURIComponent(str) + "&nt=1&nl=1&np=1";
    httpReq.send(str);
}

var shaders = gShaderIDs;
loadShaders(shaders);
