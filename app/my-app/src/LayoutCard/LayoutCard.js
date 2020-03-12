import React from 'react'
import classNames from 'classnames'

import './LayoutCard.css'

class LayoutCard extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            flipped: false
        }
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
        })
            .then(res => res.json())
            .then(result => alert(result.text))
            .catch(error => alert(error))
    }

    handleCardClick() {
        console.log(`flipped: ${this.state.flipped}`)
        this.setState({flipped: !this.state.flipped})
    }

    render(){
        const positions = this.props.positions;
        const obstacles = []


        const layoutClasses = classNames(
            'layoutcard',
            {'layoutcard--flipped': this.state.flipped}
        )

        return (
            <div
                className={layoutClasses}
                >
                    <div
                        className="layoutcard__front"
                        onClick={() => this.handleCardClick()}>
                    <div className="layoutcard__preview">

                    </div>
                    <div
                        className="layoutcard__info">
                        <strong>{this.props.name}</strong>
                        <span>{positions.length} tables, {obstacles.length} obstacles.</span>
                    </div>
                </div>
                <div className="layoutcard__back">
                    <a href="#" >edit</a>
                    <span>&nbsp;&bull;&nbsp;</span>
                    <a href="#" className="layoutcard__execute">execute</a>
                    <div
                        onClick={() => this.handleCardClick()}
                        class="layoutcard__flipback">&times;</div>
                </div>
            </div>
        )
            /*
        return(
            <div>
                <p>{this.props.name}</p>
                <p>Positions:</p>
                <ul>
                    {positions.map((p) => 
                    <li key={`${p.x}${p.y}${p.rotation}`}>x: {p.x} y: {p.y} rotation: {p.rotation} </li>)}
                </ul>
                <button onClick={this.handleClick}>Choose this layout!</button>
            </div>
        )*/
    }
}

export default LayoutCard
