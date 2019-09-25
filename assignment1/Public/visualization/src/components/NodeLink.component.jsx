import React, {Component} from 'react';

import * as d3 from 'd3';

import './NodeLink.component.css'

export class NodeLink extends Component {


    constructor(props){
        super(props);

        this.state = {
            nodeLinkData: {
                nodes: [],
                links: []
            }
        }

    }
    render_node_link = () => {
        const graph = {nodes: this.state.nodeLinkData.nodes, links: this.state.nodeLinkData.links}
        const width = 800, height = 600;

        const svg = d3.select(this.ref)


        let g = svg.append("g")
            .attr("class", "everything");

        let color = d3.scaleOrdinal(d3.schemeCategory10);

        let simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function(d) { return d.id; }))
            .force("charge", d3.forceManyBody().distanceMax(150))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force('collide', d3.forceCollide(function(d) {
                return d.id === "j" ? 100 : 50
            }))
        ;

        let link = g.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("stroke-width", function(d) { return Math.sqrt(d.weight/40); });

        let node = g.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(graph.nodes)
            .enter().append("g")

        node.append("circle")
            .attr("r", 5)
            .attr("fill", function(d) { return color(d.group); })
            .attr("r", function(d) {
                if(d.value !== 0)
                return Math.sqrt(d.value/10);
                else {
                    return 3;
                }
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function(d) { return d.name });


        node.append("title")
            .text(function(d) { return d.id; });

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function zoom_actions(){
            g.attr("transform", d3.event.transform)
        }
        let zoom_handler = d3.zoom()
            .on("zoom", zoom_actions);

        zoom_handler(svg);
        function ticked() {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node
                .attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")";
                })
        }

        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            simulation.force("link", null).force("charge", null).force("center", null);
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

    }
    componentDidMount() {



        fetch(`${this.props.ip}/basic-node-link-v1`)
            .then(result => (result.json()))
            .then(data => {
                this.setState({nodeLinkData: data});
                this.render_node_link();
            })



    }
    render() {

        return (
            <svg ref={(ref) => this.ref = ref} width={1000} height={700}>
            </svg>
        );
    }
}