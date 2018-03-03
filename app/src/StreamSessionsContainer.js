import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroup } from 'react-bootstrap';
import { StreamSessions } from './StreamSessions';
import InfiniteScroll from 'react-infinite-scroller';

export class StreamSessionsContainer extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      streams: "",
      nextPage: ""
    };
  }

  componentWillMount() {
    fetch("/api/streams",
    {credentials: 'same-origin'})
    .then((response)=> response.json())
    .then((data) => {
      console.log("StreamSessionsContainer mounted!");
      this.setState({
        streams: data.streams,
        nextPage: data.next
      });
    })        
  }

  render() {
    if (this.state.streams) {
      console.log("Stream data fetched.")
      return (
          <StreamSessions
            streams={this.state.streams}
            userId={this.props.userId}
          />
      ); 
    } else {
      return <div></div>
    }
  }
}

StreamSessionsContainer.propTypes = {
  userId: PropTypes.number.isRequired
}