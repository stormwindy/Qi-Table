import React from 'react';
import SelectionView from '../SelectionView/SelectionView'
import EditorView from '../EditorView/EditorView'
import SettingsView from '../SettingsView/SettingsView'
import logo from './Logo_2D.svg'
import classNames from 'classnames'

import './MainView.css'

const NavigationButton = props => (
    <div
        className={classNames('main__navbutton', {'main__navbutton--active': props.active})}
        onClick={props.onClick}>
        {props.children}
    </div>
)

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
            <main className="main">
                <nav className="main__navigation">
                    <img src={logo} alt=""/>

                    <NavigationButton
                        onClick={() => this.setState({view: 'select'})}
                        active={ this.state.view === 'select' }>
                        Select Layout
                    </NavigationButton>
                    <NavigationButton
                        onClick={() => this.setState({view: 'editor'})}
                        active={ this.state.view === 'editor' }>
                        Create Layout
                    </NavigationButton>
                    <NavigationButton
                        onClick={() => this.setState({view: 'settings'})}
                        active={ this.state.view === 'settings' }>
                        Configuration
                    </NavigationButton>

                </nav>
                <article className="main__container">
                    {view}
                </article>
            </main>
        );
    }
}

export default MainView
