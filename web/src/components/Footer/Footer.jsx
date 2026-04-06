import "./footer.css";
import {Link} from "react-router-dom";

function Footer() {
    return (
        <footer className="footer">
            <div className="container-lg">
                <div className="footer-wrap">
                    <div className="footer-top">
                        <img src="/assets/blank_image_square.png" alt="Blank image." className="footer-logo"/>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
                            voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
                    </div>
                    <div className="footer-bottom">
                        <Link to="/">Lorem ipsum</Link>
                        <Link to="/">Lorem ipsum</Link>
                        <Link to="/">Lorem ipsum</Link>
                        <Link to="/">Lorem ipsum</Link>
                        <Link to="/">Lorem ipsum</Link>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer;
