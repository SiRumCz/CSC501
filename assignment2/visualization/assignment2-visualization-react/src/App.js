import React, {Component} from 'react';
import './App.css';


import {LeafletMap} from "./components/leaflet-map.component";
import {LinePlot} from "./components/LinePlot.component";
import {BarChartSample} from "./components/BarChart.component";

import Video1 from './videos/taxi_nyc_0.2_60_11.mp4';
import Video2 from './videos/taxi_nyc_0.2_60_12.mp4';
import Video3 from './videos/taxi_nyc_0.2_60_13.mp4';

class App extends Component{

    constructor(props){
        super(props);

        this.state = {
            localIP: 'http://127.0.0.1:5000',
        }
    }


  render() {
      return (
          <div className="App">
              <h2 className={'margin-top-100'}>Choropleth for taxi pickups</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'busy-areas'}/>
              <h2 className={'margin-top-100'}>Choropleth for average passenger</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'average-passenger-counts'}/>
              <hr/>
              <h2 className={'margin-top-100'}>Total amount of traffic(arrivals + departures) are shown as video during time</h2>
              <h4>zoom one:</h4>
              <video height={400} loop  autoPlay src={Video1}  />
              <h4>zoom two:</h4>
              <video height={400}  loop autoPlay src={Video2}  />
              <h4>zoom three:</h4>
              <video height={400} loop  autoPlay src={Video3}  />
              <hr/>
              <h2 className={'margin-top-100'}>Heat Maps done with Jupyter Notebook:</h2>
              <h4>Heat Map one:</h4>
              <img src={require("./pictures/H1.png")} alt=""/>
              <h4>Heat Map two:</h4>
              <img src={require("./pictures/H2.png")} alt=""/>
              <h4>Heat Map three:</h4>
              <img src={require("./pictures/H3.png")} alt=""/>
              <hr/>
              <h2 className={'margin-top-100'}>Choropleth for average passenger</h2>
              <LinePlot ip={this.state.localIP}/>
              <h2 className={'margin-top-100'}>Bar chart for usage of different payment method</h2>
              <BarChartSample ip={this.state.localIP}/>
              <div className={'margin-bot-50'} ></div>
          </div>
      );
  }
}

export default App;
