import React from 'react'

import PositionForm from '../PositionForm/PositionForm'
import EditorBox from './EditorBox'

import { TABLE_WIDTH, TABLE_HEIGHT } from '../constants'


class EditorView extends React.Component{

    constructor(props){
        super(props);

        this.state = {name: "New Layout", positions: [{id:0, x: TABLE_WIDTH, y:TABLE_HEIGHT, r:0}]};
    }

    inputHandleChange(e, rowID){
        let positions = this.state.positions;


        for (let i=0; i<positions.length; i++){
            if (positions[i].id === rowID){
                if (e.target.name==='x') positions[i].x=e.target.value;
                if (e.target.name==='y') positions[i].y=e.target.value;
                if (e.target.name==='r') positions[i].r=e.target.value;
            }
        }

        this.setState({positions: positions});
    }

    handleDelete(e, rowID){
        e.preventDefault();
        let positions = this.state.positions;

        for (let i=0; i<positions.length; i++){
            if (positions[i].id === rowID){
                positions.splice(i, 1);
            }
        }

        this.setState({positions: positions});
    }

    onChange(id, x, y, r){
        let positions = this.state.positions;

        //normalize r to <0,360>
        if (r<360) r = 360+r%360
        if (r>=360) r = r%360;
        
        for (let i=0; i<positions.length; i++){
            if (positions[i].id === id){
                positions[i].x = x;
                positions[i].y = y;
                positions[i].r = r;
            }
        }

        this.setState({positions: positions});
    }

    handleAddPos(){
        const positions = this.state.positions;
        //get highest id
        let highestID = 0;

        positions.forEach(function({id,x,y,r}){
            if (id>=highestID) highestID = id; 
        })

        //update state
        this.setState({
            positions: positions.concat([{id: highestID+1, x:TABLE_WIDTH, y:TABLE_HEIGHT, r:0}])
        });
    }

    handleSubmit(){
        fetch('http://127.0.0.1:5000/addlayout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({name: this.state.name, positions: this.state.positions})
        }).then(res => res.json())
        .then(
           (result) => alert(result.text),
           (error) => alert('Error')
        )
    }

    render(){

        const positions = this.state.positions;

        return(
            <div>
                <h1>Layout Editor</h1>
                <form>
                    <label>Layout Name:</label>
                    <input type="text" value={this.state.name} onChange={(e) => this.setState({name: e.target.value})} />
                </form>
                <ul>
                    {
                        positions.map(({id,x,y,r}) => 
                            <PositionForm id={id} x={x} y={y} r={r} 
                            inputHandleChange={this.inputHandleChange.bind(this)}
                            handleDelete={this.handleDelete.bind(this)} />
                        )
                    }
                </ul>
                <EditorBox positions = {this.state.positions} onChange = {this.onChange.bind(this)}/>
                <button onClick={this.handleAddPos.bind(this)}>More Positions</button>
                <button onClick={this.handleSubmit.bind(this)}>Submit Layout</button>
            </div>
        );
    }
}

export default EditorView
