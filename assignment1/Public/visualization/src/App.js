import React from 'react';
import './App.css';

import { BarChart } from './components/BarChart-component';

function App() {
  return (
    <div className="App">
       <h1> This is going to be an awesome visualization</h1>
        <p>And this is an example:</p>
        <BarChart></BarChart>
    </div>
  );
}

export default App;
