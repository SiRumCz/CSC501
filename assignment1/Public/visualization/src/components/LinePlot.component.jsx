import React, {Component} from 'react';

import * as d3 from 'd3';

import {LineChart} from 'react-d3-components';

import './LinePlot.style.css'

export class LinePlot extends Component {

    render(){
        const tooltipLine = function(label, data) {
            return label;
        }
        return(

            <LineChart
                    data={this.props.data}
                    width={800}
                    height={400}
                    margin={{top: 10, bottom: 50, left: 50, right: 10}}
                    tooltipHtml={tooltipLine}
                    xAxis={{tickFormat: d3.format("d")}}

            />
        )
    }
}