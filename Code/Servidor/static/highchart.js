var svg;

var graph_data = [];
var myColor;
var x, y, xAxis, yAxis;
var domain_x = 0;
var line;
var mouseover, mousemove, mouseleave;

var chart;
var chart2;
var data_chart2 = [];

//  * Request data from the server, add it to the graph and set a timeout
//  * to request again
function requestData() {
    $.ajax({
        url: 'http://localhost:5000/get_graph_data',
        dataType:'json',
        success: function(datos) {
            // console.log(datos);
            // var insertado_punto = false;
            if(datos.length > 0)
            {
                for(var i = 0; i < datos[0].length; i++)
                {
                    x_step = datos[0][i];
                    y_lobo = datos[1][i][0];
                    y_conejo = datos[1][i][1];
                    
                    
                    y_lobo_teorico = datos[2][i][0];
                    y_conejo_teorico = datos[2][i][1];

                    // console.log(datos);
                    // x = datos[0];
                    // y_lobo = datos[1];
                    // y_conejo = datos[2];
                    if(!(x_step==0 && y_lobo==0 && y_conejo==0))
                    {
                        point_lobo = [x_step, y_lobo];
                        point_conejo = [x_step, y_conejo];
                        point_lobo_teorico = [x_step, y_lobo_teorico];
                        point_conejo_teorico = [x_step, y_conejo_teorico];
                        

                        ///////////// D3 js /////////////
                        // graph_data[0].values.push({step: x_step, value:y_lobo})
                        // graph_data[1].values.push({step: x_step, value:y_conejo})
    
    
                        // insertado_punto = true


                        // var series = chart.series[0],
                        //     shift = series.data.length > 20; // shift if the series is
                        //                                     // longer than 20
    
                        ////////////// HIGHCHARTS //////////////
                        // var series_lobos = chart.series[0];
                        // var series_conejos = chart.series[1];
                        //     shift = series.data.length > 20; // shift if the series is
                        //                                     // longer than 20
                        
                        // add the point
                        chart.series[0].addPoint(point_lobo, true);
                        chart.series[1].addPoint(point_conejo, true);
                        chart.series[2].addPoint(point_lobo_teorico, true);
                        chart.series[3].addPoint(point_conejo_teorico, true);
    
                        ////////////// DYGRAPH //////////////
                        // var data1 = [];
                        // var data2 = [];
                        // data1.push(y_lobo);
                        // data2.push(y_conejo);
                        // data = [data1, data2];
                        
                        // data_chart2.push([x_step, y_lobo, y_conejo]);
    
                        // data.push(point_conejo);
                        // chart2.updateOptions( { 'file': data_chart2 } )
                    }
                }
                // if (insertado_punto)
                // {
                //     console.log("hay datos");
                //     console.log(datos);
                //     redraw();
                // }
            }
            // call it again after one second
            setTimeout(requestData, 1000);
            },
        cache: false
    });
}

$(document).ready(function() {
    // chart2= new Dygraph(document.getElementById('fig03'),data_chart2,{
    //     drawPoints: true,
    //     showRoller: true,
    //     highlightCircleSize: 2,
    //     strokeWidth: 1,
    //     highlightSeriesOpts: {
    //         strokeWidth: 3,
    //         strokeBorderWidth: 1,
    //         highlightCircleSize: 5
    //       },
    //     labels:["Step","# lobos", "# conejos"],
    //     });
    // requestData();
    
    
    // var onclick = function(ev) 
    // {
    //     if (chart2.isSeriesLocked()) {
    //         chart2.clearSelection();
    //     } else {
    //         chart2.setSelection(chart2.getSelection(), chart2.getHighlightSeries(), true);
    //     }
    // };
    // chart2.updateOptions({clickCallback: onclick}, true);
    // chart2.setSelection(false, 's005');

    // chart = new Dygraph($("#data-container"), data);

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'fig02',
            events: {
                load: requestData,
            },
            type: "line",
            animation: false,
            zoomType: 'x',
            panning: {
                enabled: true
            },
            panKey: 'shift',
        },
        plotOptions: {
            series: {
                showCheckbox: true,
                selected: true,
                events: {
                    checkboxClick: function () {
                        this.setVisible(!this.visible);
                    },
                },
                // showInNavigator: true,
            }
        },
        title: {
            text: 'Live random data'
        },
        xAxis: {
            type: 'linear',
            allowDecimals: false,
            min: 0
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            itemStyle: {
                fontSize:'17px',
                // font: '20pt Trebuchet MS, Verdana, sans-serif',
                color: '#000'
             },
        //     //  itemCheckboxStyle: {
        //     //     cursor: "pointer",
        //     //     border: "1px solid #62737a",
        //     // },
        //     //  itemHoverStyle: {
        //     //     color: '#FFF'
        //     //  },
        //     //  itemHiddenStyle: {
        //     //     color: '#444'
        //     //  }
        },
        tooltip: {
            crosshairs: [true, true],
            shared: true
        },
        series: [
        {
            // marker: {
            //     enabled: true
            // },
            name: '# lobos',
            data: []
        },
        {
            // marker: {
            //     enabled: true
            // },
            name: '# conejos',
            data: []
        },
        {
            // marker: {
            //     enabled: true
            // },
            name: '# lobos teoricos',
            data: []
        },
        {
            // marker: {
            //     enabled: true
            // },
            name: '# conejos teoricos',
            data: []
        }]
    });
});
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// set the dimensions and margins of the graph
// var margin = {top: 10, right: 100, bottom: 30, left: 30},
// width = 460 - margin.left - margin.right,
// height = 400 - margin.top - margin.bottom;

// // append the svg object to the body of the page
// svg = d3.select("#data-container")
// .append("svg")
// .attr("width", width + margin.left + margin.right)
// .attr("height", height + margin.top + margin.bottom)
// .append("g")
// .attr("transform",
//     "translate(" + margin.left + "," + margin.top + ")");

// //Read the data
// // d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_connectedscatter.csv", function(data) {


// data = [{name:"Lobos", values:[]},{name:"Conejos", values:[]}];
// // console.log(data);
// // List of groups (here I have one group per column)
// // var allGroup = ["valueA", "valueB", "valueC"]
// var allGroup = ["Lobos", "Conejos"];

// // Reformat the data: we need an array of arrays of {x, y} tuples
// // var dataReady = allGroup.map( function(grpName) { // .map allows to do something for each element of the list
// // return {
// //     name: grpName,
// //     values: data.map(function(d) {
// //     return {time: d.time, value: +d[grpName]};
// //     })
// // };
// // });
// dataReady = data;

// console.log(dataReady);
// graph_data = dataReady;
// // I strongly advise to have a look to dataReady with
// // console.log(dataReady)

// // A color scale: one color for each group
// myColor = d3.scaleOrdinal()
// .domain(allGroup)
// .range(d3.schemeSet2);

// // Add X axis --> it is a date format
// domain_x = 10;

// x = d3.scaleLinear()
// .domain([0,domain_x])
// .range([ 0, width ]);
// svg.append("g")
// .attr("transform", "translate(0," + height + ")")
// .attr("class", "x axis")
// .call(d3.axisBottom(x));

// // Add Y axis
// y = d3.scaleLinear()
// .domain( [0,20])
// .range([ height, 0 ]);
// svg.append("g")
// .attr("class", "y axis")
// .call(d3.axisLeft(y));



// // Add the lines
// line = d3.line()
// .x(function(d) { return x(+d.step) })
// .y(function(d) { return y(+d.value) })
// svg.selectAll("myLines")
// .data(dataReady)
// .enter()
// .append("path")
//     .attr("class", function(d){ return d.name })
//     .attr("d", function(d){ return line(d.values) } )
//     .attr("stroke", function(d){ return myColor(d.name) })
//     .style("stroke-width", 4)
//     .style("fill", "none")

// // create a tooltip
// var Tooltip = d3.select("#data-container")
//     .append("div")
//     .style("opacity", 0)
//     .attr("class", "tooltip")
//     .style("background-color", "white")
//     .style("border", "solid")
//     .style("border-width", "2px")
//     .style("border-radius", "5px")
//     .style("padding", "5px")

// // Three function that change the tooltip when user hover / move / leave a cell
// mouseover = function(d) {
//     Tooltip
//     .style("opacity", 1)
// }
// mousemove = function(d) {
//     var height_offset = $('.jumbotron').outerHeight(true);
//     // console.log(height_offset);
//     // var width_offset = $('#data-container').offset().left;
//     // // console.log(width_offset);
//     // // console.log(d3.mouse(this));
//     // console.log("width_offset: "+width_offset+"tooltip-left: " + String(d3.mouse(this)[0]+width_offset));
//     // console.log("debería ser: " + d3.mouse(this)[0] + "px");

//     // console.log(d3.event.pageX - document.getElementById("data-container").getBoundingClientRect().x + 10);
//     // console.log(d3.event.pageX);
//     // console.log("Ahora estoy poniendo un offset de: " + String(d3.mouse(this)[0]+110));
//     var left = d3.event.pageX;

//     Tooltip
//     .html("Exact value: " + d.value)
//     .style("left", left + 10 + "px")
//     .style("top", d3.mouse(this)[1]+height_offset + "px")
// }
// mouseleave = function(d) {
//     Tooltip
//     .style("opacity", 0)
// }

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Add the points
// svg
// // First we need to enter in a group
// .selectAll("myDots")
// .data(dataReady)
// .enter()
//     .append('g')
//     .style("fill", function(d){ return myColor(d.name) })
//     .attr("class", function(d){ return d.name })
// // Second we need to enter in the 'values' part of this group
// .selectAll("myPoints")
// .data(function(d){ return d.values })
// .enter()
// .append("circle")
//     .attr("cx", function(d) { return x(d.time) } )
//     .attr("cy", function(d) { return y(d.value) } )
//     .attr("r", 5)
//     .attr("stroke", "white")
//     .attr("class", "point")
// .on("mouseover", mouseover)
// .on("mousemove", mousemove)
// .on("mouseleave", mouseleave)

// Add a legend at the end of each line
// svg
// .selectAll("myLabels")
// .data(dataReady)
// .enter()
//     .append('g')
//     .append("text")
//         .attr("class", function(d){ return d.name })
//         .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; }) // keep only the last value of each time series
//         .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.value) + ")"; }) // Put the text at the position of the last point
//         .attr("x", 12) // shift the text a bit more right
//         .text(function(d) { return d.name; })
//         .style("fill", function(d){ return myColor(d.name) })
//         .style("font-size", 15)



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Add a legend (interactive)
// svg
// .selectAll("myLegend")
// .data(dataReady)
// .enter()
// .append('g')
// .append("text")
//     .attr('x', function(d,i){ return 30 + i*60})
//     .attr('y', 30)
//     .text(function(d) { return d.name; })
//     .style("fill", function(d){ return myColor(d.name) })
//     .style("font-size", 15)
// .on("click", function(d){
//     // is the element currently visible ?
//     currentOpacity = d3.selectAll("." + d.name).style("opacity")
//     // Change the opacity: from 0 to 1 or from 1 to 0
//     d3.selectAll("." + d.name).transition().style("opacity", currentOpacity == 1 ? 0:1)
// })
// });
// // })

// function redraw()
// {
//     var lastStep = graph_data[0].values[graph_data[0].values.length -1 ].step;
//     x.domain([0,lastStep]);


//     var max_value = d3.max(graph_data, function(d)
//                     {
//                         return d3.max(d.values, function(e)
//                         {
//                             return e.value;
//                         })
//                     })

    
//     y.domain([0,max_value+max_value*0.5]);

//     svg.selectAll("g.x.axis")
//     .call(d3.axisBottom(x));

//     svg.selectAll("g.y.axis")
//     .call(d3.axisLeft(y));

//     // svg.selectAll("g.y.axis")
//     // .call(yAxis);

//     // svg.selectAll("g.x.axis")
//     // .call(xAxis);

//     svg.selectAll("myLines")
//     .data(dataReady)
//     .enter()
//     .append("path")
//     .attr("class", function(d){ return d.name })
//     .attr("d", function(d){ return line(d.values) } )
//     .attr("stroke", function(d){ return myColor(d.name) })
//     .style("stroke-width", 4)
//     .style("fill", "none")

//     svg
//     // First we need to enter in a group
//     .selectAll("myDots")
//     .data(graph_data)
//     .enter()
//     .append('g')
//         .style("fill", function(d){ return myColor(d.name) })
//         .attr("class", function(d){ return d.name })
//         // Second we need to enter in the 'values' part of this group
//         .selectAll("myPoints")
//         .data(function(d){ return d.values })
//         .enter()
//         .append("circle")
//         .attr("cx", function(d) { return x(d.step) } )
//         .attr("cy", function(d) { return y(d.value) } )
//         .attr("r", 5)
//         .attr("stroke", "white")
//         .attr("class", "point")
//         .on("mouseover", mouseover)
//         .on("mousemove", mousemove)
//         .on("mouseleave", mouseleave)

// }

// function add_data()
// {
    
    
    
//     // graph_data[0].values.push({time: 4, value: 11});
//     // graph_data[0].values.push({time: 11, value: 5});
//     // console.log(graph_data);
//     requestData();
//     // redraw();
// }
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////