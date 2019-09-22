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
            genres: [
                'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'FilmNoir', 'Horror', 'Musical', 'Mystery', 'Romance', 'SciFi', 'Thriller', 'War', 'Western'
            ],
            localIP: 'http://127.0.0.1:5000'
        }
    }

    render () {
        return(
        <div className="App">
            <h1 className={'margin-top-50'}> Bar chart for movies by ranking:</h1>
            <div className={'margin-top-50'}>
            <BarChartSample ip={this.state.localIP} />
            </div>
            <hr/>
            <h1 className={'margin-top-50'}> Different ratings in different genres across past several years:</h1>
            <LinePlot ip={this.state.localIP}  genres={this.state.genres}/>
            <hr/>
            <h1 className={'margin-top-50'}> Word Cloud of movie tags:</h1>
            <WordCloudSample ip={this.state.localIP}/>
            <hr/>
            <h1 className={'margin-top-50'}> Distribution of different Genres throughout years:</h1>
            <GroupBarChart ip={this.state.localIP} genres={this.state.genres}/>

        </div>
        )
    }
}

export default App;
