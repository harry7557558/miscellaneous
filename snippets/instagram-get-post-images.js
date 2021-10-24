"use strict";

// pause the current thread
function sleep(ms) {
    return new Promise((resolve)=>{
        setTimeout(resolve, ms);
    }
    );
}

// for https://www.instagram.com/p/[ID]/
async function getPostImages() {

    // go to the previous/next image in the post
    // return false of button not found
    function previousImage(post) {
        var button = post.getElementsByClassName("POSa_");
        if (button.length == 0)
            return false;
        if (button.length != 1)
            throw "Error: Multiple previous buttons found";
        button[0].click();
        return true;
    }
    function nextImage(post) {
        var button = post.getElementsByClassName("_6CZji");
        if (button.length == 0)
            return false;
        if (button.length != 1)
            throw "Error: Multiple next buttons found";
        button[0].click();
        return true;
    }

    // add an url to a list, take no action if url is already in the list
    function addUrlToList(list, url) {
        if (url == "")
            return false;
        for (var i = 0; i < list.length; i++) {
            if (url == list[i])
                return false;
        }
        list.push(url);
        return true;
    }

    // add all available images in the page
    function addAllImages(post, list) {
        var images = post.getElementsByClassName("FFVAD");
        for (var i = 0; i < images.length; i++) {
            if (images[i].tagName.toLocaleLowerCase() != "img")
                throw "Error: Image object tag name is not img";
            var src = images[i].src;
            addUrlToList(list, src);
        }
        if (images.length == 0) {
            console.warn("Warning: No image found.", "Make sure the post contains images instead of videos.");
        }
    }

    // get post
    var container = document.getElementsByClassName("ltEKP");
    if (container.length == 0)
        container = document.getElementsByClassName("PdwC2 fXiEu");
    if (container.length == 0)
        throw "Error: No post found.";
    if (container.length > 1)
        throw "Error: Multiple posts found.";
    var post = container[0];

    // go to the first image
    while (previousImage(post))
        ;

    // adding images
    var urls = [];
    do {
        await sleep(1000);
        addAllImages(post, urls);
    } while (nextImage(post));

    console.log(urls.length + " image URLs found.\n" + urls.join("\n"));
}

getPostImages();
