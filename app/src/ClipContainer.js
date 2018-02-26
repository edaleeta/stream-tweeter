import React, { Component } from 'react';
import PropTypes from 'prop-types';
import  Loader  from 'react-loader-advanced';
import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faSpinner from '@fortawesome/fontawesome-free-solid/faSpinner';
import { Clip } from './Clip';

const spinnerElement = (
  <FontAwesomeIcon
    icon={faSpinner}
    transform="grow-50"
    spin />
)

const loaderForegroundConfig = {
  color: "black"
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