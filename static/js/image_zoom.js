var container = document.getElementById("image-container");
var img = document.getElementById("full-image");
var scaled = false;
img.onclick = function(e) {
    if (scaled) {
        container.style.overflow = "";
        img.style.cssText = "cursor: -moz-zoom-in; cursor: -webkit-zoom-in" 
        img.style.width = "100%";
    } else {
        container.style.overflow = "scroll";
        var x = (e.clientX - img.offsetLeft) / img.offsetWidth;
        var y = (e.clientY - img.offsetTop) / img.offsetHeight;
        container.scrollLeft = x * img.naturalWidth  - container.offsetWidth / 2;
        container.scrollTop  = y * img.naturalHeight - container.offsetHeight / 2;
        img.style.cssText = "cursor: -moz-zoom-out; cursor: -webkit-zoom-out" 
        img.style.width = "" + img.naturalWidth + "px";
    }
    scaled = !scaled;
}