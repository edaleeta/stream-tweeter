import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetTemplatesCurrent } from './TweetTemplatesCurrent'
import { TweetTemplateCreateNew } from './TweetTemplateCreateNew'

export class TweetTemplates extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            isUpdated: false
        };
        this.onClickUpdateTweetTemplatesCurrent = this.onClickUpdateTweetTemplatesCurrent.bind(this);
    }

    onClickUpdateTweetTemplatesCurrent() {
        this.setState({
            isUpdated: true
        })
    }

    render() {
        if (this.props.isTwitterAuth) {
            
            return (
                <div>
                    <h3>Your Tweet Templates</h3>
                    <TweetTemplatesCurrent isUpdated={this.state.isUpdated}/>
                    <TweetTemplateCreateNew onClick={this.onClickUpdateTweetTemplatesCurrent} />
                </div>
            ); 
        } else {
            return <div></div>
        }
    }
}

TweetTemplates.propTypes = {
    isTwitterAuth: PropTypes.bool.isRequired
}