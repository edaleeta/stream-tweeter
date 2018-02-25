import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroupItem, Button } from 'react-bootstrap';
import { convertTimeStamp } from './services/log'
import Autolinker from 'autolinker';

export class SentTweet extends Component {

  render() {
    let messageHTML = Autolinker.link(this.props.message, {
      newWindow : true,
      truncate  : 30
    });
    console.log(messageHTML);

    return (
      <ListGroupItem
        header={"Tweet Created: " + convertTimeStamp(this.props.createdAt)}
        target="_blank"
      >
        <span>Message: </span><span dangerouslySetInnerHTML={{__html: messageHTML}}></span>
        <br /><br />
        <Button 
          href={this.props.permalink}
          target="_blank"
        >
          View on Twitter
        </Button>       
      </ListGroupItem>
    )
  }
}

SentTweet.propTypes = {
  clipId: PropTypes.number,
  createdAt: PropTypes.number.isRequired,
  message: PropTypes.string.isRequired,
  permalink: PropTypes.string.isRequired,
  tweetTwtrId: PropTypes.string.isRequired,
  userId: PropTypes.number.isRequired
}