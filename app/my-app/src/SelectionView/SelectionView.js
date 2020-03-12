import React from 'react';
import LayoutCard from '../LayoutCard/LayoutCard'

import './SelectionView.css'

class SelectionView extends React.Component{
    constructor(props){
        super(props)

        this.state={loaded: false};
    }

    fetchLayouts(){

        fetch('http://127.0.0.1:5000/getlayouts', /*{
            
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({name: this.state.name, positions: this.state.positions})
        }*/).then(res => res.json())
        .then(
            result => this.setState({loaded: true, layouts: result.layouts}))
        .catch(
           error => this.setState({loaded: true, error})
        )
    }

    componentDidMount(){
        this.fetchLayouts();
    }

    render(){
        const layouts = this.state.layouts;
        let layoutDisplay;

        if(!this.state.loaded){
            layoutDisplay = "Loading layouts";
        }
        else if(this.state.error){
            layoutDisplay = "Error: could not load layouts"
        }
        else {
            layoutDisplay = layouts.map(l => (
                <LayoutCard
                    id={l.id}
                    key={l.id}
                    name={l.name}
                    positions={l.positions}/>
            ))
        }

        return(
            <div>
                <h1>Available Layouts</h1>
                <div className="layouts__container">
                    {layoutDisplay}
                </div>
            </div>
        );
    }
}

export default SelectionView
