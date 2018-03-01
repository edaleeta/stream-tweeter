import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Row } from 'react-bootstrap';
import { TweetTemplatesCurrent } from './TweetTemplatesCurrent';
import { TweetTemplateCreateNew } from './TweetTemplateCreateNew';


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
    });
  }

  render() {
    if (this.props.isTwitterAuth) {
      return (
        <div>
          <Row>
            <h2>Your Tweet Templates</h2>
          </Row>
          <Row>
            <TweetTemplatesCurrent onClick={this.onClickUpdateTweetTemplatesCurrent} isUpdated={this.state.isUpdated}/>
          </Row>
          <Row>
            <TweetTemplateCreateNew onClick={this.onClickUpdateTweetTemplatesCurrent} />
          </Row>
        </div>
      ); 
    } else {
      return <div></div>
    }
  }
}

TweetTemplates.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired
}