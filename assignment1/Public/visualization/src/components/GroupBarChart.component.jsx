import React, {Component} from 'react';

import {BarChart} from 'react-d3-components';

export class GroupBarChart extends Component {

    render(){
        const data = this.props.data;

        const tooltip = function(x, y0, y, title) {

            return <div className={'tooltipP'}>{title}</div>;
        };
        return(
            <BarChart
                groupedBars
                data={data}
                width={600}
                height={400}
                margin={{top: 10, bottom: 50, left: 50, right: 10}}
                tooltipHtml={tooltip}
            />
        )
    }
}