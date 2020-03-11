import React from 'react'

import { Stage, Layer, Rect, Text, Transformer} from 'react-konva';
import { TABLE_HEIGHT, TABLE_WIDTH } from '../constants'
import {resolveCollision, getVertices, getEdges} from '../lib/collision.js';


class Table extends React.Component{
    constructor(props){
        super(props)

        this.shapeRef = React.createRef();
        this.trRef = React.createRef();
    }

    componentDidMount() {
        
        //console.log(getVertices(this.props.x, this.props.y, TABLE_WIDTH, TABLE_HEIGHT, this.props.r))

        if (this.props.selected) {
            // we need to attach transformer manually
            this.trRef.current.setNode(this.shapeRef.current);
            this.trRef.current.getLayer().batchDraw();
        }

    }

    componentDidUpdate(){
        //let vs = getVertices(this.props.x, this.props.y, TABLE_WIDTH, TABLE_HEIGHT, this.props.r);
        //console.log(vs);
        //console.log(getEdges(vs));

        if (this.props.selected) {
            // we need to attach transformer manually
            this.trRef.current.setNode(this.shapeRef.current);
            this.trRef.current.getLayer().batchDraw();
        }
    }
    //TODO - FINISH THIS
    /*
    dragBoundFunc(pos, bounds, dimensions){
        let newX = pos.x;
        let newY = pos.y;

        let allTables = this.props.allPositions;
        //distance at which we may want to check for collisions
        let collisionDistanceSquared = Math.pow(TABLE_WIDTH, 2) + Math.pow(TABLE_HEIGHT, 2);
        allTables.forEach(t =>{
            //check if t is close enough to warrant more precise checking
            let distanceSquared = Math.pow(t.x-newX, 2) + Math.pow(t.y-newY, 2);
            if (t.id !== this.props.id && distanceSquared<collisionDistanceSquared){
                let collisionPushVector = resolveCollision({x: newX, y: newY}, {x: t.x, y: t.y},
                                            getVertices(newX, newY, TABLE_WIDTH, TABLE_HEIGHT, this.props.r),
                                            getVertices(t.x, t.y, TABLE_WIDTH, TABLE_HEIGHT, t.r));
                if (collisionPushVector.x != 0 && collisionPushVector.y != 0)
                    alert("Collision Push Vector: [" + collisionPushVector.x + ", " + collisionPushVector.y + "]");
                newX += collisionPushVector.x;
                newY += collisionPushVector.y;
            }
        })
        
        

        if (pos.x>bounds.x-dimensions.x) newX = bounds.x-dimensions.x;
        if (pos.x<0) newX = 0;

        if (pos.y>bounds.y-dimensions.y) newY = bounds.y-dimensions.y;
        if (pos.y<0) newY = 0;
        

        return {
            x: newX,
            y: newY
        }
        
    }
*/
    dragBoundFunc(pos, bounds, dimensions){
        return pos;
    }

    handleChange(x, y, r){
        let allTables = this.props.allPositions;
        //distance at which we may want to check for collisions
        let collisionDistanceSquared = Math.pow(TABLE_WIDTH, 2) + Math.pow(TABLE_HEIGHT, 2);
        allTables.forEach(t =>{
            //check if t is close enough to warrant more precise checking
            let distanceSquared = Math.pow(t.x-x, 2) + Math.pow(t.y-y, 2);
            if (t.id !== this.props.id && distanceSquared<collisionDistanceSquared){
                let collisionPushVector = resolveCollision({x: x, y: y}, {x: t.x, y: t.y},
                                            getVertices(x, y, TABLE_WIDTH, TABLE_HEIGHT, this.props.r),
                                            getVertices(t.x, t.y, TABLE_WIDTH, TABLE_HEIGHT, t.r));
                //if (collisionPushVector.x != 0 && collisionPushVector.y != 0)
                    console.log("Collision Push Vector: [" + collisionPushVector.x + ", " + collisionPushVector.y + "]");
                x += collisionPushVector.x;
                y += collisionPushVector.y;
            }
        });

        this.props.onChange(this.props.id, x, y, r);
    }

    render(){

        return(
            <React.Fragment>
                <Rect x={this.props.x} y={this.props.y} rotation={this.props.r} offsetX={TABLE_WIDTH/2} offsetY={TABLE_HEIGHT/2}
                    width={TABLE_WIDTH} height={TABLE_HEIGHT} fill="blue" draggable={true} stroke="black"
                    ref={this.shapeRef}
                    dragBoundFunc = {(pos) => this.dragBoundFunc(pos, this.props.bounds, {x: TABLE_WIDTH, y:TABLE_HEIGHT})}
                    onDragEnd={(e) => this.handleChange(e.target.x(), e.target.y(), this.props.r)}
                    onClick={this.props.onSelect}
                    onTransformEnd={(e)=> {
                        const node = this.shapeRef.current;
                        this.handleChange(this.props.x, this.props.y, e.target.rotation())
                    }}
                />
                {this.props.selected && <Transformer ref={this.trRef} resizeEnabled={false}/>}
            </React.Fragment>
        )
    }
}

export default Table
