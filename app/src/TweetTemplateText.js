import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class TweetTemplateText extends Component {

    render() {
        return <p>{this.props.contents.split('\r\n').map((text, key) => {
            return (
                <span key={key}>{text}<br /></span>
            )
        })}</p>
    }
}

TweetTemplateText.propTypes = {
    contents: PropTypes.string.isRequired
}