//Flot Bar Chart
// $(function() {
//     var barOptions = {
//         series: {
//             bars: {
//                 show: true,
//                 barWidth: 0.6,
//                 fill: true,
//                 fillColor: {
//                     colors: [{
//                         opacity: 0.8
//                     }, {
//                         opacity: 0.8
//                     }]
//                 }
//             }
//         },
//         xaxis: {
//             tickDecimals: 0
//         },
//         colors: ["#1ab394"],
//         grid: {
//             color: "#999999",
//             hoverable: true,
//             clickable: true,
//             tickColor: "#D4D4D4",
//             borderWidth:0
//         },
//         legend: {
//             show: false
//         },
//         tooltip: true,
//         tooltipOpts: {
//             content: "x: %x, y: %y"
//         }
//     };
//     var barData = {
//         label: "bar",
//         data: [
//             [1, 34],
//             [2, 25],
//             [3, 19],
//             [4, 34],
//             [5, 32],
//             [6, 44]
//         ]
//     };
//     $.plot($("#flot-bar-chart"), [barData], barOptions);
//
// });

// $(function() {
//     var barOptions = {
//         series: {
//             lines: {
//                 show: true,
//                 lineWidth: 2,
//                 fill: true,
//                 fillColor: {
//                     colors: [{
//                         opacity: 0.0
//                     }, {
//                         opacity: 0.0
//                     }]
//                 }
//             }
//         },
//         xaxis: {
//             tickDecimals: 0
//         },
//         colors: ["#1ab394"],
//         grid: {
//             color: "#999999",
//             hoverable: true,
//             clickable: true,
//             tickColor: "#D4D4D4",
//             borderWidth:0
//         },
//         legend: {
//             show: false
//         },
//         tooltip: true,
//         tooltipOpts: {
//             content: "x: %x, y: %y"
//         }
//     };
//     var barData = {
//         label: "bar",
//         data: [
//             [1, 34],
//             [2, 25],
//             [3, 19],
//             [4, 34],
//             [5, 32],
//             [6, 44]
//         ]
//     };
//     $.plot($("#flot-line-chart"), [barData], barOptions);
//
// });
//Flot Pie Chart
// $(function() {
//
//     var data = [{
//         label: "数据 1",
//         data: 21,
//         color: "#d3d3d3",
//     }, {
//         label: "数据 2",
//         data: 3,
//         color: "#bababa",
//     }, {
//         label: "数据 3",
//         data: 15,
//         color: "#79d2c0",
//     }, {
//         label: "数据 4",
//         data: 52,
//         color: "#1ab394",
//     }];
//
//     var plotObj = $.plot($("#flot-pie-chart"), data, {
//         series: {
//             pie: {
//                 show: true
//             }
//         },
//         grid: {
//             hoverable: true
//         },
//         tooltip: true,
//         tooltipOpts: {
//             content: "%p.0%, %s", // show percentages, rounding to 2 decimal places
//             shifts: {
//                 x: 20,
//                 y: 0
//             },
//             defaultTheme: false
//         }
//     });
//
// });

// $(function() {
//
//     var container = $("#flot-line-chart-moving");
//
//     // Determine how many data points to keep based on the placeholder's initial size;
//     // this gives us a nice high-res plot while avoiding more than one point per pixel.
//
//     var maximum = container.outerWidth() / 2 || 300;
//
//     //
//
//     var data = [];
//
//     function getRandomData() {
//
//         if (data.length) {
//             data = data.slice(1);
//         }
//
//         while (data.length < maximum) {
//             var previous = data.length ? data[data.length - 1] : 50;
//             var y = previous + Math.random() * 10 - 5;
//             data.push(y < 0 ? 0 : y > 100 ? 100 : y);
//         }
//
//         // zip the generated y values with the x values
//
//         var res = [];
//         for (var i = 0; i < data.length; ++i) {
//             res.push([i, data[i]])
//         }
//
//         return res;
//     }
//
//     //
//
//     series = [{
//         data: getRandomData(),
//         lines: {
//             fill: true
//         }
//     }];
//
//     //
//
//     var plot = $.plot(container, series, {
//         grid: {
//
//             color: "#999999",
//             tickColor: "#D4D4D4",
//             borderWidth:0,
//             minBorderMargin: 20,
//             labelMargin: 10,
//             backgroundColor: {
//                 colors: ["#ffffff", "#ffffff"]
//             },
//             margin: {
//                 top: 8,
//                 bottom: 20,
//                 left: 20
//             },
//             markings: function(axes) {
//                 var markings = [];
//                 var xaxis = axes.xaxis;
//                 for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
//                     markings.push({
//                         xaxis: {
//                             from: x,
//                             to: x + xaxis.tickSize
//                         },
//                         color: "#fff"
//                     });
//                 }
//                 return markings;
//             }
//         },
//         colors: ["#1ab394"],
//         xaxis: {
//             tickFormatter: function() {
//                 return "";
//             }
//         },
//         yaxis: {
//             min: 0,
//             max: 110
//         },
//         legend: {
//             show: true
//         }
//     });
//
//     // Update the random dataset at 25FPS for a smoothly-animating chart
//
//     setInterval(function updateRandom() {
//         series[0].data = getRandomData();
//         plot.setData(series);
//         plot.draw();
//     }, 40);
//
// });

//Flot Multiple Axes Line Chart
$(function() {
    var oilprices = [
        [1167692400000, 61.05],
        [1167778800000, 58.32],
        [1167865200000, 57.35],
        [1167951600000, 56.31],
        [1168210800000, 55.55]
    ];

    var exchangerates = [
        [1167692400000, 61.05],
        [1167778800000, 58.32],
        [1167865200000, 57.35],
        [1167951600000, 56.31],
        [1168210800000, 55.55],
        [1168297200000, 55.64]
    ];

        var add1 = [
        [1167692400000, 61.05],
        [1167778800000, 58.32],
        [1167865200000, 57.35],
        [1167951600000, 56.31],
        [1168210800000, 55.55],
        [1168297200000, 55.64]
    ]

    function euroFormatter(v, axis) {
        return "&yen;"+v.toFixed(axis.tickDecimals);
    }

    function doPlot(position) {
        $.plot($("#flot-line-chart-multi"), [{
            data: oilprices,
            label: "油价 (&yen;)"
        }, {
            data: exchangerates,
            label: "美元/人民币汇率",
            yaxis: 2
        },{
            data: add1,
            label: "add1",
            yaxis: 3
        }], {
            xaxes: [{
                mode: 'time'
            }],
            yaxes: [{
                min: 0
            }, {
                // align if we are to the right
                alignTicksWithAxis: position == "right" ? 1 : null,
                position: position,
                tickFormatter: euroFormatter
            }],
            legend: {
                position: 'sw'
            },
            colors: ["#1ab394"],
            grid: {
                color: "#999999",
                hoverable: true,
                clickable: true,
                tickColor: "#D4D4D4",
                borderWidth:0,
                hoverable: true //IMPORTANT! this is needed for tooltip to work,

            },
            tooltip: true,
            tooltipOpts: {
                content: "%s %x 为 %y",
                xDateFormat: "%y-%0m-%0d",

                onHover: function(flotItem, $tooltipEl) {
                    // console.log(flotItem, $tooltipEl);
                }
            }

        });
    }

    doPlot("right");

    $("button").click(function() {
        doPlot($(this).text());
    });
});




