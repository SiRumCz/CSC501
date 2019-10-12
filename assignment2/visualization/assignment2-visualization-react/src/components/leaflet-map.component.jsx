import React, {Component} from 'react'

import { Map, TileLayer, GeoJSON } from 'react-leaflet'

import './LeafletMap.style.css';
import 'leaflet/dist/leaflet.css';

import {nyc_geojson} from './NYC-GeoJSON';

export class LeafletMap extends Component {
    constructor(props){
        super(props);
        this.state = {
            lat: 40.730610,
            lng: -73.935242,
            zoom: 12
        }
    }


    render(){

        const position = [this.state.lat, this.state.lng];
        return (
            <Map center={position} zoom={this.state.zoom}>
                <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
                />
                <GeoJSON key={'123#123'} data={nyc_geojson} />

            </Map>
        );

    }
}
