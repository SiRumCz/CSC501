import React, { Component } from 'react';

import {BarChart} from 'react-d3-components'

import * as d3 from 'd3';

import './BarChart.style.css';
export class BarChartSample extends Component {



    render() {
        const data = this.props.data;
        const tooltip = function(x, y0, y) {
            return <div className={'tooltipP'}>{y.toString()}</div>;
        };
        const scale = d3.scaleOrdinal().range(d3.schemeCategory10);


        return(
            <BarChart
                data={data}
                width={400}
                height={400}
                margin={{top: 10, bottom: 50, left: 50, right: 10}}
                tooltipMode={'mouse'}
                tooltipHtml={tooltip}
                colorByLabel={false}
                colorScale={scale}
            />
        )
    }
}
