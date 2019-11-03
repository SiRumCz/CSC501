import React, {Component} from 'react';

import * as d3 from 'd3';

import {les_miserables} from "./les_miserables.data";

import './NodeLink.component.css'

export class NodeLink extends Component {


    constructor(props){
        super(props);



    }
    render_node_link = () => {
        const graph = {
            nodes: les_miserables.nodes,
            links: les_miserables.links
        };
        let svg = d3.select(this.ref),
            width = +svg.attr("width"),
            height = +svg.attr("height");

        let color = d3.scaleOrdinal(d3.schemeCategory10);

        let simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function(d) { return d.id; }))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2))

        ;


        let link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

            let node = svg.append("g")
                .attr("class", "nodes")
                .selectAll("g")
                .data(graph.nodes)
                .enter().append("g")

            let circles = node.append("circle")
                .attr("r", 5)
                .attr("fill", function(d) { return color(d.group); })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            let lables = node.append("text")
                .text(function(d) {
                    return d.id;
                })
                .attr('x', 6)
                .attr('y', 3);

            node.append("title")
                .text(function(d) { return d.id; });

            simulation
                .nodes(graph.nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(graph.links);

            function ticked() {
                link.attr("x1", function (d) {
                    return d.source.x;
                })
                    .attr("y1", function (d) {
                        return d.source.y;
                    })
                    .attr("x2", function (d) {
                        return d.target.x;
                    })
                    .attr("y2", function (d) {
                        return d.target.y;
                    });

                node.attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });
            }

        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.5).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0.5);
            d.fx = null;
            d.fy = null;
        }



    }
    componentDidMount() {
        this.render_node_link();

    }
    render() {

        return (
            <svg ref={(ref) => this.ref = ref} width={1000} height={700}>
            </svg>
        );
    }
}