import {useEffect, useMemo, useState} from 'react';
import {useAuth} from '../context/AuthContext.jsx';
import {logService, listVehicleServiceHistory} from '../services/serviceLogService.js';
import {listVehicles} from '../services/vehicleService.js';
import {SERVICE_NAMES} from '../types/domain.js';
import Sidebar from "../components/Navigation/Sidebar.jsx";

function todayIsoDate() {
    return new Date().toISOString().slice(0, 10);
}

function LogServicePage() {
    const [vehicles, setVehicles] = useState([]);
    const [history, setHistory] = useState([]);
    const [loadingVehicles, setLoadingVehicles] = useState(true);
    const [loadingHistory, setLoadingHistory] = useState(false);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const [vehicleId, setVehicleId] = useState('');
    const [serviceName, setServiceName] = useState(SERVICE_NAMES[0]);
    const [mileage, setMileage] = useState('');
    const [serviceDate, setServiceDate] = useState(todayIsoDate());

    const {uid: userId} = useAuth();

    const selectedVehicle = useMemo(
        () => vehicles.find((vehicle) => vehicle.id === vehicleId) ?? null,
        [vehicleId, vehicles],
    );

    async function refreshVehicles() {
        setLoadingVehicles(true);
        setError('');

        try {
            const nextVehicles = await listVehicles(userId);
            setVehicles(nextVehicles);

            if (!vehicleId && nextVehicles.length > 0) {
                setVehicleId(nextVehicles[0].id);
                setMileage(String(nextVehicles[0].currentMileage));
            }
        } catch (loadError) {
            setError(loadError.message ?? 'Failed to load vehicles');
        } finally {
            setLoadingVehicles(false);
        }
    }

    async function refreshHistory(nextVehicleId) {
        if (!nextVehicleId) {
            setHistory([]);
            return;
        }

        setLoadingHistory(true);

        try {
            const nextHistory = await listVehicleServiceHistory(userId, nextVehicleId);
            setHistory(nextHistory);
        } catch (loadError) {
            setError(loadError.message ?? 'Failed to load service history');
        } finally {
            setLoadingHistory(false);
        }
    }

    useEffect(() => {
        refreshVehicles();
    }, []);

    useEffect(() => {
        refreshHistory(vehicleId);
    }, [vehicleId]);

    useEffect(() => {
        if (!selectedVehicle) {
            return;
        }

        setMileage(String(selectedVehicle.currentMileage));
    }, [selectedVehicle?.id]);

    async function handleSubmit(event) {
        event.preventDefault();
        setError('');
        setSuccessMessage('');

        const numericMileage = Number.parseInt(mileage, 10);

        if (!Number.isFinite(numericMileage) || numericMileage < 0) {
            setError('Mileage must be a non-negative number');
            return;
        }

        if (!vehicleId) {
            setError('Select a vehicle first');
            return;
        }

        try {
            await logService(userId, vehicleId, serviceName, numericMileage, serviceDate);
            setSuccessMessage('Service entry logged successfully.');
            await refreshVehicles();
            await refreshHistory(vehicleId);
        } catch (saveError) {
            setError(saveError.message ?? 'Failed to log service');
        }
    }

    return (
        <div className="page-wrap">
            <div className="dashboard-wrap">
                <Sidebar/>
                <div className="dashboard-main">
                    <section className="dashboard-form-section">
                        <div className="container-lg">
                            <form onSubmit={handleSubmit}>
                                <h1>Log Service</h1>
                                <div className="form-wrap">
                                    <div className="input-wrap">
                                        <label htmlFor="vehicle">Vehicle</label>
                                        <select
                                            id="vehicle"
                                            value={vehicleId}
                                            onChange={(event) => setVehicleId(event.target.value)}
                                            disabled={loadingVehicles || vehicles.length === 0}
                                        >
                                            {vehicles.length === 0 ?
                                                <option value="">No vehicles available</option> : null}
                                            {vehicles.map((vehicle) => (
                                                <option key={vehicle.id} value={vehicle.id}>
                                                    {vehicle.year} {vehicle.make} {vehicle.model}
                                                </option>
                                            ))}
                                        </select>
                                    </div>

                                    <div className="input-wrap">
                                        <label htmlFor="serviceName">Service</label>
                                        <select
                                            id="serviceName"
                                            value={serviceName}
                                            onChange={(event) => setServiceName(event.target.value)}
                                        >
                                            {SERVICE_NAMES.map((name) => (
                                                <option key={name} value={name}>{name}</option>
                                            ))}
                                        </select>
                                    </div>

                                    <div className="input-wrap">
                                        <label htmlFor="mileage">Mileage</label>
                                        <input
                                            id="mileage"
                                            type="number"
                                            min="0"
                                            value={mileage}
                                            onChange={(event) => setMileage(event.target.value)}
                                            required
                                        />
                                    </div>

                                    <div className="input-wrap">
                                        <label htmlFor="serviceDate">Date</label>
                                        <input
                                            id="serviceDate"
                                            type="date"
                                            value={serviceDate}
                                            onChange={(event) => setServiceDate(event.target.value)}
                                            required
                                        />
                                    </div>
                                </div>
                                <button className="button" type="submit"
                                        disabled={loadingVehicles || vehicles.length === 0}>Log Service
                                </button>
                            </form>
                        </div>
                    </section>
                    <section className="vehicle-list-section">
                        <h2>Service History</h2>

                        {loadingHistory ? <p>Loading history...</p> : null}

                        {!loadingHistory && history.length === 0 ?
                            <p>No service records for this vehicle yet.</p> : null}
                        {!loadingHistory && history.length > 0 ? (
                            <ul className="vehicle-list-wrap">
                                {history.map((record) => (
                                    <li className="vehicle-list-item" key={record.id}>
                                        {record.date}: {record.serviceName} at {record.mileage} mi
                                    </li>
                                ))}
                            </ul>
                        ) : null}
                    </section>

                    {error ? <p>{error}</p> : null}
                    {successMessage ? <p>{successMessage}</p> : null}

                </div>
            </div>
        </div>

    );
}

export default LogServicePage;
