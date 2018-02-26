import React, { Component } from 'react';
import PropTypes from 'prop-types';
import  Loader  from 'react-loader-advanced';
import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faCog from '@fortawesome/fontawesome-free-solid/faCog';
import { Clip } from './Clip';

const spinnerElement = (
  <div>
    <h4>Loading from Twitch...</h4>
    <FontAwesomeIcon
      icon={faCog}
      transform="grow-50 down-50"
      spin />
  </div>
)

const loaderForegroundConfig = {
  color: "black",
  fontWeight: "bold"
}

const loaderBackgroundConfig = {
  backgroundColor: "rgba(255, 255, 255, 1)"
}

export class ClipContainer extends Component {

  constructor(props) {
    super(props);
    this.state = {
      clipSlug: null,
      clipLoaderShown: this.props.clipLoaderShown
    };
  }

  componentWillMount() {
    // Fetch to get clip info.

    let url = `/api/clips/${this.props.clipId}`;
    
    fetch(url,{
      credentials: 'same-origin'
    })
    .then((response)=> response.json())
    .then((data) => {
      this.setState({
        clipSlug: data.clips[0].slug
      });
    });
  }

  render() {
    return (
      <div> 
        <Loader
          show={this.props.clipLoaderShown}
          message={spinnerElement}
          foregroundStyle={loaderForegroundConfig}
          backgroundStyle={loaderBackgroundConfig}
          hideContentOnLoad={true}
        >
          <Clip
            clipSlug={this.state.clipSlug}
            hidden={this.props.clipHidden}
            onLoad={this.props.onLoadEmbed}
            loaded={this.state.loaded}
          />
        </Loader>

      </div>
    )
  }
}

ClipContainer.propTypes = {
  clipId: PropTypes.number,
  clipHidden: PropTypes.bool.isRequired,
  clipLoaderShown: PropTypes.bool.isRequired,
  onLoadEmbed: PropTypes.func.isRequired
}