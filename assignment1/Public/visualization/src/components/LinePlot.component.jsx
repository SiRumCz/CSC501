import React, {Component} from 'react';

import * as d3 from 'd3';

import {LineChart} from 'react-d3-components';

import './LinePlot.style.css'

export class LinePlot extends Component {

    constructor(props){
        super(props);

        this.state = {
            lines: [
                {
                    label: 'Comedy',
                    values: [{x: 2010, y: 2}, {x: 2011, y: 5}, {x: 2012, y: 6}, {x: 2013, y: 6.5}, {x: 2014, y: 6}, {x: 2015, y: 6}, {x: 2016, y: 7}, {x: 2017, y: 8}]
                },
                {
                    label: 'Action',
                    values: [{x: 2010, y: 3}, {x: 2011, y: 4}, {x: 2012, y: 7}, {x: 2013, y: 8}, {x: 2014, y: 7}, {x: 2015, y: 7}, {x: 2016, y: 7.8}, {x: 2017, y: 9}]
                }
            ]
        }

    }


    componentDidMount() {
        const {genres} = this.props;
        let lineData = [];
        fetch(`${this.props.ip}/genres-distribution-per-year`)
            .then(result => (result.json()))
            .then(data => {
                genres.forEach(genre => {
                    lineData.push({label: genre, values: []});
                    lineData[lineData.length-1].values = data.map(rs => ({x: rs.year, y: rs.data[0][genre]}))

                })
                this.setState({lines: lineData})

            })
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
                    margin={{top: 10, bottom: 50, left: 50, right: 10}}
                    tooltipHtml={tooltipLine}
                    xAxis={{tickFormat: d3.format("d")}}

            />)
        )
    }
}