import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';

export class TweetTemplateDeleteButton extends Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(e) {
        console.log(e.target.value);
        // Trigger reload of current template list
        // Note: We'll want to prevent TweetTemplateCurrent from rerendering if no tweet was deleted.

        
        this.props.onClick();
    }

    render() {
        return (
            <Button bsStyle="danger" className="del-tweet-button" value={this.props.templateId} onClick={this.handleClick}>
                Delete Template
            </Button>
        )
    }
}

TweetTemplateDeleteButton.propTypes = {
    templateId: PropTypes.number.isRequired,
    onClick: PropTypes.func.isRequired
}