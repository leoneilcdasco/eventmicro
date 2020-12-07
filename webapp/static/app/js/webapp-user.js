$(function () {
    "use strict";
    // ============================================================== 
    // Registration Chart
    // ============================================================== 
    var chart2 = new Chartist.Bar('.amp-pxl', {
          labels: x_series,
          series: [
                    y1_series
                ] 
        }, {
          axisX: {
            // On the x-axis start means top and end means bottom
            position: 'end',
            showGrid: false
          },
          axisY: {
            // On the y-axis start means left and end means right
            position: 'start'
          },
        low: '0',
        plugins: [
            Chartist.plugins.tooltip()
        ]
    });

    $('#registeredchart').sparkline( m1_series, {
        type: 'bar',
        height: '35',
        barWidth: '4',
        resize: true,
        barSpacing: '4',
        barColor: '#1e88e5'
    });

    $('#attendeeschart').sparkline( m2_series, {
        type: 'bar',
        height: '35',
        barWidth: '4',
        resize: true,
        barSpacing: '4',
        barColor: '#7460ee'
    });
});

$(document).ready( function() {
    $(".user-table tfoot th").each(function () {
        var title = $(this).text();
        $(this).html(
        '<input type="text" class="form-control" placeholder="Search ' +
            title +
            '" />'
        );
    });

    // DataTable
    var tableSearching = $(".user-table").DataTable({
        "iDisplayLength": 50
    });

    // Apply the search
    tableSearching.columns().every(function () {
    var that = this;

    $("input", this.footer()).on("keyup change", function () {
        if (that.search() !== this.value) {
        that.search(this.value).draw();
        }
    });
    });
})