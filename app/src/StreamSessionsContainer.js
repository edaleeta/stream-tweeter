import React, { Component } from "react";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroller";
import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faCog from "@fortawesome/fontawesome-free-solid/faCog";
import { StreamSessions } from "./StreamSessions";

// Store already fetched streams.
let fetchedStreams;

export class StreamSessionsContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      streams: "",
      nextPage: ""
    };
    this.handleLoadMore = this.handleLoadMore.bind(this);
  }

  componentWillMount() {
    fetch("/api/streams", { credentials: "same-origin" })
      .then(response => response.json())
      .then(data => {
        console.log("StreamSessionsContainer mounted!");
        fetchedStreams = data.streams;
        this.setState({
          streams: data.streams,
          nextPage: data.next
        });
      });
  }

  handleLoadMore() {
    console.log("We're going to load more streams.");
    // Fetch next "page" of streams
    // Add those to fetched streams array
    // Push them to state
    fetch(this.state.nextPage, { credentials: "same-origin" })
      .then(response => response.json())
      .then(data => {
        fetchedStreams.push(...data.streams);
        console.log(data.streams);
        console.log(fetchedStreams);
        this.setState({
          streams: fetchedStreams,
          nextPage: data.next ? data.next : null
        });
      });
  }

  render() {
    if (this.state.streams) {
      console.log(this.state.nextPage);

      const loadingElement = (
        <span key={this.state.nextPage}>
          Loading more past stream data...
          <FontAwesomeIcon icon={faCog} spin />
        </span>
      );

      return (
        <InfiniteScroll
          loadMore={this.handleLoadMore}
          hasMore={this.state.nextPage ? true : false} // When this.state.nextPage does not exist, set to false.
          loader={loadingElement}
        >
          <StreamSessions
            streams={this.state.streams}
            userId={this.props.userId}
          />
        </InfiniteScroll>
      );
    } else {
      return <div />;
    }
  }
}

StreamSessionsContainer.propTypes = {
  userId: PropTypes.number.isRequired
};
