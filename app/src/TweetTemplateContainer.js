import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class TweetTemplateContainer extends Component {

    render() {
        return <p>{this.props.template.contents.split('\r\n').map((text, key) => {
            return (
                <span key={key}>{text}<br /></span>
            )
        })}</p>
    }
}

TweetTemplateContainer.propTypes = {
    template: PropTypes.object.isRequired
}