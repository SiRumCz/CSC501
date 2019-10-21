import React, {Component} from 'react';
import './App.css';

import {LeafletMap} from "./components/leaflet-map.component";
import {LinePlot} from "./components/LinePlot.component";
import {BarChartSample} from "./components/BarChart.component";
import {LinePlotTrends} from "./components/LinePlot-payment-trends.component";
import {LinePlotInterval} from "./components/LinePlot-interval-tree.component";
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
              <h2 className={'margin-top-100'}>Choropleth for taxi pickups zip-file from Connex</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'busy-areas'}/>
              <h2 className={'margin-top-100'}>Choropleth for taxi pickups in 2018 after processing data</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'busy-areas-2018'}/>
              <h2 className={'margin-top-100'}>Choropleth for average passenger zip-file from Connex</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'average-passenger-counts'}/>
              <h2 className={'margin-top-100'}>Choropleth for average passenger in 2018 after processing data</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'average-passenger-counts-2018'}/>
              <hr/>
              <h2 className={'margin-top-100'}>Total amount of traffic(arrivals + departures) are shown as video during time</h2>
              <h4>zoom one:</h4>
              <video height={400} playsInline  muted loop controls  autoPlay src={Video1}  />
              <h4>zoom two:</h4>
              <video height={400}  playsInline  muted loop controls autoPlay src={Video2}  />
              <h4>zoom three:</h4>
              <video height={400} playsInline  muted loop controls autoPlay src={Video3}  />
              <hr/>
              <h2 className={'margin-top-100'}>Heat Maps done with Jupyter Notebook:span</h2>
              <p>(html files are included in separate folder for these images)</p>
              <h4>Heat Map one:</h4>
              <img src={require("./pictures/H1.png")} alt=""/>
              <h4>Heat Map two:</h4>
              <img src={require("./pictures/H2.png")} alt=""/>
              <h4>Heat Map three:</h4>
              <img src={require("./pictures/H3.png")} alt=""/>
              <hr/>
              <h2 className={'margin-top-100'}>Pickups in different hours of the day</h2>
              <LinePlot ip={this.state.localIP} />
              <h2 className={'margin-top-100'}>Bar chart for usage of different payment method zip-file Connex</h2>
              <BarChartSample api={'payment-trend-usage'} ip={this.state.localIP}/>
              <h2 className={'margin-top-100'}>Bar chart for usage of different payment method in 2018 after processing data</h2>
              <BarChartSample api={'payment-trend-usage-2018'} ip={this.state.localIP}/>
              <h2 className={'margin-top-100'}>Different payment trends in 2018</h2>
              <LinePlotTrends ip={this.state.localIP}/>
              <h2 className={'margin-top-100'}>Interval Trees</h2>
              <LinePlotInterval api={'interval-tree-passengers'} ip={this.state.localIP}/>
              <h2 className={'margin-top-100'}>Interval Trees for 2018</h2>
              <LinePlotInterval api={'interval-tree-passengers-2018'} ip={this.state.localIP}/>

              <div className={'margin-bot-50'} ></div>

          </div>
      );
  }
}

export default App;
