import React, {Component} from 'react'
import ChordDiagram from 'react-chord-diagram'


export class Chord extends Component {

    render() {
        const matrix = [
            [11975, 5871, 8916, 2868],
            [1951, 10048, 2060, 6171],
            [8010, 16145, 8090, 8045],
            [1013, 990, 940, 6907]
        ];
        return(
            <ChordDiagram
                width={800}
                height={800}
                disableHover = {true}
                disableRibbonHover = {false}
                matrix={matrix}
                componentId={1}
                groupLabels={['Black', 'Yellow', 'Brown', 'Orange']}
                groupColors={["#000000", "#FFDD89", "#957244", "#F26223"]}
            />
        )
    }
}
