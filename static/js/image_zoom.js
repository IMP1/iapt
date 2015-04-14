var container = document.getElementById("image-container");
var img = document.getElementById("full-image");
var scaled = false;
img.onclick = function(e) {
    if (scaled) {
        container.style.overflow = "";
        container.style.maxHeight = "";
        img.style.cssText = "cursor: -moz-zoom-in; cursor: -webkit-zoom-in" 
        img.style.width = "100%";
    } else {
        var x = (e.pageX - container.offsetLeft) / img.offsetWidth;
        var y = (e.pageY - container.offsetTop)  / img.offsetHeight;
        container.style.overflow = "auto";
        container.style.maxHeight = "550px";
        img.style.cssText = "cursor: -moz-zoom-out; cursor: -webkit-zoom-out" 
        img.style.width = "" + img.naturalWidth + "px";
        container.scrollLeft = x * img.naturalWidth  - container.offsetWidth / 2;
        container.scrollTop  = y * img.naturalHeight - container.offsetHeight / 2;
    }
    scaled = !scaled;
}