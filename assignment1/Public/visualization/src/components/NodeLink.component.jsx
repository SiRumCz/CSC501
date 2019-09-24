import React, {Component} from 'react';


import { Graph } from "react-d3-graph";


export class NodeLink extends Component {


    render() {
        const data = {
            nodes: [{ id: "Harry" }, { id: "Sally" }, { id: "Alice" }],
            links: [{ source: "Harry", target: "Sally" }, { source: "Harry", target: "Alice" }],
        };
        const myConfig = {
            nodeHighlightBehavior: true,
            node: {
                color: "lightgreen",
                size: 120,
                highlightStrokeColor: "blue",
            },
            link: {
                highlightColor: "lightblue",
            },
        };
        return(
            <Graph
                id="node-link"
                data={data}
                config={myConfig}
            />
        )

    }
}