import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class TweetTemplateEditButton extends Component {

    render() {
        return (
            <button className="del-edit-button" value={this.props.templateId}>
                Edit Template
            </button>
        )
    }
}

TweetTemplateEditButton.propTypes = {
    templateId: PropTypes.string.isRequired
}