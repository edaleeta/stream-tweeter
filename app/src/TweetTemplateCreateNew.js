import React, { Component } from 'react';
import { FormGroup, ControlLabel, FormControl, Button } from 'react-bootstrap';
export class TweetTemplateCreateNew extends Component {
    constructor(props) {
        super(props);
        this.state = {
            contents: "Enter your tweet here! Use placeholders, such as ${game}, to include your streamed game's title!",
            defaultContents: "Enter your tweet here! Use placeholders, such as ${game}, to include your streamed game's title!"
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleFocus = this.handleFocus.bind(this);
    }

    handleClick(e) {
        e.preventDefault();
        console.log(this.state.contents);
        console.log(JSON.stringify(this.state));
        let url = "/api/add-tweet-template";
        let payload = JSON.stringify(this.state);

        fetch(url, {
                credentials: 'same-origin',
                method: 'POST',
                body: payload, 
                headers: new Headers({
                'Content-Type': 'application/json'
                })
        })
        .then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => {
                console.log('Success:', response);
                // Tells Tweet Templates that we saved a new Template!
                this.props.onClick();
                // Clear contents of textbox after submitting.
                this.setState({
                    contents: ""
                });
        })
    }

    handleChange(e) {
        this.setState({
            contents: e.target.value
        });
    }

    handleFocus(e) {
        if (this.state.contents === this.state.defaultContents) {
            this.setState({
                contents: ""
            });
        }
    }

    render() {
        return (
            <form>
                <FormGroup>
                    <ControlLabel>Create a new Tweet Template: </ControlLabel>
                    <FormControl onFocus={this.handleFocus} onChange={this.handleChange} componentClass="textarea" value={this.state.contents}>
                    </FormControl>
                    <Button type="submit" onClick={this.handleClick}>Save Tweet Template</Button>
                </FormGroup>

            </form>
        )
    }
}
