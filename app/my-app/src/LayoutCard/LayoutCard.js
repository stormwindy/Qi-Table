import React from 'react'

class LayoutCard extends React.Component{
    constructor(props){
        super(props);
        this.handleClick = this.handleClick.bind(this)
    }
    handleClick(e){
        fetch('http://127.0.0.1:5000/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({id: this.props.id})
            //body: "aaaaaa"
        }).then(res => res.json())
        .then(
           (result) => alert(result.text),
           (error) => alert('Error')
        )
    }

    render(){
        const positions = this.props.positions;

        return(
            <div>
            <p>{this.props.name}</p>
            <p>Positions:</p>
            <ul>
                {positions.map((p) => 
                <li>x: {p.x} y: {p.y} rotation: {p.rotation} </li>)}
            </ul>
            <button onClick={this.handleClick}>Choose this layout!</button>
            </div>
        )
    }
}

export default LayoutCard
