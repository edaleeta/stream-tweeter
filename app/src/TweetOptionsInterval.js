import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class TweetOptionsInterval extends Component {

    render() {
        return (
            <div>
                We'll change the tweeting interval here.
            </div>
        ); 
    }
}

TweetOptionsInterval.propTypes = {
    userId: PropTypes.number.isRequired
}