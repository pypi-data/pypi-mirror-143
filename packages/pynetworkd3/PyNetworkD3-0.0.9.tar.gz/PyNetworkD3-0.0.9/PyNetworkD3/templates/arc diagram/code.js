$main

const LEG_HOVER_KWS = $legend_kws;
const NODE_KWS = $node_kws;
const LINK_KWS = $link_kws;

let RADIUS = 0.5 * widthSVG / (dataset.nodes.length + 0.0000001);;
let COLOR_NODE = "#abd9e9";
let COLOR_LINK = "black";
let STROKE_WIDTH = 1;

if (NODE_KWS.size_default) {
    RADIUS = NODE_KWS.size_default;
}
if (NODE_KWS.color_default) {
    COLOR_NODE = NODE_KWS.color_default;
}
if (LINK_KWS.color_default) {
    COLOR_LINK = LINK_KWS.color_default;
}
if (LINK_KWS.stroke_width) {
    STROKE_WIDTH = LINK_KWS.stroke_width;
}

let x = d3.scalePoint()
    .range([RADIUS, widthSVG - RADIUS])
    .domain(dataset.nodes.map((d) => d.id))

let idToNode = {};
dataset.nodes.forEach(function(n) {
    idToNode[n.id] = n;
});

let color = GetColorFunction(NODE_KWS, dataset, COLOR_NODE);
let colorLink = GetColorFunction(LINK_KWS, dataset, COLOR_LINK);
let size = GetSizeFunction(NODE_KWS, dataset, RADIUS)

let links = container.append("g")
    .selectAll('path')
    .data(dataset.links)
    .enter()
    .append('path')
    .attr('d', function(d) {
        start = x(idToNode[d.source].id) // X position of start node on the X axis
        end = x(idToNode[d.target].id) // X position of end node
        return ['M', start, heightSVG - RADIUS, // the arc starts at the coordinate x=start, y=heightSVG-30 (where the starting node is)
                'A', // This means we're gonna build an elliptical arc
                (start - end) / 2, ',', // Radius in X
                Math.min(Math.abs(start - end) / 2, heightSVG), // Radius in Y
                0, 0, ',',
                start < end ? 1 : 0, end, ',', heightSVG - RADIUS
            ] // We always want the arc on top. So if end is before start, putting 0 here turn the arc upside down.
            .join(' ');
    })
    .attr("stroke", colorLink)
    .attr("stroke-width", STROKE_WIDTH);

if (LINK_KWS.hover) {
    links.on('mouseover', function(event, d) {
            if (LEG_HOVER_KWS.show) {
                hoverLegend.style("display", "block");
            }
            nodes.style('fill', node => {
                if (d.target == node.id) return LEG_HOVER_KWS.color_target_hovered;
                if (d.source == node.id) return LEG_HOVER_KWS.color_source_hovered;
                return "#B8B8B8";
            })
            links.style('stroke', (link_d) => {
                    if (link_d == d) return "red";
                    return '#b8b8b8';
                })
                .style('stroke-width', (link_d) => link_d == d ? STROKE_WIDTH : 0.3)

            ShowTooltip(d, event, LINK_KWS);
        })
        .on('mouseout', function(_) {
            if (LEG_HOVER_KWS.show) {
                hoverLegend.style("display", "none");
            }
            nodes.style('fill', color)
            links
                .style('stroke', colorLink)
                .style('stroke-width', null);
            HideTooltip(LINK_KWS);
        })
}


let nodes = container.append("g")
    .selectAll("circle")
    .data(dataset.nodes)
    .enter()
    .append("circle")
    .attr("cx", function(d) { return (x(d.id)) })
    .attr("cy", heightSVG - RADIUS)
    .attr("r", size)
    .attr("fill", color);

let hoverLegend;
if (LEG_HOVER_KWS.show) {
    buildHoverLegend()
}

if (NODE_KWS.hover) {
    nodes
        .on('mouseover', function(event, d) {
            if (LEG_HOVER_KWS.show) {
                hoverLegend.style("display", "block");
            }
            let targetNodes = new Set(dataset.links.filter(link => link.source === d.id).map(d => d.target));
            let sourceNodes = new Set(dataset.links.filter(link => link.target === d.id).map(d => d.source));

            nodes.style('fill', node => {
                if (node == d) return "red";
                if (targetNodes.has(node.id)) return LEG_HOVER_KWS.color_target_hovered;
                if (sourceNodes.has(node.id)) return LEG_HOVER_KWS.color_source_hovered;
                return "#B8B8B8";
            })
            links
                .style('stroke', (link_d) => {
                    if (link_d.source === d.id) return LEG_HOVER_KWS.color_target_hovered;
                    if (link_d.target === d.id) return LEG_HOVER_KWS.color_source_hovered;
                    return '#b8b8b8';
                })
                .style('stroke-width', (link_d) => link_d.source === d.id || link_d.target === d.id ? 2 : 0.3)

            ShowTooltip(d, event, NODE_KWS);
        })
        .on('mouseout', function(_) {
            if (LEG_HOVER_KWS.show) {
                hoverLegend.style("display", "none");
            }
            nodes.style('fill', color)
            links
                .style('stroke', colorLink)
                .attr("stroke-width", STROKE_WIDTH);

            HideTooltip(NODE_KWS);
        })
}

function buildHoverLegend() {
    const FontProp = 0.03 * LEG_HOVER_KWS.scale_size;
    const RadioProp = 0.015 * LEG_HOVER_KWS.scale_size;

    hoverLegend = container
        .append("g")
        .attr("transform", `translate(${RadioProp * widthSVG}, ${RadioProp * widthSVG})`)
        .style("display", "none");

    hoverLegend
        .append("circle")
        .attr("cy", 0)
        .attr("r", RadioProp * widthSVG)
        .style("fill", LEG_HOVER_KWS.color_source_hovered);

    hoverLegend.append("text")
        .style("dominant-baseline", "central")
        .attr("x", 1.2 * RadioProp * widthSVG)
        .attr("y", 0)
        .style("font-size", FontProp * widthSVG)
        .text("Source node");

    hoverLegend
        .append("circle")
        .attr("cy", 1.2 * Math.max(FontProp * widthSVG, RadioProp * widthSVG))
        .attr("r", RadioProp * widthSVG)
        .style("fill", LEG_HOVER_KWS.color_target_hovered);

    hoverLegend.append("text")
        .style("dominant-baseline", "central")
        .attr("x", 1.2 * RadioProp * widthSVG)
        .attr("y", 1.2 * Math.max(FontProp * widthSVG, RadioProp * widthSVG))
        .style("font-size", FontProp * widthSVG)
        .text("Target node");
}