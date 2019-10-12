import React, {Component} from 'react'
import Choropleth from 'react-leaflet-choropleth'

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
        const heat_map = [
            {
                "id": 0,
                "value": 64
            },
            {
                "id": 1,
                "value": 98
            },
            {
                "id": 2,
                "value": 23
            },
            {
                "id": 3,
                "value": 65
            },
            {
                "id": 4,
                "value": 32
            },
            {
                "id": 5,
                "value": 41
            },
            {
                "id": 6,
                "value": 96
            },
            {
                "id": 7,
                "value": 20
            },
            {
                "id": 8,
                "value": 69
            },
            {
                "id": 9,
                "value": 77
            },
            {
                "id": 10,
                "value": 13
            },
            {
                "id": 11,
                "value": 1
            },
            {
                "id": 12,
                "value": 34
            },
            {
                "id": 13,
                "value": 91
            },
            {
                "id": 14,
                "value": 83
            },
            {
                "id": 15,
                "value": 17
            },
            {
                "id": 16,
                "value": 83
            },
            {
                "id": 17,
                "value": 67
            },
            {
                "id": 18,
                "value": 96
            },
            {
                "id": 19,
                "value": 17
            },
            {
                "id": 20,
                "value": 16
            },
            {
                "id": 21,
                "value": 95
            },
            {
                "id": 22,
                "value": 74
            },
            {
                "id": 23,
                "value": 11
            },
            {
                "id": 24,
                "value": 85
            },
            {
                "id": 25,
                "value": 81
            },
            {
                "id": 26,
                "value": 13
            },
            {
                "id": 27,
                "value": 59
            },
            {
                "id": 28,
                "value": 33
            },
            {
                "id": 29,
                "value": 3
            },
            {
                "id": 30,
                "value": 18
            },
            {
                "id": 31,
                "value": 52
            },
            {
                "id": 32,
                "value": 58
            },
            {
                "id": 33,
                "value": 50
            },
            {
                "id": 34,
                "value": 88
            },
            {
                "id": 35,
                "value": 97
            },
            {
                "id": 36,
                "value": 24
            },
            {
                "id": 37,
                "value": 91
            },
            {
                "id": 38,
                "value": 65
            },
            {
                "id": 39,
                "value": 69
            },
            {
                "id": 40,
                "value": 53
            },
            {
                "id": 41,
                "value": 28
            },
            {
                "id": 42,
                "value": 91
            },
            {
                "id": 43,
                "value": 38
            },
            {
                "id": 44,
                "value": 16
            },
            {
                "id": 45,
                "value": 29
            },
            {
                "id": 46,
                "value": 43
            },
            {
                "id": 47,
                "value": 33
            },
            {
                "id": 48,
                "value": 85
            },
            {
                "id": 49,
                "value": 38
            },
            {
                "id": 50,
                "value": 51
            },
            {
                "id": 51,
                "value": 32
            },
            {
                "id": 52,
                "value": 83
            },
            {
                "id": 53,
                "value": 80
            },
            {
                "id": 54,
                "value": 22
            },
            {
                "id": 55,
                "value": 12
            },
            {
                "id": 56,
                "value": 10
            },
            {
                "id": 57,
                "value": 20
            },
            {
                "id": 58,
                "value": 83
            },
            {
                "id": 59,
                "value": 34
            },
            {
                "id": 60,
                "value": 74
            },
            {
                "id": 61,
                "value": 17
            },
            {
                "id": 62,
                "value": 73
            },
            {
                "id": 63,
                "value": 54
            },
            {
                "id": 64,
                "value": 91
            },
            {
                "id": 65,
                "value": 62
            },
            {
                "id": 66,
                "value": 21
            },
            {
                "id": 67,
                "value": 78
            },
            {
                "id": 68,
                "value": 39
            },
            {
                "id": 69,
                "value": 58
            },
            {
                "id": 70,
                "value": 37
            },
            {
                "id": 71,
                "value": 8
            },
            {
                "id": 72,
                "value": 99
            },
            {
                "id": 73,
                "value": 85
            },
            {
                "id": 74,
                "value": 69
            },
            {
                "id": 75,
                "value": 42
            },
            {
                "id": 76,
                "value": 28
            },
            {
                "id": 77,
                "value": 97
            },
            {
                "id": 78,
                "value": 72
            },
            {
                "id": 79,
                "value": 12
            },
            {
                "id": 80,
                "value": 33
            },
            {
                "id": 81,
                "value": 55
            },
            {
                "id": 82,
                "value": 75
            },
            {
                "id": 83,
                "value": 93
            },
            {
                "id": 84,
                "value": 55
            },
            {
                "id": 85,
                "value": 66
            },
            {
                "id": 86,
                "value": 45
            },
            {
                "id": 87,
                "value": 14
            },
            {
                "id": 88,
                "value": 27
            },
            {
                "id": 89,
                "value": 49
            },
            {
                "id": 90,
                "value": 28
            },
            {
                "id": 91,
                "value": 53
            },
            {
                "id": 92,
                "value": 3
            },
            {
                "id": 93,
                "value": 87
            },
            {
                "id": 94,
                "value": 75
            },
            {
                "id": 95,
                "value": 26
            },
            {
                "id": 96,
                "value": 44
            },
            {
                "id": 97,
                "value": 90
            },
            {
                "id": 98,
                "value": 69
            },
            {
                "id": 99,
                "value": 63
            },
            {
                "id": 100,
                "value": 92
            },
            {
                "id": 101,
                "value": 30
            },
            {
                "id": 102,
                "value": 4
            },
            {
                "id": 103,
                "value": 76
            },
            {
                "id": 104,
                "value": 48
            },
            {
                "id": 105,
                "value": 67
            },
            {
                "id": 106,
                "value": 64
            },
            {
                "id": 107,
                "value": 80
            },
            {
                "id": 108,
                "value": 50
            },
            {
                "id": 109,
                "value": 91
            },
            {
                "id": 110,
                "value": 9
            },
            {
                "id": 111,
                "value": 88
            },
            {
                "id": 112,
                "value": 76
            },
            {
                "id": 113,
                "value": 50
            },
            {
                "id": 114,
                "value": 1
            },
            {
                "id": 115,
                "value": 27
            },
            {
                "id": 116,
                "value": 48
            },
            {
                "id": 117,
                "value": 30
            },
            {
                "id": 118,
                "value": 29
            },
            {
                "id": 119,
                "value": 96
            },
            {
                "id": 120,
                "value": 25
            },
            {
                "id": 121,
                "value": 67
            },
            {
                "id": 122,
                "value": 81
            },
            {
                "id": 123,
                "value": 82
            },
            {
                "id": 124,
                "value": 68
            },
            {
                "id": 125,
                "value": 36
            },
            {
                "id": 126,
                "value": 59
            },
            {
                "id": 127,
                "value": 86
            },
            {
                "id": 128,
                "value": 89
            },
            {
                "id": 129,
                "value": 5
            },
            {
                "id": 130,
                "value": 37
            },
            {
                "id": 131,
                "value": 27
            },
            {
                "id": 132,
                "value": 33
            },
            {
                "id": 133,
                "value": 63
            },
            {
                "id": 134,
                "value": 9
            },
            {
                "id": 135,
                "value": 25
            },
            {
                "id": 136,
                "value": 16
            },
            {
                "id": 137,
                "value": 6
            },
            {
                "id": 138,
                "value": 99
            },
            {
                "id": 139,
                "value": 98
            },
            {
                "id": 140,
                "value": 48
            },
            {
                "id": 141,
                "value": 35
            },
            {
                "id": 142,
                "value": 38
            },
            {
                "id": 143,
                "value": 2
            },
            {
                "id": 144,
                "value": 93
            },
            {
                "id": 145,
                "value": 5
            },
            {
                "id": 146,
                "value": 18
            },
            {
                "id": 147,
                "value": 15
            },
            {
                "id": 148,
                "value": 30
            },
            {
                "id": 149,
                "value": 51
            },
            {
                "id": 150,
                "value": 30
            },
            {
                "id": 151,
                "value": 54
            },
            {
                "id": 152,
                "value": 17
            },
            {
                "id": 153,
                "value": 91
            },
            {
                "id": 154,
                "value": 81
            },
            {
                "id": 155,
                "value": 91
            },
            {
                "id": 156,
                "value": 6
            },
            {
                "id": 157,
                "value": 69
            },
            {
                "id": 158,
                "value": 85
            },
            {
                "id": 159,
                "value": 5
            },
            {
                "id": 160,
                "value": 19
            },
            {
                "id": 161,
                "value": 26
            },
            {
                "id": 162,
                "value": 80
            },
            {
                "id": 163,
                "value": 5
            },
            {
                "id": 164,
                "value": 23
            },
            {
                "id": 165,
                "value": 55
            },
            {
                "id": 166,
                "value": 57
            },
            {
                "id": 167,
                "value": 48
            },
            {
                "id": 168,
                "value": 58
            },
            {
                "id": 169,
                "value": 59
            },
            {
                "id": 170,
                "value": 71
            },
            {
                "id": 171,
                "value": 28
            },
            {
                "id": 172,
                "value": 60
            },
            {
                "id": 173,
                "value": 11
            },
            {
                "id": 174,
                "value": 2
            },
            {
                "id": 175,
                "value": 55
            },
            {
                "id": 176,
                "value": 7
            },
            {
                "id": 177,
                "value": 13
            },
            {
                "id": 178,
                "value": 59
            },
            {
                "id": 179,
                "value": 24
            },
            {
                "id": 180,
                "value": 67
            },
            {
                "id": 181,
                "value": 95
            },
            {
                "id": 182,
                "value": 86
            },
            {
                "id": 183,
                "value": 33
            },
            {
                "id": 184,
                "value": 55
            },
            {
                "id": 185,
                "value": 83
            },
            {
                "id": 186,
                "value": 14
            },
            {
                "id": 187,
                "value": 28
            },
            {
                "id": 188,
                "value": 70
            },
            {
                "id": 189,
                "value": 92
            },
            {
                "id": 190,
                "value": 9
            },
            {
                "id": 191,
                "value": 71
            },
            {
                "id": 192,
                "value": 85
            },
            {
                "id": 193,
                "value": 83
            },
            {
                "id": 194,
                "value": 51
            },
            {
                "id": 195,
                "value": 84
            },
            {
                "id": 196,
                "value": 48
            },
            {
                "id": 197,
                "value": 67
            },
            {
                "id": 198,
                "value": 53
            },
            {
                "id": 199,
                "value": 29
            },
            {
                "id": 200,
                "value": 14
            },
            {
                "id": 201,
                "value": 3
            },
            {
                "id": 202,
                "value": 17
            },
            {
                "id": 203,
                "value": 55
            },
            {
                "id": 204,
                "value": 50
            },
            {
                "id": 205,
                "value": 97
            },
            {
                "id": 206,
                "value": 81
            },
            {
                "id": 207,
                "value": 37
            },
            {
                "id": 208,
                "value": 94
            },
            {
                "id": 209,
                "value": 89
            },
            {
                "id": 210,
                "value": 73
            },
            {
                "id": 211,
                "value": 67
            },
            {
                "id": 212,
                "value": 92
            },
            {
                "id": 213,
                "value": 56
            },
            {
                "id": 214,
                "value": 3
            },
            {
                "id": 215,
                "value": 10
            },
            {
                "id": 216,
                "value": 38
            },
            {
                "id": 217,
                "value": 19
            },
            {
                "id": 218,
                "value": 73
            },
            {
                "id": 219,
                "value": 8
            },
            {
                "id": 220,
                "value": 96
            },
            {
                "id": 221,
                "value": 25
            },
            {
                "id": 222,
                "value": 68
            },
            {
                "id": 223,
                "value": 45
            },
            {
                "id": 224,
                "value": 33
            },
            {
                "id": 225,
                "value": 33
            },
            {
                "id": 226,
                "value": 51
            },
            {
                "id": 227,
                "value": 51
            },
            {
                "id": 228,
                "value": 34
            },
            {
                "id": 229,
                "value": 61
            },
            {
                "id": 230,
                "value": 70
            },
            {
                "id": 231,
                "value": 73
            },
            {
                "id": 232,
                "value": 74
            },
            {
                "id": 233,
                "value": 62
            },
            {
                "id": 234,
                "value": 31
            },
            {
                "id": 235,
                "value": 13
            },
            {
                "id": 236,
                "value": 56
            },
            {
                "id": 237,
                "value": 38
            },
            {
                "id": 238,
                "value": 6
            },
            {
                "id": 239,
                "value": 55
            },
            {
                "id": 240,
                "value": 8
            },
            {
                "id": 241,
                "value": 1
            },
            {
                "id": 242,
                "value": 53
            },
            {
                "id": 243,
                "value": 43
            },
            {
                "id": 244,
                "value": 66
            },
            {
                "id": 245,
                "value": 73
            },
            {
                "id": 246,
                "value": 95
            },
            {
                "id": 247,
                "value": 3
            },
            {
                "id": 248,
                "value": 69
            },
            {
                "id": 249,
                "value": 16
            },
            {
                "id": 250,
                "value": 29
            },
            {
                "id": 251,
                "value": 54
            },
            {
                "id": 252,
                "value": 64
            },
            {
                "id": 253,
                "value": 38
            },
            {
                "id": 254,
                "value": 24
            },
            {
                "id": 255,
                "value": 34
            },
            {
                "id": 256,
                "value": 22
            },
            {
                "id": 257,
                "value": 61
            },
            {
                "id": 258,
                "value": 60
            },
            {
                "id": 259,
                "value": 56
            },
            {
                "id": 260,
                "value": 24
            },
            {
                "id": 261,
                "value": 67
            },
            {
                "id": 262,
                "value": 100
            },
            {
                "id": 263,
                "value": 100
            }
        ]
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
                <Choropleth
                    data={nyc_geojson}
                    valueProperty={(feature) => {
                        for(let i=0; i < heat_map.length; i++){
                        if(heat_map[i].id === feature.properties.objectid){
                            return heat_map[i].value;
                        }
                        }
                    }}
                    scale={['#ffeda0', '#f03b20']}
                    steps={7}
                    mode='e'
                    style={style}
                    onEachFeature={(feature, layer) => layer.bindPopup(feature.properties.label)}
                    ref={(el) => this.choropleth = el.leafletElement}
                />
            </Map>
        );

    }
}
