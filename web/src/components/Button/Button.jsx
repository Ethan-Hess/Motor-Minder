import "./button.css";
import {Link} from "react-router-dom";

function Button({text, link, variant}) {
    const className = `button ${variant ? `button-${variant}` : ""}`;

    if (link) {
        return (
            <Link to={link} className={className}>
                {text}
            </Link>
        );
    }

    return (
        <button className={className}>
            {text}
        </button>
    );
}

export default Button;
