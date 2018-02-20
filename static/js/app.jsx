const navLinks = {
    home: "/index-react",
    login: "/login",
    logout: "/logout"
}

// Parent Component
class App extends React.Component 
{
    componentWillMount(nextProps, nextState){
        fetch("/current-user.json",
        {credentials: 'same-origin'})
        .then((response)=>
    console.log(response.json()))
    }
    render() {
        return <NavBar links={navLinks} />
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

// Username
class Username extends React.Component {
    render() {
        return this.props.username
    }
}

// Render Parent
ReactDOM.render(
    <App />,
    document.getElementById("root")
);
