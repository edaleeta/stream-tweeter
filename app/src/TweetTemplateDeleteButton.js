import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class TweetTemplateDeleteButton extends Component {

    render() {
        return (
            <button className="del-tweet-button" value={this.props.templateId}>
                Delete Template
            </button>
        )
    }
}

TweetTemplateDeleteButton.propTypes = {
    templateId: PropTypes.string.isRequired
}