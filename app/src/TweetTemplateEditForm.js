import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { FormGroup, ControlLabel, FormControl, Button , ButtonToolbar } from 'react-bootstrap';

export class TweetTemplateEditForm extends Component {

    constructor(props) {
        super(props);
        this.state = {
            contents: this.props.contents,
            originalContents: this.props.contents
        };
        this.handleSaveClick = this.handleSaveClick.bind(this);
        this.handleResetClick = this.handleResetClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleSaveClick(e) {
        e.preventDefault();
        console.log(this.state.contents);
    }

    handleResetClick(e) {
        this.setState({
            contents: this.state.originalContents
        });
    }

    handleChange(e) {
        this.setState({
            contents: e.target.value
        });
    }

    render() {
        if (this.props.hidden) {
            return(
                <div>
                    I'm a hidden form...:)
                </div>
            )
        }
        return (
            <div>
                <form>
                    <FormGroup>
                        <ControlLabel>Update Tweet Template: </ControlLabel>
                        <FormControl onChange={this.handleChange} componentClass="textarea" value={this.state.contents}>
                        </FormControl>
                        <ButtonToolbar>
                            <Button type="submit" onClick={this.handleSaveClick}>Save Changes</Button>
                            <Button onClick={this.handleResetClick}>Reset Changes</Button>
                        </ButtonToolbar>
                    </FormGroup>
                </form>
            </div>
        )
    }
}

TweetTemplateEditForm.propTypes = {
    hidden: PropTypes.bool.isRequired,
    contents: PropTypes.string.isRequired
}