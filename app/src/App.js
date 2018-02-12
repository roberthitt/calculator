import React from 'react';
import axios from 'axios';
import Dropzone from 'react-dropzone';
import { Input, Container, Header, Image, Grid, Button, Modal } from 'semantic-ui-react';

const SERVICE_URL = 'http://localhost:8080';

class UploadModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {files: [], isDropzoneHidden: false};
    }

    onDrop(files) {
        this.setState({files: files, isDropzoneHidden: true});
    }

    render() {
        let imageSource;
        let imageName;
        if(this.state.files.length !== 0){
            imageSource = this.state.files[0].preview;
            imageName = this.state.files[0].name;
        }

        return (
            <Modal size='tiny' trigger={<Button icon='upload'/>}>
                <Modal.Header>Select an image to extract text from.</Modal.Header>
                <Modal.Content>
                    <section>
                        <div className='dropzone'>
                            <div style={{display: 'flex', justifyContent: 'center'}}>
                                <Dropzone onDrop={this.onDrop.bind(this)}
                                        hidden={this.state.isDropzoneHidden}>
                                    <p>Drop an image here, or click to select an image.</p>
                                </Dropzone>
                            </div>
                            <Image hidden={!this.state.isDropzoneHidden} src={imageSource}/>
                        </div>
                        <aside>
                            <p hidden={!this.state.isDropzoneHidden}>{imageName}</p>
                        </aside>
                    </section>
                    <div hidden={!this.state.isDropzoneHidden}>
                        <Button positive>Upload</Button>
                        <Button onClick={() => this.setState({isDropzoneHidden: !this.state.isDropzoneHidden})}>Cancel</Button>
                    </div>
                </Modal.Content>
            </Modal>
        )
    }
}

class EquationInput extends React.Component {
    render() {
        const value = this.props.value;
        return (
            <Input placeholder='(enter an equation)'
                   label='f(x) = ' size='big'
                   value={value}
                   //action={<UploadButton onClick={this.props.onButtonClick}/>}
                   action={<UploadModal onClick={this.props.onButtonClick}/>}
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
        this.handleUpload = this.handleUpload.bind(this);
    }

    handleUpload() {
        console.log("UPLOAD");
    }

    handleChange(value) {
        this.setState({text: value});
    }

    handleKeyPress(key, value) {
        if(key === 'Enter') {
            const argument = encodeURIComponent(value);
            const validUrl = SERVICE_URL + '/valid?exp=' + argument;
            axios.get(validUrl).then(response => {
                if(response.data.localeCompare('valid') === 0) {
                    this.setState({text: value, value: value});
                }
            });
        }
    }

    render() {
        const argument = encodeURIComponent(this.state.value);
        const imageSource = SERVICE_URL + '/graph?exp=' + argument;
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
                                       onChange={this.handleChange}
                                       onButtonClick={this.handleUpload}/>
                    </Grid.Row>
                </Grid>
            </Container>
        );
    }
}

export default App;
