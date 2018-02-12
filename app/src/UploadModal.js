import React from 'react';
import Dropzone from 'react-dropzone';
import { Image, Button, Modal } from 'semantic-ui-react';

class UploadModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {files: [], isDropzoneHidden: false, isOpen: false};

        this.onClick = this.onClick.bind(this);
    }

    onDrop(files) {
        this.setState({files: files, isDropzoneHidden: true});
    }

    onClick() {
        this.setState({isOpen: false, isDropzoneHidden: false});
        this.props.onClick(this.state.files[0]);
    }

    render() {
        let imageSource;
        let imageName;
        if(this.state.files.length !== 0){
            imageSource = this.state.files[0].preview;
            imageName = this.state.files[0].name;
        }

        return (
            <Modal open={this.state.isOpen} size='tiny'
                   onClose={() => this.setState({isOpen: false})}
                   trigger={<Button icon='upload' onClick={() => this.setState({isOpen: true})}/>}>
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
                        <Button positive onClick={() => this.onClick()}>Upload</Button>
                        <Button onClick={() => this.setState({isDropzoneHidden: !this.state.isDropzoneHidden})}>Cancel</Button>
                    </div>
                </Modal.Content>
            </Modal>
        )
    }
}

export default UploadModal;
