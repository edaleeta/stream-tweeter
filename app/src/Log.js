import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { StreamSessionsContainer } from './StreamSessionsContainer';
import { Grid } from 'react-bootstrap';

export class Log extends Component {

  render() {
    console.log("Log rendering.")
    return (
      <Grid fluid={true}>
        <h3>Your Stream Tweeter History</h3>
        <StreamSessionsContainer userId={this.props.userId} />
      </Grid>
    )
  
  }
}

Log.propTypes = {
  userId: PropTypes.number.isRequired,
}


