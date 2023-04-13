var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: 'http://localhost:5000/get_graph_data',
        success: function(datos) {
            for(var i = 0; i < datos[0].length; i++)
            {
                x_step = datos[0][i];
                y_lobo = datos[1][i][0];
                y_conejo = datos[1][i][1];
            
                // console.log(datos);
                // x = datos[0];
                // y_lobo = datos[1];
                // y_conejo = datos[2];
                if(!(x_step==0 && y_lobo==0 && y_conejo==0))
                {
                    point_lobo = [x_step, y_lobo];
                    point_conejo = [x_step, y_conejo];
                    
                    // var series = chart.series[0],
                    //     shift = series.data.length > 20; // shift if the series is
                    //                                     // longer than 20
                    
                    // add the point
                    chart.series[0].addPoint(point_lobo, true);
                    chart.series[1].addPoint(point_conejo, true);
                }
            }

            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            },
            resetZoomButton: {
              position: {
                  align: 'left'
                }
            }
        },
        title: {
            text: 'Live random data'
        },
        xAxis: {
            type: 'linear',
            allowDecimals: false,
            min: 0,
            tickPixelInterval: 1
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: '# lobos',
            data: []
        },
        {
            name: '# conejos',
            data: []
        }]
    });
});