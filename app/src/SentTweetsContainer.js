import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroup, Row, Col } from 'react-bootstrap';
import { SentTweet } from './SentTweet';

export class SentTweetsContainer extends Component {

  render() {
    let content = [];

    this.props.tweets.map((tweet, key)=> {
      content.push(
        <Col xs={12} md={6}>
          <SentTweet
            key={key}
            clipId={tweet.clipId}
            createdAt={tweet.createdAt}
            message={tweet.message}
            permalink={tweet.permalink}
            tweetTwtrId={tweet.tweetTwtrId}
            userId={tweet.userId}
          />
        </Col>
      )
    });

    let groupSize = 2;
    let rows = content.reduce((row, column, key) => {
      key % groupSize == 0 && row.push([]);
      row[row.length - 1].push(column);
      return row;
    }, []).map((rowContent, key) => {
      return (
        <Row key={key}>
          {rowContent}
        </Row>
      )
    })

    return (
      <div>{rows}</div>
    )
  }
}

SentTweetsContainer.propTypes = {
  tweets: PropTypes.array.isRequired
}