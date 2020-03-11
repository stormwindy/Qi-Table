import React from 'react'
import Konva from 'konva';
import { Stage, Layer, Rect, Text, Transformer} from 'react-konva';
import Table from './Table'

//adapted from https://konvajs.org/docs/react/Transformer.html
class EditorBox extends React.Component{
    constructor(props){
        super(props);

        this.state = {selectedID: null};
    }

    render(){
        let bounds = {x: window.innerWidth/2, y: window.innerHeight/2};

        const positions = this.props.positions;

        return(
            //the border rect might get removed once CSS is implemented
            <div>
                <Stage width={bounds.x} height={bounds.y} 
                    onMouseDown = {e => {
                        if (e.target === e.target.getStage()) {
                            this.setState({selectedID: null});
                        }
                    }}
                >
                    <Layer>
                        <Rect x={0} y={0} width={bounds.x} height={bounds.y} stroke="black"
                            onClick = {(e) => {
                                this.setState({selectedID:null});
                            }}
                        />
                        {positions.map(({id,x,y,r}) => 
                            <Table id={id} x={x} y={y} r={r} bounds={bounds}
                                onChange={this.props.onChange}
                                onSelect={() => {this.setState({selectedID: id})}} 
                                selected={this.state.selectedID === id}
                                allPositions = {positions}
                            />
                        )}   
                    </Layer>
                </Stage>
            </div>
        )
    }
}

export default EditorBox
