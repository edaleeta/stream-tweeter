import React, { Component } from 'react';
import { FormGroup, ControlLabel, FormControl, Button } from 'react-bootstrap';
import { TweetTemplatesCurrent } from './TweetTemplatesCurrent'; 
export class TweetTemplateCreateNew extends Component {
    constructor(props) {
        super(props);
        this.state = {
            contents: null
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleOnChange = this.handleOnChange.bind(this);
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
        }).then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => {
            if (response.ok) {
            console.log('Success:', response);
            } else {
                console.log("Error:", response)
            }
        })
    }

    handleOnChange(e) {
        // Note: We only want to set the state after someone types in the text field.
        // This is to prevent someone from submitting the defaultValue to db.
        this.setState({
            contents: e.target.value
        });
    }

    render() {
        return (
            <form>
                <FormGroup>
                    <ControlLabel>Create a new Tweet Template: </ControlLabel>
                    <FormControl onChange={this.handleOnChange} componentClass="textarea" defaultValue={"Enter your tweet here! Use placeholders, such as ${game}, to include your streamed game's title!"}>
                    </FormControl>
                    <Button type="submit" onClick={this.handleClick}>Save Tweet Template</Button>
                </FormGroup>

            </form>
        )
    }
}
