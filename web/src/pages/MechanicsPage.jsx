import {useState} from 'react';
import {findMechanicByCityState} from '../services/mechanicService.js';
import Sidebar from "../components/Navigation/Sidebar.jsx";

function MechanicsPage() {
    const [city, setCity] = useState('');
    const [stateCode, setStateCode] = useState('');
    const [mechanic, setMechanic] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    async function handleSearch(event) {
        event.preventDefault();
        setError('');
        setMechanic(null);
        setLoading(true);

        try {
            const result = await findMechanicByCityState(city, stateCode);
            setMechanic(result);

            if (!result) {
                setError('No mechanic found for that city and state.');
            }
        } catch (searchError) {
            setError(searchError.message ?? 'Failed to search mechanics');
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="page-wrap">
            <div className="dashboard-wrap">
                <Sidebar/>
                <div className="dashboard-main">
                    <section className="dashboard-form-section">
                        <form>
                            <h1>Manage Vehicles</h1>
                            <div className="form-wrap">
                                <div className="input-wrap">
                                    <label htmlFor="city">City</label>
                                    <input
                                        id="city"
                                        value={city}
                                        onChange={(event) => setCity(event.target.value)}
                                        required
                                    />
                                </div>
                                <div className="input-wrap">
                                    <label htmlFor="stateCode">State</label>
                                    <input
                                        id="stateCode"
                                        value={stateCode}
                                        onChange={(event) => setStateCode(event.target.value)}
                                        maxLength={2}
                                        required
                                    />
                                </div>
                            </div>
                            <button className="button" type="submit" disabled={loading}>Search</button>
                        </form>

                        {loading ? <p>Searching mechanics...</p> : null}

                        {mechanic ? (
                            <section>
                                <h2>{mechanic.name}</h2>
                                <p>
                                    {mechanic.address.address_line_1}
                                    {mechanic.address.address_line_2 ? `, ${mechanic.address.address_line_2}` : ''}
                                    {', '}
                                    {mechanic.address.city}, {mechanic.address.state} {mechanic.address.zip_code}
                                </p>
                                <p>Phone: {mechanic.phone || 'N/A'}</p>
                                <p>Email: {mechanic.email || 'N/A'}</p>
                                <p>Website: {mechanic.website || 'N/A'}</p>
                                <p>Rating: {mechanic.rating || 'N/A'}</p>
                                <p>Appointment Required: {mechanic.appointment_required ? 'Yes' : 'No'}</p>
                            </section>
                        ) : null}

                        {error ? <p>{error}</p> : null}
                    </section>
                </div>
            </div>
        </div>
        //   <form onSubmit={handleSearch}>

        //
        //
        //   </form>
        //

    );
}

export default MechanicsPage;
