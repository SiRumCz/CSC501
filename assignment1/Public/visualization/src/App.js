import React, { Component } from 'react';
import './App.css';

import { BarChartSample } from './components/BarChart.component';
// import {PieChartSample} from "./components/PieChart.component";

import {LinePlot} from "./components/LinePlot.component";
import {GroupBarChart} from "./components/GroupBarChart.component";
import {WordCloudSample} from "./components/WordCloud.component";

class App extends Component{

    constructor(props){
        super(props);

        this.state = {
            barData:[
                {
                    label: 'Ratings',
                    values: [{x: '1', y: 103}, {x: '2', y: 220}, {x: '3', y: 260}, {x: '4', y: 150}, {x: '5', y: 110}]
                }
            ],
            pieData: [{
                label: '2010',
                values: [{x: '1star', y: 27}, {x: '2star', y: 40}, {x: '3star', y: 50}, {
                    x: '4star',
                    y: 12
                }, {x: '5star', y: 15}]
            },
                {
                    label: '2011',
                    values: [{x: '1star', y: 24}, {x: '2star', y: 20}, {x: '3star', y: 70}, {
                        x: '4star',
                        y: 18
                    }, {x: '5star', y: 7}]
                },
                {
                    label: '2012',
                    values: [{x: '1star', y: 14}, {x: '2star', y: 29}, {x: '3star', y: 40}, {x: '4star', y: 38}, {x: '5star', y: 17}]
                },
                {
                    label: '2013',
                    values: [{x: '1star', y: 25}, {x: '2star', y: 30}, {x: '3star', y: 30}, {
                        x: '4star',
                        y: 8
                    }, {x: '5star', y: 37}]
                }
            ],
            groupBarData: [
                {
                    label: 'comedy',
                    values: [{x: '2015', y: 8, title:"Comedy" }, {x: '2016', y: 4, title:"Comedy"}, {x: '2017', y: 3, title:"Comedy"}, {x: '2018', y: 3, title:"Comedy"}]
                },
                {
                    label: 'Horror',
                    values: [{x: '2015', y: 4, title:"Horror" }, {x: '2016', y: 6, title:"Horror"}, {x: '2017', y: 1, title:"Horror"}, {x: '2018', y: 7, title:"Horror"}]
                },
                {
                    label: 'Action',
                    values: [{x: '2015', y: 3, title:"Action" }, {x: '2016', y: 8, title:"Action"}, {x: '2017', y: 3, title:"Action"}, {x: '2018', y: 4, title:"Action"}]
                },
                {
                    label: 'Fiction',
                    values: [{x: '2015', y: 6, title:"Fiction"}, {x: '2016', y: 5, title:"Fiction"}, {x: '2017', y: 8, title:"Fiction"}, {x: '2018', y: 2, title:"Fiction"}]
                }
            ],
            linePLot: [
                {
                    label: 'Comedy',
                    values: [{x: 2010, y: 2}, {x: 2011, y: 5}, {x: 2012, y: 6}, {x: 2013, y: 6.5}, {x: 2014, y: 6}, {x: 2015, y: 6}, {x: 2016, y: 7}, {x: 2017, y: 8}]
                },
                {
                    label: 'Action',
                    values: [{x: 2010, y: 3}, {x: 2011, y: 4}, {x: 2012, y: 7}, {x: 2013, y: 8}, {x: 2014, y: 7}, {x: 2015, y: 7}, {x: 2016, y: 7.8}, {x: 2017, y: 9}]
                },
                {
                    label: 'Drama',
                    values: [{x: 2010, y: 4}, {x: 2011, y: 2}, {x: 2012, y: 3}, {x: 2013, y: 6}, {x: 2014, y: 10}, {x: 2015, y: 9}, {x: 2016, y: 2}, {x: 2017, y: 4}]
                },
                {
                    label: 'Horror',
                    values: [{x: 2010, y: 1}, {x: 2011, y: 5}, {x: 2012, y: 2}, {x: 2013, y: 3}, {x: 2014, y: 8}, {x: 2015, y: 4}, {x: 2016, y: 5}, {x: 2017, y: 3}]
                }
            ]
        }
    }

    render () {
        return(
        <div className="App">
            <h1 className={'margin-top-50'}> Bar chart for movies by ranking:</h1>
            <div className={'margin-top-50'}>
            <BarChartSample data={this.state.barData}/>
            </div>
            <hr/>
            <h1 className={'margin-top-50'}> Different ratings in different genres across past several years:</h1>
            {/*<PieChartSample data={this.state.pieData[0]}/>*/}
            {/*<PieChartSample data={this.state.pieData[1]}/>*/}
            {/*<PieChartSample data={this.state.pieData[2]}/>*/}
            {/*<PieChartSample data={this.state.pieData[3]}/>*/}
            <LinePlot data={this.state.linePLot}/>
            <hr/>
            <h1 className={'margin-top-50'}> Word Cloud of movie tags:</h1>
            <WordCloudSample/>
            <hr/>
            <h1 className={'margin-top-50'}> Distribution of different Genres throughout years:</h1>
            <GroupBarChart data={this.state.groupBarData}/>

        </div>
        )
    }
}

export default App;
