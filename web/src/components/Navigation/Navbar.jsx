import "./navbar.css";
import {Link} from "react-router-dom";
import navLogo from "../../assets/logos/logo-navbar.svg";

function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-container">
                {/* TODO: Turn image into a link to the home page. */}
                <a href="/">
                    <img src={navLogo} alt="Blank image." className="nav-logo"/>
                </a>
                <div className="nav-menu-wrap">
                    <div className="nav-link-wrap">
                        {/*<Link className="nav-link" to="/">About</Link>*/}
                        <Link className="nav-link" to="/signup">Sign Up</Link>
                        <Link className="nav-link" to="/login">Login</Link>
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Navbar;
