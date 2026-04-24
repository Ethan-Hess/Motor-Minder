import {useEffect, useMemo, useState} from "react";
import {
    BarChart,
    Bar,
    CartesianGrid,
    PieChart,
    Pie,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import Sidebar from "../components/Navigation/Sidebar.jsx";
import {useAuth} from "../context/AuthContext.jsx";
import {listVehicles} from "../services/vehicleService.js";
import {SERVICE_NAMES, SERVICE_INTERVALS} from "../types/domain.js";

const HEALTH_SCORE_MAP = {
    OK: 100,
    DUE_SOON: 65,
    OVERDUE: 25,
    UNKNOWN: 50,
};

function getMileageStatus(vehicle, serviceName) {
    const interval = SERVICE_INTERVALS[serviceName];
    const lastService = vehicle.lastService?.[serviceName];

    if (!interval || !lastService || !Number.isFinite(lastService.mileage)) {
        return "UNKNOWN";
    }

    const milesSinceService = vehicle.currentMileage - lastService.mileage;
    const dueSoonMiles = interval.miles?.[0];
    const overdueMiles = interval.miles?.[1];

    if (!Number.isFinite(milesSinceService)) {
        return "UNKNOWN";
    }

    if (Number.isFinite(overdueMiles) && milesSinceService >= overdueMiles) {
        return "OVERDUE";
    }

    if (Number.isFinite(dueSoonMiles) && milesSinceService >= dueSoonMiles) {
        return "DUE_SOON";
    }

    return "OK";
}

function getVehicleHealthScore(vehicle) {
    const scores = SERVICE_NAMES.map((serviceName) => {
        const status = getMileageStatus(vehicle, serviceName);
        return HEALTH_SCORE_MAP[status];
    });

    if (scores.length === 0) return 0;

    const total = scores.reduce((sum, score) => sum + score, 0);
    return Math.round(total / scores.length);
}

function DashboardPage() {
    const {uid: userId} = useAuth();
    const [vehicles, setVehicles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadVehicles() {
            setLoading(true);
            setError("");

            try {
                const nextVehicles = await listVehicles(userId);
                setVehicles(nextVehicles);
            } catch (loadError) {
                setError(loadError.message ?? "Failed to load dashboard data");
            } finally {
                setLoading(false);
            }
        }

        if (userId) {
            loadVehicles();
        }
    }, [userId]);

    const averageMileage = useMemo(() => {
        if (vehicles.length === 0) return 0;
        const total = vehicles.reduce(
            (sum, vehicle) => sum + (vehicle.currentMileage || 0),
            0
        );
        return Math.round(total / vehicles.length);
    }, [vehicles]);

    const averageHealth = useMemo(() => {
        if (vehicles.length === 0) return 0;
        const total = vehicles.reduce(
            (sum, vehicle) => sum + getVehicleHealthScore(vehicle),
            0
        );
        return Math.round(total / vehicles.length);
    }, [vehicles]);

    const mileageChartData = useMemo(() => {
        return vehicles.map((vehicle) => ({
            name: `${vehicle.year} ${vehicle.make}`,
            mileage: vehicle.currentMileage || 0,
        }));
    }, [vehicles]);

    const healthChartData = useMemo(() => {
        return [
            {name: "Health", value: averageHealth},
            {name: "Remaining", value: Math.max(100 - averageHealth, 0)},
        ];
    }, [averageHealth]);

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
                        <div className="dashboard-grid dashboard-grid-cards">
                            <div className="dashboard-card">
                                <div className="dashboard-card-header">
                                    <h3>Average Vehicle Health</h3>
                                    <p>{averageHealth}%</p>
                                </div>

                                <div className="chart-wrap">
                                    <ResponsiveContainer width="100%" height={260}>
                                        <PieChart>
                                            <Pie
                                                data={healthChartData}
                                                dataKey="value"
                                                innerRadius={70}
                                                outerRadius={100}
                                                startAngle={90}
                                                endAngle={-270}
                                            >
                                                <Cell fill="var(--colors-teal-9)"/>
                                                <Cell fill="var(--colors-gray-4)"/>
                                            </Pie>
                                            <Tooltip/>
                                        </PieChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            <div className="dashboard-card">
                                <div className="dashboard-card-header">
                                    <h3>Average Mileage</h3>
                                    <p>{averageMileage.toLocaleString()} mi</p>
                                </div>

                                <div className="chart-wrap">
                                    <ResponsiveContainer width="100%" height={260}>
                                        <BarChart data={mileageChartData}>
                                            <CartesianGrid strokeDasharray="3 3"/>
                                            <XAxis dataKey="name"/>
                                            <YAxis/>
                                            <Tooltip/>
                                            <Bar dataKey="mileage" fill="var(--colors-teal-9)" radius={[8, 8, 0, 0]}/>
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            <div className="dashboard-card">
                                <div className="dashboard-card-header">
                                    <h3>Total Vehicles</h3>
                                    <p>{vehicles.length}</p>
                                </div>
                            </div>

                            <div className="dashboard-card">
                                <div className="dashboard-card-header">
                                    <h3>Highest Mileage Vehicle</h3>
                                    <p>
                                        {vehicles.length > 0
                                            ? `${Math.max(...vehicles.map((v) => v.currentMileage || 0)).toLocaleString()} mi`
                                            : "0 mi"}
                                    </p>
                                </div>
                            </div>
                        </div>
                    ) : null}
                </div>
            </div>
        </div>
    );
}

export default DashboardPage;
