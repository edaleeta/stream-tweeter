import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetTemplateText } from './TweetTemplateText';

export class TweetTemplateContainer extends Component {

    render() {
        return (
            <div>
                <TweetTemplateText contents={this.props.template.contents} />
            </div>
        )
    }
}

TweetTemplateContainer.propTypes = {
    template: PropTypes.object.isRequired
}