import React, { Component} from "react";

import {PieChart} from 'react-d3-components'

import './PieChart.style.css'

export class PieChartSample extends Component {

    render() {
        const data = this.props.data
            ,
        sort = null
        ;
        const tooltip = function(x, y) {
            return <div className={'tooltipP'}>{y.toString()}</div>;
        };
        return(
            <div className={'pieChartBlock'}>
            <PieChart
                data={data}
                width={600}
                height={400}
                margin={{top: 10, bottom: 10, left: 100, right: 100}}
                sort={sort}
                tooltipMode={'mouse'}
                tooltipHtml={tooltip}
            />
            <h2>Year: {this.props.data.label}</h2>
            </div>
        )
    }
}