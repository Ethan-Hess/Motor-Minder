import "./footer.css";
import footerLogo from "@/assets/logos/logo-footer.svg";
import {Link} from "react-router-dom";

function Footer() {
    return (
        <footer className="footer">
            <div className="container-lg">
                <div className="footer-wrap">
                    <div className="footer-top">
                        <img src={footerLogo} alt="MotorMinder logo" className="footer-logo"/>
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
