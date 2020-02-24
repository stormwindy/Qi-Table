import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Konva from 'konva';
import { Stage, Layer, Rect, Circle} from 'react-konva';
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
        if (this.state.view === "demo") view = <DemoView />;

        return (
            <div>
                <ul>
                    <li><button onClick={() => this.setState({view: "select"})}>Selection view</button></li>
                    <li><button onClick={() => this.setState({view: "editor"})}>Editor view</button></li>
                    <li><button onClick={() => this.setState({view: "settings"})}>Settings view</button></li>
                    <li><button onClick={() => this.setState({view: "demo"})}>ROBOT MOVEMENT DEMO</button></li>
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



//Input line for test editor
//Based on Controlled Text Example from React website
//work in progress!!
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

class DemoView extends React.Component{
    constructor(props){
        super(props);
        this.state = ({x:-100, y:-100});
    }

    onMouseDown(e, bounds){
        let stage = e.target.getStage();
        let pos = stage.getPointerPosition();
        let x = (pos.x/(bounds.x*2))*1920
        let y = (pos.y/(bounds.y*2))*1080
        this.setState({x:x, y:y});
    }

    moveRobot(direction){
        
        fetch('http://127.0.0.1:5000/demo', {
            method: 'GET',
            headers: {
                'Direction': direction
            },
        }).then(res=>res.json())
        .then(
           (res) => alert(res.text),
           (error) => alert('Error')
        )
    }

    moveToTarget(){
        fetch('http://127.0.0.1:5000/demopathfinding', {
            method: 'GET',
            headers: {
                'x': this.state.x*2,
                'y': this.state.y*2
            },
        }).then(res=>res.json())
        .then(
           (res) => alert(res.text),
           (error) => alert('Error')
        )
    }

    render(){

        let bounds = {x: window.innerWidth/2, y: (window.innerWidth/32)*9};

        return(
            <div>
                <h1>This is a demo of the communication flow from the app, through the server, to the robot.</h1>
                <ul>
                    <li><button onClick={() => this.moveRobot('forwards')}>Move Forwards</button></li>
                    <li><button onClick={() => this.moveRobot('backwards')}>Move Backwards</button></li>
                    <li><button onClick={() => this.moveRobot('left')}>Turn Left</button></li>
                    <li><button onClick={() => this.moveRobot('right')}>Turn Right</button></li>
                    <li><button onClick={() => this.moveRobot('stop')}>Stop</button></li>

                </ul>

                <Stage width={bounds.x} height={bounds.y} onMouseDown = {(e) => this.onMouseDown(e, bounds)}>
                    <Layer>
                        <Rect x={0} y={0} width={bounds.x} height={bounds.y} onClick = {this.onClick} stroke="black" />
                        <Circle x={(this.state.x/1920)*bounds.x*2} y={(this.state.y/1080)*bounds.y*2} fill={'red'} radius={10}/>
                    </Layer>
                </Stage>
                <button onClick = {this.moveToTarget.bind(this)}>Move to target</button>
            </div>
        )
    }
}

ReactDOM.render(<MainView />, document.getElementById('root'));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
