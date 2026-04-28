import {useEffect, useMemo, useState} from 'react';
import Sidebar from "../components/Navigation/Sidebar.jsx";
import {useAuth} from '../context/AuthContext.jsx';
import {listVehicles} from '../services/vehicleService.js';
import {listVehicleServiceHistory} from '../services/serviceLogService.js';
import {SERVICE_NAMES, SERVICE_INTERVALS} from '../types/domain.js';

function getServiceStatus(vehicle, serviceName) {
    const interval = SERVICE_INTERVALS[serviceName];
    const lastService = vehicle.lastService?.[serviceName];

    if (!interval || !lastService || !Number.isFinite(lastService.mileage)) {
        return 'unknown';
    }

    const milesSinceService = vehicle.currentMileage - lastService.mileage;
    const dueSoonMiles = interval.miles?.[0];
    const overdueMiles = interval.miles?.[1];

    if (!Number.isFinite(milesSinceService)) {
        return 'unknown';
    }

    if (Number.isFinite(overdueMiles) && milesSinceService >= overdueMiles) {
        return 'overdue';
    }

    if (Number.isFinite(dueSoonMiles) && milesSinceService >= dueSoonMiles) {
        return 'dueSoon';
    }

    return 'ok';
}

function DashboardPage() {
    const {uid: userId} = useAuth();

    const [vehicles, setVehicles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [totalLoggedServices, setTotalLoggedServices] = useState(0);

    useEffect(() => {
        async function loadDashboardData() {
            if (!userId) {
                setVehicles([]);
                setTotalLoggedServices(0);
                setLoading(false);
                return;
            }

            setLoading(true);
            setError('');

            try {
                const nextVehicles = await listVehicles(userId);
                setVehicles(nextVehicles);

                if (nextVehicles.length === 0) {
                    setTotalLoggedServices(0);
                    return;
                }

                const historyLists = await Promise.all(
                    nextVehicles.map((vehicle) => listVehicleServiceHistory(userId, vehicle.id))
                );

                const totalServices = historyLists.reduce((sum, history) => sum + history.length, 0);
                setTotalLoggedServices(totalServices);
            } catch (loadError) {
                setError(loadError.message ?? 'Failed to load dashboard data');
                setVehicles([]);
                setTotalLoggedServices(0);
            } finally {
                setLoading(false);
            }
        }

        loadDashboardData();
    }, [userId]);

    const totalVehicles = vehicles.length;

    const nextServicesDueCount = useMemo(() => {
        if (vehicles.length === 0) return 0;

        let count = 0;

        vehicles.forEach((vehicle) => {
            SERVICE_NAMES.forEach((serviceName) => {
                const status = getServiceStatus(vehicle, serviceName);

                if (status === 'dueSoon') {
                    count += 1;
                }
            });
        });

        return count;
    }, [vehicles]);

    const overdueServicesCount = useMemo(() => {
        if (vehicles.length === 0) return 0;

        let count = 0;

        vehicles.forEach((vehicle) => {
            SERVICE_NAMES.forEach((serviceName) => {
                const status = getServiceStatus(vehicle, serviceName);

                if (status === 'overdue') {
                    count += 1;
                }
            });
        });

        return count;
    }, [vehicles]);

    return (
        <div className="page-wrap">
            <div className="dashboard-wrap">
                <Sidebar/>
                <div className="dashboard-main">
                    <div className="dashboard-header">
                        <h1>MotorMinder</h1>
                        <p>Welcome back! Here’s a quick look at your vehicles.</p>
                    </div>

                    {loading ? <p>Loading dashboard...</p> : null}
                    {error ? <p className="message-error">{error}</p> : null}

                    {!loading && !error ? (
                        <div className="dashboard-grid">
                            <div className="card-dashboard">
                                <div className="text-size-xl text-align-center">Total Vehicles</div>
                                <div className="text-size-huge text-color-brand">{totalVehicles}</div>
                            </div>

                            <div className="card-dashboard">
                                <div className="text-size-xl text-align-center">Total Logged Services</div>
                                <div className="text-size-huge text-color-brand">{totalLoggedServices}</div>
                            </div>

                            <div className="card-dashboard">
                                <div className="text-size-xl text-align-center">Next Services Due</div>
                                <div className="text-size-huge text-color-brand">{nextServicesDueCount}</div>
                            </div>

                            <div className="card-dashboard">
                                <div className="text-size-xl text-align-center">Overdue Services Count</div>
                                <div className="text-size-huge text-color-brand">{overdueServicesCount}</div>
                            </div>
                        </div>
                    ) : null}
                </div>
            </div>
        </div>
    );
}

export default DashboardPage;