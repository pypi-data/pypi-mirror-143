//////////////////////
//  main constants  //
//////////////////////
const WIDTH = $width;
const HEIGHT = $height;
const dataset = $data;
const tooltipAttributes = $tooltip;
const useviewBox = $view_box;
const useCanvas = $canvas;

const MARGIN = { TOP: 10, BOTTOM: 10, LEFT: 10, RIGHT: 10 };
const widthSVG = WIDTH - MARGIN.RIGHT - MARGIN.LEFT;
const heightSVG = HEIGHT - MARGIN.TOP - MARGIN.BOTTOM;
let container;

////////////////////////////////
//  Check the dataset format  //
////////////////////////////////
let goodFormat = true;
dataset.nodes.every(element => {
    if (element.id === undefined) {
        goodFormat = false;
        return false;
    }
    return true
});
dataset.links.every(element => {
    if ((element.source === undefined) || (element.target === undefined)) {
        goodFormat = false;
        return false;
    }
    return true;
});
if (!goodFormat) {
    let errorText = "The dataset isn't in the correct format"
    d3.select('#pynetworkd3-chart').append("text").text(errorText)
    throw new Error(errorText);
}

///////////////////////////////////////////////
//  Build main html element (canvas or svg)  //
///////////////////////////////////////////////
if (useCanvas) {
    container = d3.select('#pynetworkd3-chart').append('canvas')
        .attr('width', widthSVG + 'px')
        .attr('height', heightSVG + 'px')
        .node();

} else {
    const SVG = d3.select('#pynetworkd3-chart').append('svg');

    if (useviewBox) {
        SVG.attr("viewBox", [0, 0, WIDTH, HEIGHT]);
    } else {
        SVG.attr('width', WIDTH).attr('height', HEIGHT);
    }

    container = SVG.append("g").attr(
        "transform",
        `translate(${MARGIN.LEFT}, ${MARGIN.TOP})`
    );
}

//////////////////////////
//  Auxiliar functions  //
//////////////////////////
const tooltip = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

function ShowTooltip(element, event, KWS) {
    if (!KWS.tooltip) return;
    let content = '<table style="margin-top: 2.5px;">'
    KWS.tooltip.forEach(d2 => {
        content += `<tr><td>${d2}: </td><td style="text-align: right">${element[d2]}</td></tr>`
    })
    content += '</table>'

    tooltip
        .transition()
        .duration(200)
        .style("opacity", 0.9);

    tooltip
        .html(content)

    let tooltipWidth = tooltip.node().offsetWidth;
    let posX = event.pageX;
    if (event.pageX + tooltipWidth > widthSVG) {
        posX -= tooltipWidth
    };
    tooltip
        .style("left", posX + "px")
        .style("top", event.pageY - (KWS.tooltip.length * 29) + "px");
}

function HideTooltip(KWS) {
    if (!KWS.tooltip) return;
    tooltip
        .transition()
        .duration(200)
        .style("opacity", 0);

}

$aux_functions;

/////////////////
//  main code  //
/////////////////