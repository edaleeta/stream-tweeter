const navLinks = {
    home: "/index-react",
    login: "/login",
    logout: "/logout"
}

// Navigation 
export class NavBar extends React.Component {
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