import "./sidebar.css"
import {Link, useNavigate} from 'react-router-dom';
import Icon from "../Icon/Icon.jsx";
import {signOut} from '../../services/authService.js';

function Sidebar() {
    const navigate = useNavigate();

    async function handleSignOut() {
        await signOut();
        navigate('/');
    }

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
                    <button className="dashboard-nav-link" onClick={handleSignOut}>Sign Out</button>
                </div>
            </div>
        </div>

    )
}

export default Sidebar;