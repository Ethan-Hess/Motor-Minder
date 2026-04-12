import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {signUp} from '../services/authService.js';
import Navbar from "../components/Navigation/Navbar.jsx";
import Footer from "../components/Footer/Footer.jsx";

// import Button from "../components/Button/Button.jsx";

function SignupPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();
        setError('');
        setLoading(true);

        try {
            await signUp(email, password);
            navigate('/');
        } catch (err) {
            setError(err.message ?? 'Failed to create account');
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="page-wrap">
            <Navbar/>
            <div className="main-wrap">
                <section className="section-padding-lg">
                    <div className="container-lg">
                        <form onSubmit={handleSubmit}>
                            <div className="form-wrap">
                                <div className="input-wrap">
                                    <label htmlFor="email">Email</label>
                                    <input
                                        id="email"
                                        type="email"
                                        value={email}
                                        onChange={(event) => setEmail(event.target.value)}
                                        required/>
                                </div>
                                <div className="input-wrap">
                                    <label htmlFor="password">Password</label>
                                    <input id="password"
                                           type="password"
                                           value={password}
                                           onChange={(event) => setPassword(event.target.value)}
                                           minLength={6}
                                           required/>
                                </div>
                            </div>
                            <button className="button" type="submit" disabled={loading}>
                                {loading ? 'Creating account...' : 'Sign Up'}
                            </button>
                            <p>Already have an account? <Link to="/login">Login</Link>.</p>
                        </form>
                        {error ? <p>{error}</p> : null}
                    </div>
                </section>
            </div>
            <Footer/>
        </div>
    );
}

export default SignupPage;
