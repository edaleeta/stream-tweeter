import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { NavBar } from './NavBar'
import { WelcomeUser } from './WelcomeUser'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userId: null,
      twitchDisplayName: null,
    }
  }

  componentWillMount(nextProps, nextState){
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
  render() {
    if (this.state.fetched) {
      return (
          <div>
              <NavBar />
              <WelcomeUser twitchDisplayName={this.state.twitchDisplayName} />
              <ConnectTwitter isTwitterAuth={this.state.isTwitterAuth}/>
          </div>
      )
    } else {
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
              <a href="http://localhost:7000/auth-twitter">Connect Twitter</a>
          </p>
      )
  }
}

export default App;
