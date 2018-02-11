import React from 'react';
import axios from 'axios';
import { Input, Container, Header, Image, Grid } from 'semantic-ui-react';

const SERVICE_URL = 'http://localhost:8080';

class EquationInput extends React.Component {
    render() {
        const value = this.props.value;
        return (
            <Input placeholder='(enter an equation)'
                   label='f(x) = ' size='big'
                   value={value}
                   onChange={(event, data) => this.props.onChange(data.value)}
                   onKeyPress={(e) => this.props.onKeyPress(e.key, value)}/>
        );
    }
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: 'x',
            value: 'x',
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
    }

    handleChange(value) {
        this.setState({text: value});
    }

    handleKeyPress(key, value) {
        if(key === 'Enter') {
            const validPath = encodeURI(SERVICE_URL + '/valid?exp=' + value);
            axios.get(validPath).then(response => {
                if(response.data.localeCompare('valid') === 0) {
                    this.setState({text: value, value: value});
                }
            });
        }
    }

    render() {
        const imageSource = encodeURI(SERVICE_URL + '/graph?exp=' + this.state.value);
        return (
            <Container style={{marginTop: '1em'}}>
                <Header as='h1' dividing>Calculator</Header>
                <Grid>
                    <Grid.Row>
                        <Image bordered rounded centered
                            src={imageSource} />
                    </Grid.Row>
                    <Grid.Row centered>
                        <EquationInput value={this.state.text}
                                       onKeyPress={this.handleKeyPress}
                                       onChange={this.handleChange}/>
                    </Grid.Row>
                </Grid>
            </Container>
        );
    }
}

export default App;
