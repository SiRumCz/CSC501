import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import {BarChart, LineChart} from 'react-d3-components'

import * as d3 from 'd3';

import './BarChart.style.css';
export class BarChartSample extends Component {


    constructor(props){
        super(props);

        this.state = {
            barData: [
                {
                    label: 'Ratings',
                    values: [{x: '1', y: 103}, {x: '2', y: 220}, {x: '3', y: 260}, {x: '4', y: 150}, {x: '5', y: 110}]
                }
            ]
        }

    }

    componentDidMount() {
        let barData = [{label: 'Ratings', values:[]}];
        fetch(`${this.props.ip}/num-movies-by-ratings`)
            .then(result => (result.json()))
            .then(data => {
                barData[0].values = data.map(rs => ({x: rs.counts.toString(), y: rs.rating}))
                this.setState({barData: barData});
            })
        const node = ReactDOM.findDOMNode(this);
        const g_x_element = node.querySelector('.x.axis.label')
        g_x_element.setAttribute('y', '46' )
    }



    render() {
        const data = this.props.data;
        const tooltip = function(x, y0, y) {
            return <div className={'tooltipP'}>{y.toString()}</div>;
        };
        const scale = d3.scaleOrdinal().range(d3.schemeCategory10);


        return(
            this.state.barData &&
            (<BarChart
                ref={this.x_axis_labels}
                data={this.state.barData}
                width={400}
                height={400}
                yAxis={{label: "Ratings Count"}}
                xAxis={{label: "Ratings"}}
                margin={{top: 10, bottom: 50, left: 50, right: 10}}
                tooltipMode={'mouse'}
                tooltipHtml={tooltip}
                colorByLabel={false}
                colorScale={scale}
            />)
        )
    }
}
