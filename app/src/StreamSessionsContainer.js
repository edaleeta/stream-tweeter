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

  handleLoadMore() {
    console.log("We're going to load more streams.");
  }

  render() {
    if (this.state.streams) {
      console.log("Stream data fetched.")
      return (

        <InfiniteScroll
          loadMore={this.handleLoadMore}
          hasMore={this.state.nextPage} // When this.state.nextPage does not exist, set to false.
          loader={<div className="loader">Loading ...</div>}
        >
          <StreamSessions
            streams={this.state.streams}
            userId={this.props.userId}
          />
        </InfiniteScroll>
      ); 
    } else {
      return <div></div>
    }
  }
}

StreamSessionsContainer.propTypes = {
  userId: PropTypes.number.isRequired
}