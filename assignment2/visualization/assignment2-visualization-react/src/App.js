import React, {Component} from 'react';
import './App.css';

import {LeafletMap} from "./components/leaflet-map.component";

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
              <h2>Choropleth for taxi pickups</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'busy-areas'}/>
              <h2>Choropleth for average passenger</h2>
              <LeafletMap ip={this.state.localIP} data={this.state.heat_map_pickups} api={'average-passenger-counts'}/>
          </div>
      );
  }
}

export default App;
