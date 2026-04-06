import "./navbar.css";
import {Link} from "react-router-dom";

function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <img src="/assets/blank_image.png" alt="Blank image." className="nav-logo"/>
                <div className="nav-menu-wrap">
                    <div className="nav-link-wrap">
                        <Link className="nav-link" to="/">About</Link>
                        <Link className="nav-link" to="/signup">Sign Up</Link>
                        <Link className="nav-link" to="/login">Login</Link>
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Navbar;
