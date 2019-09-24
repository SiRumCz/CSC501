import React, {Component} from 'react';

import {BarChart} from 'react-d3-components';

export class GroupBarChart extends Component {


    constructor(props){
        super(props);

        this.state = {
            groupBarData: [
                {
                    label: 'comedy',
                    values: [{x: '2015', y: 8, title:"Comedy" }, {x: '2016', y: 4, title:"Comedy"}, {x: '2017', y: 3, title:"Comedy"}, {x: '2018', y: 3, title:"Comedy"}]
                },
                {
                    label: 'Horror',
                    values: [{x: '2015', y: 4, title:"Horror" }, {x: '2016', y: 6, title:"Horror"}, {x: '2017', y: 1, title:"Horror"}, {x: '2018', y: 7, title:"Horror"}]
                }
            ]
        }

    }

    componentDidMount() {
        const ratings = ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'];
        let groupData = [];

        fetch(`${this.props.ip}/rating-distribution-each-year`)
            .then(result => (result.json()))
            .then(data => {
                ratings.forEach(rate => {
                    groupData.push({label: rate, values: []});
                    groupData[groupData.length-1].values = data.map(rs => ({x: rs.year.toString(), y: rs.data.filter(rateCount => (rateCount.counts.toString() === rate))[0], title: rate}) )

                })
                groupData.forEach(data => {
                    data.values.forEach(value => {
                        if(value.y) {
                            value.y = value.y.rating;
                        }
                        else {
                            value.y = 0;
                        }
                    })
                    data.values.sort(this.compare);
                })
                this.setState({groupBarData: groupData})
            })

    }

    compare = (a, b) => {
        if(parseInt(a.x) < parseInt(b.x)) {
            return -1;
        }
        if (parseInt(a.x) > parseInt(b.x)) {
            return 1;
        }
        return 0;

    }
    render(){

        const tooltip = function(x, y0, y, title) {
            return <div className={'tooltipP'}>{title}</div>;
        };
        return(
            <BarChart
                groupedBars
                data={this.state.groupBarData}
                width={1400}
                height={600}
                margin={{top: 10, bottom: 50, left: 50, right: 10}}
                tooltipHtml={tooltip}
            />
        )
    }
}