import {Link} from 'react-router-dom';
import Icon from "../components/Icon/Icon.jsx";
import Sidebar from "../components/Navigation/Sidebar.jsx";

function DashboardPage() {
    return (
        <div className="page-wrap">
            <div className="dashboard-wrap">
                <Sidebar/>
                <div className="dashboard-main">
                    <div className="dashboard-header">
                        <h1>MotorMinder</h1>
                    </div>
                    <div className="dashboard-grid">
                        <img alt="Future graph" src="/assets/blank_image_square.png"/>
                        <img alt="Future graph" src="/assets/blank_image_square.png"/>
                        <img alt="Future graph" src="/assets/blank_image_square.png"/>
                        <img alt="Future graph" src="/assets/blank_image_square.png"/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DashboardPage;
