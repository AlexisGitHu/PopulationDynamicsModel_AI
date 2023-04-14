var chart;

var data = [];
/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
function requestData() {
                    point_lobo = [x_step, y_lobo];
                    point_conejo = [x_step, y_conejo];
                    
                    // var series = chart.series[0],
                    //     shift = series.data.length > 20; // shift if the series is
                    //                                     // longer than 20

                    ////////////// HIGHCHARTS //////////////
                    // var series_lobos = chart.series[0];
                    // var series_conejos = chart.series[1];
                    // //     shift = series.data.length > 20; // shift if the series is
                    // //                                     // longer than 20
                    
                    // // add the point
                    // chart.series[0].addPoint(point_lobo, true);
                    // chart.series[1].addPoint(point_conejo, true);

                    ////////////// DYGRAPH //////////////
                    // var data1 = [];
                    // var data2 = [];
                    // data1.push(y_lobo);
                    // data2.push(y_conejo);
                    // data = [data1, data2];
                    
                    data.push([x_step, y_lobo, y_conejo]);
                    
                    // add the point
                    chart.series[0].addPoint(point_lobo, true);
                    chart.series[1].addPoint(point_conejo, true);

                    // data.push(point_conejo);
                    chart.updateOptions( { 'file': data } )
                }
            }
**/
$(document).ready(function() {
//     chart= new Dygraph(document.getElementById('data-container'),data,{
//         drawPoints: true,
//         showRoller: true,
//         highlightCircleSize: 2,
//         strokeWidth: 1,
//         highlightSeriesOpts: {
//             strokeWidth: 3,
//             strokeBorderWidth: 1,
//             highlightCircleSize: 5
//           },
//         labels:["Step","# lobos", "# conejos"],
//         });
//     requestData();
    
    
    // var onclick = function(ev) 
    // {
    //     if (chart.isSeriesLocked()) {
    //         chart.clearSelection();
    //     } else {
    //         chart.setSelection(chart.getSelection(), chart.getHighlightSeries(), true);
    //     }
    // };
    // chart.updateOptions({clickCallback: onclick}, true);
    // chart.setSelection(false, 's005');

    // chart = new Dygraph($("#data-container"), data);

    // chart = new Highcharts.Chart({
    //     chart: {
    //         renderTo: 'data-container',
    //         events: {
    //             load: requestData
    //         },
    //         type: "line",
    //         animation: false,
    //     },
    //     plotOptions: {
    //         series: {
    //             showCheckbox: true,
    //             selected: true,
    //             events: {
    //                 checkboxClick: function () {
    //                     this.setVisible(!this.visible);
    //                 },
    //             },
    //         }
    //     },
    //     title: {
    //         text: 'Live random data'
    //     },
    //     xAxis: {
    //         type: 'linear',
    //         allowDecimals: false,
    //         min: 0
    //     },
    //     yAxis: {
    //         minPadding: 0.2,
    //         maxPadding: 0.2,
    //         title: {
    //             text: 'Value',
    //             margin: 80
    //         }
    //     },
    //     legend: {
    //         layout: 'vertical',
    //         align: 'right',
    //         verticalAlign: 'middle',
    //         itemStyle: {
    //             fontSize:'17px',
    //             // font: '20pt Trebuchet MS, Verdana, sans-serif',
    //             color: '#000'
    //          },
    //     //     //  itemCheckboxStyle: {
    //     //     //     cursor: "pointer",
    //     //     //     border: "1px solid #62737a",
    //     //     // },
    //     //     //  itemHoverStyle: {
    //     //     //     color: '#FFF'
    //     //     //  },
    //     //     //  itemHiddenStyle: {
    //     //     //     color: '#444'
    //     //     //  }
    //     },
    //     // tooltip: {
    //     //     crosshairs: [true, true],
    //     //     shared: true
    //     // },
    //     series: [
    //     {
    //         // marker: {
    //         //     enabled: true
    //         // },
    //         name: '# lobos',
    //         data: []
    //     },
    //     {
    //         // marker: {
    //         //     enabled: true
    //         // },
    //         name: '# conejos',
    //         data: []
    //     }]
    // });
// });
// set the dimensions and margins of the graph
var margin = {top: 10, right: 100, bottom: 30, left: 30},
width = 460 - margin.left - margin.right,
height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#data-container")
.append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

//Read the data
d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_connectedscatter.csv", function(data) {

// List of groups (here I have one group per column)
var allGroup = ["valueA", "valueB", "valueC"]

// Reformat the data: we need an array of arrays of {x, y} tuples
var dataReady = allGroup.map( function(grpName) { // .map allows to do something for each element of the list
return {
    name: grpName,
    values: data.map(function(d) {
    return {time: d.time, value: +d[grpName]};
    })
};
});
// I strongly advise to have a look to dataReady with
// console.log(dataReady)

// A color scale: one color for each group
var myColor = d3.scaleOrdinal()
.domain(allGroup)
.range(d3.schemeSet2);

// Add X axis --> it is a date format
var x = d3.scaleLinear()
.domain([0,10])
.range([ 0, width ]);
svg.append("g")
.attr("transform", "translate(0," + height + ")")
.call(d3.axisBottom(x));

// Add Y axis
var y = d3.scaleLinear()
.domain( [0,20])
.range([ height, 0 ]);
svg.append("g")
.call(d3.axisLeft(y));

// Add the lines
var line = d3.line()
.x(function(d) { return x(+d.time) })
.y(function(d) { return y(+d.value) })
svg.selectAll("myLines")
.data(dataReady)
.enter()
.append("path")
    .attr("class", function(d){ return d.name })
    .attr("d", function(d){ return line(d.values) } )
    .attr("stroke", function(d){ return myColor(d.name) })
    .style("stroke-width", 4)
    .style("fill", "none")

// create a tooltip
var Tooltip = d3.select("#data-container")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

// Three function that change the tooltip when user hover / move / leave a cell
var mouseover = function(d) {
    Tooltip
    .style("opacity", 1)
}
var mousemove = function(d) {
    Tooltip
    .html("Exact value: " + d.value)
    .style("left", (d3.mouse(this)[0]+70) + "px")
    .style("top", document.getElementById('data-container').offsetHeight + "px")
}
var mouseleave = function(d) {
    Tooltip
    .style("opacity", 0)
}


// Add the points
svg
// First we need to enter in a group
.selectAll("myDots")
.data(dataReady)
.enter()
    .append('g')
    .style("fill", function(d){ return myColor(d.name) })
    .attr("class", function(d){ return d.name })
// Second we need to enter in the 'values' part of this group
.selectAll("myPoints")
.data(function(d){ return d.values })
.enter()
.append("circle")
    .attr("cx", function(d) { return x(d.time) } )
    .attr("cy", function(d) { return y(d.value) } )
    .attr("r", 5)
    .attr("stroke", "white")
.on("mouseover", mouseover)
.on("mousemove", mousemove)
.on("mouseleave", mouseleave)

// Add a legend at the end of each line
svg
.selectAll("myLabels")
.data(dataReady)
.enter()
    .append('g')
    .append("text")
        .attr("class", function(d){ return d.name })
        .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; }) // keep only the last value of each time series
        .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.value) + ")"; }) // Put the text at the position of the last point
        .attr("x", 12) // shift the text a bit more right
        .text(function(d) { return d.name; })
        .style("fill", function(d){ return myColor(d.name) })
        .style("font-size", 15)

// Add a legend (interactive)
svg
.selectAll("myLegend")
.data(dataReady)
.enter()
.append('g')
.append("text")
    .attr('x', function(d,i){ return 30 + i*60})
    .attr('y', 30)
    .text(function(d) { return d.name; })
    .style("fill", function(d){ return myColor(d.name) })
    .style("font-size", 15)
.on("click", function(d){
    // is the element currently visible ?
    currentOpacity = d3.selectAll("." + d.name).style("opacity")
    // Change the opacity: from 0 to 1 or from 1 to 0
    d3.selectAll("." + d.name).transition().style("opacity", currentOpacity == 1 ? 0:1)
})
});
})