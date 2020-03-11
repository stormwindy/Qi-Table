import React from 'react';
import SelectionView from '../SelectionView/SelectionView'
import EditorView from '../EditorView/EditorView'
import SettingsView from '../SettingsView/SettingsView'

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

export default MainView
