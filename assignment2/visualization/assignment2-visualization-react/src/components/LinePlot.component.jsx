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
                    label: 'pickups-total',
                    values: [{x: 2010, y: 2}, {x: 2011, y: 5}, {x: 2012, y: 6}, {x: 2013, y: 6.5}, {x: 2014, y: 6}, {x: 2015, y: 6}, {x: 2016, y: 7}, {x: 2017, y: 8}]
                },
                {
                    label: 'pickups-2018-processed-data',
                    values: [{x: 2010, y: 10}, {x: 2011, y: 4}, {x: 2012, y: 2}, {x: 2013, y: 8}, {x: 2014, y: 2}, {x: 2015, y: 4}, {x: 2016, y: 1}, {x: 2017, y: 6}]
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
                    lineData.push({label: 'pickups-zipfile-connex', values: []});
                    lineData[lineData.length-1].values = data.map(rs => ({x: parseInt(rs.time[0]+rs.time[1]), y: Math.abs(Math.sqrt(rs.pickups))}))
                fetch(`${this.props.ip}/pickup-rush-hours-2018`)
                    .then(result => (result.json()))
                    .then(data => {
                        lineData.push({label: 'pickups-2018-processed-data', values: []});
                        lineData[lineData.length-1].values = data.map(rs => ({x: parseInt(rs.time[0]+rs.time[1]), y: Math.abs(Math.sqrt(rs.pickups))}))
                        this.setState({lines: lineData})
                        console.log(this.state.lines);
                    })
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
                    width={900}
                    height={400}
                    yAxis={{label: "Number of Pickups(square root)"}}
                    margin={{top: 10, bottom: 50, left: 50, right: 10}}
                    tooltipHtml={tooltipLine}
                    xAxis={{tickFormat: d3.format("d"), label: "Time during the day"}}

            />)
        )
    }
}
