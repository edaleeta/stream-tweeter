import React, { Component } from 'react';
// import logo from './logo.svg';
import { PageHeader } from 'react-bootstrap';
import './App.css';
import { NavBar } from './NavBar'
import { WelcomeUser } from './WelcomeUser'
import { TweetTemplates } from './TweetTemplates'
import { TweetOptions } from './TwitterOptions'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userId: null,
      twitchDisplayName: null,
    };
    this.onClickTwitterAccessRevoked = this.onClickTwitterAccessRevoked.bind(this);
  }

  componentDidMount(nextProps, nextState) {
      fetch("/api/current-user.json",
      {credentials: 'same-origin'})
      .then((response)=> response.json())
      .then((data) => {
          let userId = data.userId;
          let twitchDisplayName = data.twitchDisplayName;
          let isTwitterAuth = data.isTwitterAuth;

          this.setState({
              userId: userId,
              twitchDisplayName: twitchDisplayName,
              isTwitterAuth: isTwitterAuth,
              fetched: true});
      })
  }

  onClickTwitterAccessRevoked() {
    this.setState({
      isTwitterAuth: false
    })
  }

  render() {
    if (this.state.fetched && this.state.userId) {
      // When the initial data has been fetched, and we receive the logged in user...
      return (
        <div>
            <PageHeader>Stream Tweeter <small>A social media automation tool for Twitch streamers.</small></PageHeader>
            <NavBar />
            <WelcomeUser twitchDisplayName={this.state.twitchDisplayName} />
            <ConnectTwitter isTwitterAuth={this.state.isTwitterAuth} />
            <TweetOptions isTwitterAuth={this.state.isTwitterAuth} userId={this.state.userId} onClick={this.onClickTwitterAccessRevoked} />
            <TweetTemplates isTwitterAuth={this.state.isTwitterAuth} userId={this.state.userId} />
          </div>
      );
    } else if (this.state.fetched) {
      // If we don't have a logged in user, show this...
      return (
        <div>
        <PageHeader>Stream Tweeter <small>A social media automation tool for Twitch streamers.</small></PageHeader>
        <NavBar />
        <WelcomeUser twitchDisplayName={this.state.twitchDisplayName} />
        {/* Perhaps include some other info we'll want to a show a non-logged in user. */}
        </div>
      );
    } else {
      // If our fetch hasn't completed, do not render anything.
      return <div></div>
    }
  }
}

// Connect Twitter Account
class ConnectTwitter extends Component {

  render() {
      if (this.props.isTwitterAuth) {
          return (
              <p>
                  Your Twitter is account is connected! <br />
                  Let's make some Tweets!
              </p>
          );
      }
      return (
          <p>
              To get started, please connect your Twitter account:<br />
              <a href="/auth-twitter">Connect Twitter</a>
          </p>
      )
  }
}

export default App;
