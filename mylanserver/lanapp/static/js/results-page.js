// When the user scrolls the page, execute myFunction
window.onscroll = function () {
    myFunction()
};

function clearBox() {
    document.getElementById("dropdownbox").innerHTML = "";
    // document.getElementById("navigationBar").innerHTML = "";
    document.getElementById("export-icon").innerHTML = "";
    document.getElementById("dropdownboxone").innerHTML = "";
    window.print()
}

function myFunction() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("myBar").style.width = scrolled + "%";
}

