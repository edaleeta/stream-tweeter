import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { convertTimeStamp } from './services/log'
import { SentTweetsContainer } from './SentTweetsContainer';

export class StreamSessionContainer extends Component {

  constructor(props) {
    super(props);
    this.state = {
      tweets: ""
    }
  }

  componentWillMount() {
    let url = `/api/sent-tweets?startedAt=${this.props.stream.startedAt}
      &endedAt=${this.props.stream.endedAt}`;
    
    fetch(url,{
      credentials: 'same-origin'
    })
    .then((response)=> response.json())
    .then((data) => {
      console.log("StreamSessionContainer mounted!");
      this.setState({
        tweets: data.tweets
      });
    })        
  }

  render() {
    let tweetsContainer = <div></div>
    if (this.state.tweets) {
      tweetsContainer = <SentTweetsContainer tweets={this.state.tweets} />;
    }

    return (
      <div>
        <h4>Stream: {this.props.stream.streamId}</h4>
        Started: {convertTimeStamp(this.props.stream.startedAt)} <br />
        Started Timestamp: {this.props.stream.startedAt} <br />
        Ended: {convertTimeStamp(this.props.stream.endedAt)} <br />
        Ended Timestamp: {this.props.stream.endedAt} <br />
        {this.props.stream.twitchSessionId} <br />
        {tweetsContainer}
      </div>
    )
  }
}


StreamSessionContainer.propTypes = {
  stream: PropTypes.object.isRequired,
}