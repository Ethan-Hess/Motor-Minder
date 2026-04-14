import "./footer.css";
import {Link} from "react-router-dom";
import footerLogo from "../../assets/logos/logo-footer.svg";

function Footer() {
    return (
        <footer className="footer">
            <div className="container-lg">
                <div className="footer-wrap">
                    <div className="footer-top">
                        <img src={footerLogo} alt="Blank image." className="footer-logo"/>
                    </div>
                    <div className="footer-bottom">
                        <Link to="/" target="_blank" className="footer-link">Ethan Hess</Link>
                        <Link to="/" target="_blank" className="footer-link">Ethan Kidd</Link>
                        <Link to="/" target="_blank" className="footer-link">Preston Little</Link>
                        <Link to="/" target="_blank" className="footer-link">Ryan Carbine</Link>
                    </div>
                </div>
            </div>
        </footer>
    )
}

export default Footer;
