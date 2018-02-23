import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetOptionsInterval } from './TweetOptionsInterval'
import { TweetOptionsRevoke } from './TweetOptionsRevoke'

export class TweetOptions extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            isUpdated: false
        }
    };

    render() {
        if (this.props.isTwitterAuth) {
            return (
                <div>
                    <h2>Twitter Options</h2>
                    Twitter Options will go here!
                    <TweetOptionsInterval userId={this.props.userId} />
                    <TweetOptionsRevoke userId={this.props.userId} onClick={this.props.onClick} />
                </div>
            ); 
        } else {
            return <div></div>
        }
    }
}

TweetOptions.propTypes = {
    isTwitterAuth: PropTypes.bool.isRequired,
    userId: PropTypes.number.isRequired,
    onClick: PropTypes.func.isRequired
}