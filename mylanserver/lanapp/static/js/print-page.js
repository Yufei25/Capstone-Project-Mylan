
function clearBox() {
    $("#results-content").append('<input id="print-icon" type="image" src="/static/image/print-icon.png" alt="Print Document" onclick="printOut()"/> <br> <input id="close-icon" type="image" src="/static/image/close-icon.png" alt="Close Window" onclick="window.close()"/>');
    $("#dropdownbox").remove();
    $("#results-nav").remove();
    $("#navigationBar").remove();

    var results = $("#results-content");
    results.removeClass('col-lg-10');
    results.addClass('col-lg-12');

}

function printOut(){
    $("#close-icon").hide();
    $("#print-icon").hide();
    window.print();
    $("#close-icon").show();
    $("#print-icon").show();
}


$(document).ready(function () {
  clearBox();
});
