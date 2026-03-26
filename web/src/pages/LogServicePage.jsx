import { useEffect, useMemo, useState } from 'react';
import { auth } from '../lib/firebase.js';
import { logService, listVehicleServiceHistory } from '../services/serviceLogService.js';
import { listVehicles } from '../services/vehicleService.js';
import { SERVICE_NAMES } from '../types/domain.js';

const DEV_USER_ID = 'dev-local-user';

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

  const userId = auth.currentUser?.uid ?? DEV_USER_ID;

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
    <main>
      <h1>Log Service</h1>
      <p>Signed-in user ID is used when available; fallback is <strong>{DEV_USER_ID}</strong>.</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="vehicle">Vehicle</label>
          <select
            id="vehicle"
            value={vehicleId}
            onChange={(event) => setVehicleId(event.target.value)}
            disabled={loadingVehicles || vehicles.length === 0}
          >
            {vehicles.length === 0 ? <option value="">No vehicles available</option> : null}
            {vehicles.map((vehicle) => (
              <option key={vehicle.id} value={vehicle.id}>
                {vehicle.year} {vehicle.make} {vehicle.model}
              </option>
            ))}
          </select>
        </div>

        <div>
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

        <div>
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

        <div>
          <label htmlFor="serviceDate">Date</label>
          <input
            id="serviceDate"
            type="date"
            value={serviceDate}
            onChange={(event) => setServiceDate(event.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={loadingVehicles || vehicles.length === 0}>Log Service</button>
      </form>

      <section>
        <h2>Service History</h2>
        {loadingHistory ? <p>Loading history...</p> : null}
        {!loadingHistory && history.length === 0 ? <p>No service records for this vehicle yet.</p> : null}

        {!loadingHistory && history.length > 0 ? (
          <ul>
            {history.map((record) => (
              <li key={record.id}>
                {record.date}: {record.serviceName} at {record.mileage} mi
              </li>
            ))}
          </ul>
        ) : null}
      </section>

      {error ? <p>{error}</p> : null}
      {successMessage ? <p>{successMessage}</p> : null}
    </main>
  );
}

export default LogServicePage;
