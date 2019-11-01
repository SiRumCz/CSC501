import React from 'react';
import './App.css';

import {Chord} from "./components/chord.diagram.component";
import {EdgeBundled} from "./components/edge_bundled.diagram.component";
import {NodeLink} from "./components/NodeLink.component";

function App() {
    return (
        <div className="App">
            <h2 className={'margin-top-100'}>Chord diagram</h2>
            <Chord/>
            <EdgeBundled/>
            <NodeLink/>
            <div className={'margin-bottom-100'}></div>
        </div>
    );
}

export default App;
