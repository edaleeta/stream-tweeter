const navLinks = {
    home: "/index-react",
    login: "/login",
    logout: "/logout"
}

// Parent Component
class App extends React.Component {
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
                <NavBar links={navLinks} />
                <WelcomeUser twitchDisplayName={this.state.twitchDisplayName} />
                <ConnectTwitter isTwitterAuth={this.state.isTwitterAuth}/>
            </div>
        )
    }
}

// Navigation 
class NavBar extends React.Component {
    render() {
        return (
            <ul>
            <li><a href={navLinks.home}>Home</a></li>
            <li><a href={navLinks.login}>Login</a></li>
            <li><a href={navLinks.logout}>Logout</a></li>
        </ul>
        )
    }
}

// Welcome
class WelcomeUser extends React.Component {
    render() {
        return (
            <h2>Welcome, {this.props.twitchDisplayName}!
            </h2>
        )
    }
}

// Connect Twitter Account
class ConnectTwitter extends React.Component {

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

// Render App
ReactDOM.render(
    <App />,
    document.getElementById("root")
);
