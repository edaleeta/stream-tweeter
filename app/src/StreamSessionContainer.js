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
    let url = `/api/sent-tweets?startedAt=${this.props.stream.startedAt}&endedAt=${this.props.stream.endedAt}`;
    
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
    if (this.state.tweets.length > 0) {
      tweetsContainer = <SentTweetsContainer tweets={this.state.tweets} />;
    } else {
      tweetsContainer = <h4>No tweets sent!</h4>
    }

    return (
      <div>
        <h4>Stream Started: {convertTimeStamp(this.props.stream.startedAt)}</h4>
        {tweetsContainer}
      </div>
    )
  }
}


StreamSessionContainer.propTypes = {
  stream: PropTypes.object.isRequired,
}