import React, {Component} from 'react';

import * as d3 from 'd3';

import {LineChart} from 'react-d3-components';

import './LinePlot.style.css'
import ReactDOM from "react-dom";

export class LinePlot extends Component {

    constructor(props){
        super(props);

        this.state = {
            lines: [
                {
                    label: 'pickups',
                    values: [{x: 2010, y: 2}, {x: 2011, y: 5}, {x: 2012, y: 6}, {x: 2013, y: 6.5}, {x: 2014, y: 6}, {x: 2015, y: 6}, {x: 2016, y: 7}, {x: 2017, y: 8}]
                }
            ]
        }

    }


    componentDidMount() {
        const {genres} = this.props;
        let lineData = [];
        fetch(`${this.props.ip}/pickup-rush-hours`)
            .then(result => (result.json()))
            .then(data => {
                    lineData.push({label: 'pickups', values: []});
                    lineData[lineData.length-1].values = data.map(rs => ({x: rs.time[0]+rs.time[1], y: rs.pickups/1000}))
                this.setState({lines: lineData})

            })
        const node = ReactDOM.findDOMNode(this);
        const g_x_element = node.querySelector('.x.axis.label')
        g_x_element.setAttribute('y', '46' )
    }
    render(){
        const tooltipLine = function(label, data) {
            return label;
        }
        return(
            this.state.lines &&
            (<LineChart
                    data={this.state.lines}
                    width={800}
                    height={400}
                    yAxis={{label: "Number of Pickups(x1000)"}}
                    margin={{top: 10, bottom: 50, left: 50, right: 10}}
                    tooltipHtml={tooltipLine}
                    xAxis={{tickFormat: d3.format("d"), label: "Time during the day"}}

            />)
        )
    }
}
