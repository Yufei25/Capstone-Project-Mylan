$(document).ready(function () {
    var height = $(window).innerHeight();
    var nav_height = $("#navBar").outerHeight();
    console.log(height);
    console.log(nav_height);
    $(".general-background").css("height",height- nav_height -30);
});

