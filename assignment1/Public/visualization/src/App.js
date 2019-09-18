import React, { Component } from 'react';
import './App.css';

import { BarChart } from './components/BarChart.component';

class App extends Component{

    constructor(props){
        super(props);

        this.state = {
            barData: [
                {title: 1, value: 243}, {title: 2, value: 187}, {title: 3, value: 234}, {title: 4, value: 104}, {title: 5, value: 83}
                ]
            ,
            width: 700,
            height: 300
        }
    }

    render () {
        return(
        <div className="App">
            <h1> Bar chart for movies by ranking:</h1>
            <BarChart width={700} height={300} data={this.state.barData}/>
        </div>
        )
    }
}

export default App;
