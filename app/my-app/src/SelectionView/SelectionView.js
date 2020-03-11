import React from 'react';
import LayoutCard from '../LayoutCard/LayoutCard'


class SelectionView extends React.Component{
    constructor(props){
        super(props)

        this.state={loaded: false};
    }

    fetchLayouts(){

        let layouts;
        fetch('http://127.0.0.1:5000/getlayouts', /*{
            
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({name: this.state.name, positions: this.state.positions})
        }*/).then(res => res.json())
        .then(
           (result) => this.setState({loaded: true, layouts: result.layouts}),
           (error) => this.setState({loaded: true, error})
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
            layoutDisplay = (<ul>
                {layouts.map((l) => 
                <li><LayoutCard id = {l.id} name = {l.name} positions = {l.positions}/></li>)}
            </ul>);
        }

        return(
            <div>
                <h1>This is the selection view. Choose a layout.</h1>
                {layoutDisplay}
            </div>
        );
    }
}

export default SelectionView
