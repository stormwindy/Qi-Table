import React from 'react';
import ReactDOM from 'react-dom';
import Konva from 'konva';
import { Stage, Layer, Rect, Text, Transformer} from 'react-konva';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

// var element = React.createElement('h1', { className: 'greeting' }, 'Hello, world!');

class MainView extends React.Component{  
    constructor(props){
        super(props);
        this.state = {
            view: "select"
        }
    }

    render(){
        let view;
        if (this.state.view === "select") view = <SelectionView />;
        if (this.state.view === "editor") view = <EditorView />;
        if (this.state.view === "settings") view = <SettingsView />;

        return (
            <div>
                <ul>
                    <li><button onClick={() => this.setState({view: "select"})}>Selection view</button></li>
                    <li><button onClick={() => this.setState({view: "editor"})}>Editor view</button></li>
                    <li><button onClick={() => this.setState({view: "settings"})}>Settings view</button></li>
                </ul>
                {view}
            </div>
        );
    }
}

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

class EditorView extends React.Component{

    constructor(props){
        super(props);

        this.state = {name: "New Layout", positions: [{id:0, x:0, y:0, r:0}]};
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
            positions: positions.concat([{id: highestID+1, x:0, y:0, r:0}])
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
                <h1>This is the editor view. Create a new layout.</h1>
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

class SettingsView extends React.Component{
    render(){
        return(
            <div><h1>This is the settings view. Change settings here.</h1></div>
        );
    }
}



class PositionForm extends React.Component{
    constructor(props){
        super(props);

    }

    render() {
        return (
          <form>
            <label>
              x:
              <input type="number" name='x' value={this.props.x} 
              onChange={(e) => this.props.inputHandleChange(e, this.props.id)} />
            </label>
            <label>
              y:
              <input type="number" name='y' value={this.props.y} 
              onChange={(e) => this.props.inputHandleChange(e, this.props.id)} />
            </label>
            <label>
              rotation:
              <input type="number" name='r' value={this.props.r}
              onChange={(e) => this.props.inputHandleChange(e, this.props.id)} />
            </label>
            <button onClick={(e) => this.props.handleDelete(e, this.props.id)}>Delete</button>
          </form>
        );
    }
}

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
                            <Table id={id} x={x} y={y} bounds={bounds}
                                onChange={this.props.onChange}
                                onSelect={() => {this.setState({selectedID: id})}} 
                                selected={this.state.selectedID === id}
                            />
                        )}   
                    </Layer>
                </Stage>
            </div>
        )
    }
}

class Table extends React.Component{
    constructor(props){
        super(props)

        this.shapeRef = React.createRef();
        this.trRef = React.createRef();
    }

    componentDidMount() {
        if (this.props.selected) {
            // we need to attach transformer manually
            this.trRef.current.setNode(this.shapeRef.current);
            this.trRef.current.getLayer().batchDraw();
        }

    }

    componentDidUpdate(){
        if (this.props.selected) {
            // we need to attach transformer manually
            this.trRef.current.setNode(this.shapeRef.current);
            this.trRef.current.getLayer().batchDraw();
        }
    }

    dragBoundFunc(pos, bounds, dimensions){
        let newX = pos.x;
        let newY = pos.y;

        if (pos.x>bounds.x-dimensions.x) newX = bounds.x-dimensions.x;
        if (pos.x<0) newX = 0;

        if (pos.y>bounds.y-dimensions.y) newY = bounds.y-dimensions.y;
        if (pos.y<0) newY = 0;

        return {
            x : newX,
            y: newY
        }
    }

    render(){
        const width = 70;
        const height = 100;

        return(
            <React.Fragment>
                <Rect x={this.props.x} y={this.props.y} rotation={this.props.r}
                    width={width} height={height} fill="blue" shadowBlur={5} draggable={true} 
                    ref={this.shapeRef}
                    dragBoundFunc = {(pos) => this.dragBoundFunc(pos, this.props.bounds, {x: width, y:height})}
                    onDragEnd={(e) => this.props.onChange(this.props.id, e.target.x(), e.target.y(), this.props.r)}
                    onClick={this.props.onSelect}
                    onTransformEnd={(e)=> {
                        const node = this.shapeRef.current;
                        this.props.onChange(this.props.id, this.props.x, this.props.y, e.target.rotation())
                    }}
                />
                {this.props.selected && <Transformer ref={this.trRef} resizeEnabled={false}/>}
            </React.Fragment>
        )
    }
}

ReactDOM.render(<MainView />, document.getElementById('root'));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
