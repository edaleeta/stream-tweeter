import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';

export class TweetTemplateDeleteButton extends Component {

    render() {
        return (
            <Button bsStyle="danger" className="del-tweet-button" value={this.props.templateId}>
                Delete Template
            </Button>
        )
    }
}

TweetTemplateDeleteButton.propTypes = {
    templateId: PropTypes.string.isRequired
}