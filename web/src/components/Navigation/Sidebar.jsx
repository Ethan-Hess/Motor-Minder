import "./sidebar.css"
import {Link} from 'react-router-dom';
import Icon from "../Icon/Icon.jsx";

function Sidebar() {
    return (
        <div className="dashboard-nav">
            <div className="dashboard-nav-menu">
                <div className="dashboard-link-wrap">
                    <Icon name="pencil" size="md" alt="Pencil Icon"/>
                    <Link className="dashboard-nav-link" to="/vehicles">Manage Vehicles</Link>
                </div>
                <div className="dashboard-link-wrap">
                    <Icon name="listPlus" size="md" alt="List Plus Icon"/>
                    <Link className="dashboard-nav-link" to="/log-service">Log Service</Link>
                </div>
                <div className="dashboard-link-wrap">
                    <Icon name="magnifyingGlass" size="md" alt="Magnifying Glass Icon"/>
                    <Link className="dashboard-nav-link" to="/mechanics">Find Mechanic</Link>
                </div>
            </div>
            <div className="dashboard-nav-footer">
                <div className="dashboard-link-wrap">
                    <Icon name="signOut" size="md" alt="Sign Out Icon"/>
                    <Link className="dashboard-nav-link" to="/">Sign Out</Link>
                </div>
            </div>
        </div>

    )
}

export default Sidebar;