import React, { Component } from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import { SentTweetsContainer } from './SentTweetsContainer';

export class StreamSessionContainer extends Component {

  constructor(props) {
    super(props);
    this.state = {
      tweets: ""
    }
    this.convertTimeStamp = this.convertTimeStamp.bind(this);
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

  convertTimeStamp(timestamp) {
    let date = moment.unix(timestamp);
    return date.format("dddd, MMMM Do YYYY, h:mm:ss a");
  }

  render() {
    let tweetsContainer = <div></div>
    if (this.state.tweets) {
      tweetsContainer = <SentTweetsContainer tweets={this.state.tweets} />;
    }

    return (
      <div>
        <h4>{this.props.stream.streamId}</h4>
        Started: {this.convertTimeStamp(this.props.stream.startedAt)} <br />
        Started Timestamp: {this.props.stream.startedAt} <br />
        Ended: {this.convertTimeStamp(this.props.stream.endedAt)} <br />
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