import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { NavBar } from './NavBar'

class App extends Component {
  constructor(props) {
      super(props);
      this.state = {twitchDisplayName: null}
  }

  componentDidMount(nextProps, nextState){
      fetch("/current-user.json",
      {credentials: 'same-origin'})
      .then((response)=> response.json())
      .then((data) => {
          let twitchDisplayName = data.twitchDisplayName;
          let isTwitterAuth = data.isTwitterAuth;

          this.setState({
              twitchDisplayName: twitchDisplayName,
              isTwitterAuth: isTwitterAuth});
      })
  }
  render() {
      return (
          <div>
              <NavBar />
              <WelcomeUser twitchDisplayName={this.state.twitchDisplayName} />
              <ConnectTwitter isTwitterAuth={this.state.isTwitterAuth}/>
          </div>
      )
  }
}

// Welcome
class WelcomeUser extends Component {
  render() {
      return (
          <h2>Welcome, {this.props.twitchDisplayName}!
          </h2>
      )
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
