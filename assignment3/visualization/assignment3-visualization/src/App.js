import React, {Component} from 'react';
import './App.css';

import {Chord} from "./components/chord.diagram.component";
import {EdgeBundled} from "./components/edge_bundled.diagram.component";
import {NodeLink} from "./components/NodeLink.component";
import {AdjacencyMatrix} from "./components/adjacency_matrix.diagram.component";

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
                <h2 className={'margin-top-100'}>Chord diagram</h2>
                <Chord/>
                <h2 className={'margin-top-100'}>Edge Bundling diagram</h2>
                <EdgeBundled ip={this.state.localIP}/>
                <h2 className={'margin-top-100'}>Node-Link diagram</h2>
                <NodeLink/>
                <h2 className={'margin-top-100'}>Adjacency Matrix diagram</h2>
                <AdjacencyMatrix/>
                <div className={'margin-bottom-100'}></div>
            </div>
        );
    }
}

export default App;
