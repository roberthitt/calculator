import React from 'react'
import { render } from 'react-dom'
import { Input, Container, Header, } from 'semantic-ui-react'

class EquationInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: '',
        };
    }

    handleChange(value) {
        this.setState({text: value});
    }

    render() {
        return (
            <Input placeholder='(enter an equation)'
                   label='f(x) = ' fluid
                   value={this.state.text}
                   onChange={(event, data) => this.handleChange(data.value)}/>
        );
    }
}

class App extends React.Component {
    render() {
        return (
            <Container style={{marginTop: '3em'}}>
                <Header as='h1' dividing>Calculator</Header>
                <EquationInput />
            </Container>
        );
    }
}

export default App;
