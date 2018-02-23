import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { FormGroup, ControlLabel, FormControl, HelpBlock, Button } from 'react-bootstrap'

export class TweetOptionsInterval extends Component {

    constructor(props) {
        super(props);
        this.state = {
            // We actually want to show the user's current tweet interval setting here, or default to 30 if not yet set.
            value: 30
        };
        this.getValidationState = this.getValidationState.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    handleChange(e) {
        this.setState({
            value: e.target.value
        });
    }
    
    handleClick(e) {
        e.preventDefault();

        // Prevent user from submitting invalid number of minutes.
        if (this.getValidationState() != null) {
            return null
        }

        let url = "/api/update-user-settings";
        let payload = JSON.stringify({
            userId: this.props.userId,
            tweetInterval: this.state.value
        });

        console.log(payload);

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
    });



    }
    getValidationState() {
        if (this.state.value < 30) {
            return "warning";
        }
        return null;
    }

    render() {
        return (
            <div>
                We'll change the tweeting interval here.
                <form>
                    <FormGroup controlId="tweetSettingsForm" validationState={this.getValidationState()} bsSize="lg">
                    <ControlLabel>Tweet Interval in Minutes</ControlLabel>
                    <FormControl
                        type="number"
                        value={this.state.value}
                        onChange={this.handleChange}
                    />
                    <FormControl.Feedback />
                    <HelpBlock>Don't spam your friends! Value be greater than 30 minutes.</HelpBlock>
                    <Button type="submit" onClick={this.handleClick} value={this.state.value} >Tweet Every {this.state.value} minutes!</Button>
                    </FormGroup>
                </form>
            </div>
        ); 
    }
}

TweetOptionsInterval.propTypes = {
    userId: PropTypes.number.isRequired
}