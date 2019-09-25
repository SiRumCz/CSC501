import React, {Component} from  'react';

import WordCloud from "react-d3-cloud";


import './WordCloud.style.css'
export class WordCloudSample extends Component {

    constructor(props){
        super(props);

        this.state = {
            tags: []
        }

    }

    componentDidMount() {

        fetch(`${this.props.ip}/tags-wordcloud`)
            .then(result => (result.json()))
            .then(data => {
                let tags = data.map(tag => ({text: tag.tag, value: Math.floor(tag.count/30)}))
                this.setState({tags: tags})
            })

    }





    render() {
        const fontSizeMapper = word => word.value+5 ;
        const rotate = word => {
            const x = Math.round(Math.random() * 5) + 1;
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
            this.state.tags &&
            (<div id={'word-cloud'}>
            <WordCloud

                width={1400}
                height={1150}
                data={this.state.tags}
                fontSizeMapper={fontSizeMapper}
                rotate={rotate}
                padding={10}
            />
            </div>)
        );
    }
}