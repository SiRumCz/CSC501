import React, {Component} from  'react';

import WordCloud from "react-d3-cloud";

import tags from './tags';

import './WordCloud.style.css'
export class WordCloudSample extends Component {

    render() {
        const fontSizeMapper = word => word.value ;
        const rotate = word => {
            const x = Math.round(Math.round(Math.random() * 5) + 1);
            if( x === 5){
                return 90;
            }
            else if (x === 4) {
                return 45;
            }
            else if (x === 3) {
                return 0;
            }
            else if (x === 2) {
                return -45;
            }
            else if (x === 1) {
                return -90;
            }
            else {
                return 0;
            }
        };
        return (
            <div id={'word-cloud'}>
            <WordCloud

                width={1000}
                height={750}
                data={tags}
                fontSizeMapper={fontSizeMapper}
                rotate={rotate}
                padding={10}
            />
            </div>
        );
    }
}