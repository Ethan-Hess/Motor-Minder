import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext.jsx';
import {
  addVehicle,
  editVehicle,
  listVehicles,
  removeVehicle,
} from '../services/vehicleService.js';

function VehiclesPage() {
  const { uid: userId } = useAuth();
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [currentMileage, setCurrentMileage] = useState('');

  async function refreshVehicles() {
    setLoading(true);
    setError('');

    try {
      const nextVehicles = await listVehicles(userId);
      setVehicles(nextVehicles);
    } catch (loadError) {
      setError(loadError.message ?? 'Failed to load vehicles');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refreshVehicles();
  }, []);

  async function handleAddVehicle(event) {
    event.preventDefault();
    setError('');

    try {
      await addVehicle(userId, {
        make,
        model,
        year: Number.parseInt(year, 10),
        currentMileage: Number.parseInt(currentMileage, 10),
      });

      setMake('');
      setModel('');
      setYear('');
      setCurrentMileage('');

      await refreshVehicles();
    } catch (saveError) {
      setError(saveError.message ?? 'Failed to add vehicle');
    }
  }

  async function handleEditVehicle(vehicle) {
    setError('');

    const nextMake = window.prompt('Make', vehicle.make);
    if (nextMake === null) return;

    const nextModel = window.prompt('Model', vehicle.model);
    if (nextModel === null) return;

    const nextYearInput = window.prompt('Year', String(vehicle.year));
    if (nextYearInput === null) return;

    const nextMileageInput = window.prompt('Current Mileage', String(vehicle.currentMileage));
    if (nextMileageInput === null) return;

    const nextYear = Number.parseInt(nextYearInput, 10);
    const nextMileage = Number.parseInt(nextMileageInput, 10);

    if (!Number.isFinite(nextYear) || !Number.isFinite(nextMileage)) {
      setError('Year and mileage must be valid numbers');
      return;
    }

    try {
      await editVehicle(userId, vehicle.id, {
        ...vehicle,
        make: nextMake,
        model: nextModel,
        year: nextYear,
        currentMileage: nextMileage,
      });
      await refreshVehicles();
    } catch (updateError) {
      setError(updateError.message ?? 'Failed to update vehicle');
    }
  }

  async function handleDeleteVehicle(vehicle) {
    setError('');

    const confirmed = window.confirm(`Delete ${vehicle.year} ${vehicle.make} ${vehicle.model}?`);
    if (!confirmed) return;

    try {
      await removeVehicle(userId, vehicle.id);
      await refreshVehicles();
    } catch (deleteError) {
      setError(deleteError.message ?? 'Failed to delete vehicle');
    }
  }

  return (
    <main>
      <h1>Vehicles</h1>


      <form onSubmit={handleAddVehicle}>
        <h2>Add Vehicle</h2>
        <div>
          <label htmlFor="make">Make</label>
          <input id="make" value={make} onChange={(event) => setMake(event.target.value)} required />
        </div>
        <div>
          <label htmlFor="model">Model</label>
          <input id="model" value={model} onChange={(event) => setModel(event.target.value)} required />
        </div>
        <div>
          <label htmlFor="year">Year</label>
          <input
            id="year"
            type="number"
            min="1886"
            value={year}
            onChange={(event) => setYear(event.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="currentMileage">Current Mileage</label>
          <input
            id="currentMileage"
            type="number"
            min="0"
            value={currentMileage}
            onChange={(event) => setCurrentMileage(event.target.value)}
            required
          />
        </div>
        <button type="submit">Add Vehicle</button>
      </form>

      <section>
        <h2>Vehicle List</h2>
        {loading ? <p>Loading vehicles...</p> : null}
        {!loading && vehicles.length === 0 ? <p>No vehicles found.</p> : null}

        {!loading && vehicles.length > 0 ? (
          <ul>
            {vehicles.map((vehicle) => (
              <li key={vehicle.id || `${vehicle.make}-${vehicle.model}-${vehicle.year}`}>
                {vehicle.year} {vehicle.make} {vehicle.model} (Odometer: {vehicle.currentMileage})
                {' '}
                <button type="button" onClick={() => handleEditVehicle(vehicle)}>
                  Edit
                </button>
                {' '}
                <button type="button" onClick={() => handleDeleteVehicle(vehicle)}>
                  Delete
                </button>
              </li>
            ))}
          </ul>
        ) : null}
      </section>

      {error ? <p>{error}</p> : null}
    </main>
  );
}

export default VehiclesPage;
