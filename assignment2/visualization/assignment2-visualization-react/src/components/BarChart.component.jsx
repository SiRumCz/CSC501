import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import {BarChart} from 'react-d3-components'

import * as d3 from 'd3';

import './BarChart.style.css';
export class BarChartSample extends Component {


    constructor(props){
        super(props);

        this.state = {
            barData: [
                {
                    label: 'Payment Method',
                    values: [{x: '1', y: 103}, {x: '2', y: 220}, {x: '3', y: 260}, {x: '4', y: 150}, {x: '5', y: 110}]
                }
            ]
        }

    }

    componentDidMount() {
        let barData = [{label: 'Payment Method', values:[]}];
        fetch(`${this.props.ip}/payment-trend-usage`)
            .then(result => (result.json()))
            .then(data => {
                barData[0].values = data.map(rs => ({x: rs.paymentType, y: (rs.totalUsage > 0) ? Math.floor(Math.abs(Math.log(rs.totalUsage))) : 0}))
                barData[0].values.splice(barData[0].values.length-2, 2);
                this.setState({barData: barData});
            })
        const node = ReactDOM.findDOMNode(this);
        const g_x_element = node.querySelector('.x.axis.label')
        g_x_element.setAttribute('y', '46' )
    }



    render() {
        const tooltip = function(x, y0, y) {
            return <div className={'tooltipP'}>{y.toString()}</div>;
        };
        const scale = d3.scaleOrdinal().range(d3.schemeCategory10);


        return(
            this.state.barData &&
            (<BarChart
                data={this.state.barData}
                width={600}
                height={400}
                yAxis={{label: "Usage of each method(logy)"}}
                xAxis={{label: "Payment Method"}}
                margin={{top: 10, bottom: 50, left: 50, right: 10}}
                tooltipMode={'mouse'}
                tooltipHtml={tooltip}
                colorByLabel={false}
                colorScale={scale}
            />)
        )
    }
}
