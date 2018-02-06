import React from 'react';
import axios from 'axios';
import { Input, Container, Header, Image } from 'semantic-ui-react';

const SERVICE_URL = 'http://localhost:8080';

class EquationInput extends React.Component {
    render() {
        const value = this.props.value;
        return (
            <Input placeholder='(enter an equation)'
                   label='f(x) = ' fluid
                   value={value}
                   onChange={(event, data) => this.props.onChange(data.value)}/>
        );
    }
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: 'x',
        };

        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(value) {
        this.setState({text: value});
    }

    render() {
        const imageSource = SERVICE_URL + '/graph?exp=' + this.state.text;
        return (
            <Container style={{marginTop: '3em'}}>
                <Header as='h1' dividing>Calculator</Header>
                <Image bordered rounded centered
                       src={imageSource} />
                <EquationInput value={this.state.text} onChange={this.handleChange}/>
            </Container>
        );
    }
}

export default App;
