import React from 'react';


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

export default PositionForm
