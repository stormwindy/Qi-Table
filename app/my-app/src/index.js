import React from 'react';
import ReactDOM from 'react-dom';
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
    render(){
        return(
            <div>
                <h1>This is the selection view. Choose a layout.</h1>
                <ul>
                    <li><LayoutCard name={1}/></li>
                    <li><LayoutCard name={2}/></li>
                </ul>
            </div>
        );
    }
}

class EditorView extends React.Component{
    render(){
        return(
            <div><h1>This is the editor view. Create a new layout.</h1></div>
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
            body: JSON.stringify({layoutID: this.props.name})
            //body: "aaaaaa"
        }).then(res => res.json())
        .then(
           (result) => alert(result.text),
           (error) => alert('Error')
        )
    }

    render(){
        return(
            <div>
            <p>Layout {this.props.name}</p>
            <button onClick={this.handleClick}>Choose this layout!</button>
            </div>
        )
    }
}

ReactDOM.render(<MainView />, document.getElementById('root'));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
