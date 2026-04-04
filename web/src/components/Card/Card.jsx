import "./card.css";
import Button from "../Button/Button.jsx";

function Card({title, description, buttonText, imageURL, imageAltText, variant}) {
    return (
        <div className={`card ${variant ? `card-${variant}` : ""}`}>
            <div className="card-header">
                <div className="card-header-content">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                <Button text={buttonText} variant="text"/>
            </div>
            <div className="card-footer">
                <img src={imageURL} alt={imageAltText}/>
            </div>
        </div>
    )
}

export default Card;
