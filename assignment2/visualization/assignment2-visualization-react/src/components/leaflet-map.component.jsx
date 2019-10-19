import React, {Component} from 'react'
import Choropleth from 'react-leaflet-choropleth'
import Legend from './legend.component'

import { Map, TileLayer } from 'react-leaflet'

import './LeafletMap.style.css';
import 'leaflet/dist/leaflet.css';
import {nyc_geojson} from './NYC-GeoJSON';

export class LeafletMap extends Component {
    constructor(props){
        super(props);
        this.state = {
            lat: 40.730610,
            lng: -73.935242,
            zoom: 11,
            data: [],
            max: 0,
            min: 1000000
        }
    }
    componentDidMount() {
        this.api_request(this.props.api)
    }
    api_request = (api) => {

        fetch(`${this.props.ip}/${api}`)
            .then(result => (result.json()))
            .then(data => {
                let max = 0, min = 0;
                data = data.map(district => {
                    if(district.avgPassengers) {
                        if(district.avgPassengers > max) {
                            max = district.avgPassengers;
                        }
                        if(district.avgPassengers < min) {
                            min = district.avgPassengers;
                        }
                    }
                    if(district.pickups) {
                        if(district.pickups > max) {
                            max = district.pickups;
                        }
                        if(district.pickups < min) {
                            min = district.pickups;
                        }
                    }
                    return {
                        id: district.areaId, value: district.pickups || (district.avgPassengers*district.avgPassengers)
                    }
                })
                this.setState({data, max, min})
            })
    }

    render(){

        const position = [this.state.lat, this.state.lng];
        const style = {
            fillColor: '#F28F3B',
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.5
        }
        return (
            <Map center={position} zoom={this.state.zoom}>
                <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
                />
                {(this.state.data.length > 0)&&(
                    <div>
                    <Choropleth
                    data={nyc_geojson}
                    valueProperty={(feature) => {
                    for (let i = 0; i < this.state.data.length; i++) {
                        if (this.state.data[i].id === feature.properties.objectid) {
                            return this.state.data[i].value*100;
                        }
                    }
                }}
                    scale={['#FFEDA0', '#800026']}
                    steps={8}
                    mode='e'
                    style={style}
                    onEachFeature={(feature, layer) => layer.bindPopup('Zone: ' + feature.properties.zone + "\n ID: " + feature.properties.objectid)}
                    ref={(el) => this.choropleth = el.leafletElement}
                    />
                        <Legend steps={8} min={this.state.min} max={this.state.max}/>
                    </div>
                )
                }
            </Map>
        );

    }
}
