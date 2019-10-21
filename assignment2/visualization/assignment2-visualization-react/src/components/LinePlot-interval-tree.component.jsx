import React, {Component} from 'react';

import * as d3 from 'd3';

import {LineChart} from 'react-d3-components';

import './LinePlot.style.css'
import ReactDOM from "react-dom";

export class LinePlotInterval extends Component {
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
        let lineData = [];
        fetch(`${this.props.ip}/${this.props.api}`)
            .then(result => (result.json()))
            .then(data => {
                data.data.forEach((obj, i) => {
                    lineData.push({label: 'Interval #'+i, values: []});
                    if(this.props.api === 'interval-tree-passengers') {
                        let x1 = 0, x2 = 0;
                        if(obj.fromDate === "2018-12") {
                            x1 = 0;
                        } else {
                            x1 = parseInt(obj.fromDate.slice(5));
                        }
                        if(obj.toDate === "2018-12") {
                            x2 = 0;
                        } else {
                            x2 = parseInt(obj.toDate.slice(5));
                        }
                        lineData[lineData.length - 1].values.push({
                            x: x1,
                            y: obj.passengerNum
                        });
                        lineData[lineData.length - 1].values.push({
                            x: x2,
                            y: obj.passengerNum
                        })
                    } else {
                        lineData[lineData.length - 1].values.push({
                            x: obj.fromDate,
                            y: Math.sqrt(obj.passengerNum)
                        });
                        lineData[lineData.length - 1].values.push({
                            x: obj.toDate,
                            y: Math.sqrt(obj.passengerNum)
                        })
                    }

                })
                this.setState({lines: lineData});
            })


        const node = ReactDOM.findDOMNode(this);
        const g_x_element = node.querySelector('.x.axis.label')
        g_x_element.setAttribute('y', '46' )
    }
    render(){
        let x_axis_label = '';
        if(this.props.api === 'interval-tree-passengers') {
            x_axis_label = "From December 2018 until September 2019";
        } else {
            x_axis_label = "Months in 2018";
        }
        const tooltipLine = function(label, data) {
            return label;
        }
        return(
            this.state.lines &&
            (<LineChart
                data={this.state.lines}
                width={1100}
                height={400}
                yAxis={{label: "y value"}}
                margin={{top: 10, bottom: 50, left: 50, right: 10}}
                tooltipHtml={tooltipLine}
                xAxis={{tickFormat: d3.format("d"), label: x_axis_label}}

            />)
        )
    }
}
