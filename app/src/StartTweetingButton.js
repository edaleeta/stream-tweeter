import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';

export class StartTweetingButton extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(e) {
        console.log(e);
        console.log(this.props.userId)

        let url = "/api/start-tweeting"
        let payload = JSON.stringify({
            userId: this.props.userId,
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
        })
    }

    render() {
        return (
            <Button bsStyle="success" className="start-tweet-button" onClick={this.handleClick}>
                Start Tweeting
            </Button>
        );
    }
}

StartTweetingButton.propTypes = {
    userId: PropTypes.number.isRequired
}