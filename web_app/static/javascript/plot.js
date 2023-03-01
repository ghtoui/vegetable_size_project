function plotGraph() {
    var plotdata = document.getElementById('plot_img');

    $.get("/check_vegetable_growth", function(data) {
        plotdata.src = "data:image/png;base64, " + data;
    });
};
$(document).ready(function() {
    plotGraph();
});