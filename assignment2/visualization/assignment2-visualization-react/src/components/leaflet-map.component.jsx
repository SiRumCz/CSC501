import React, {Component} from 'react'
import Choropleth from 'react-leaflet-choropleth'

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
            data: []
        }
    }
    componentDidMount() {
        this.api_request(this.props.api)
    }
    api_request = (api) => {

        fetch(`${this.props.ip}/${api}`)
            .then(result => (result.json()))
            .then(data => {
                data = data.map(district => {
                    if(district.areaId){
                    return {
                        id: district.areaId, value: district.pickups || (district.avgPassengers*district.avgPassengers)
                    }
                    }
                })
                this.setState({data})
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
                    <Choropleth
                    data={nyc_geojson}
                    valueProperty={(feature) => {
                    for (let i = 0; i < this.state.data.length; i++) {
                        if (this.state.data[i].id === feature.properties.objectid) {
                            return this.state.data[i].value*100;
                        }
                    }
                }}
                    scale={['#ffeda0', '#f03b20']}
                    steps={7}
                    mode='e'
                    style={style}
                    onEachFeature={(feature, layer) => layer.bindPopup('Zone: ' + feature.properties.zone + "\n ID: " + feature.properties.objectid)}
                    ref={(el) => this.choropleth = el.leafletElement}
                    />
                )
                }
            </Map>
        );

    }
}
