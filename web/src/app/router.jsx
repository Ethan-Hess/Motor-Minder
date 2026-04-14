import {createBrowserRouter, Navigate, useLocation, useRouteError} from 'react-router-dom';
import {useAuth} from '../context/AuthContext.jsx';
import HomePage from "../pages/HomePage.jsx";
import DashboardPage from '../pages/DashboardPage.jsx';
import LoginPage from '../pages/LoginPage.jsx';
import LogServicePage from '../pages/LogServicePage.jsx';
import MechanicsPage from '../pages/MechanicsPage.jsx';
import SignupPage from '../pages/SignupPage.jsx';
import VehiclesPage from '../pages/VehiclesPage.jsx';

function RequireAuth({children}) {
    const {user, loading} = useAuth();
    const location = useLocation();

    if (loading) {
        return <p>Loading...</p>;
    }

    if (!user) {
        return <Navigate to="/login" state={{from: location}} replace/>;
    }

    return children;
}

function RouteError() {
    const error = useRouteError();
    return (
        <div>
            <h1>Something went wrong</h1>
            <p>{error?.statusText ?? error?.message ?? 'An unexpected error occurred.'}</p>
            <a href="/">Go home</a>
        </div>
    );
}

export const appRouter = createBrowserRouter([
    {
        errorElement: <RouteError/>,
        children: [
            {
                path: "/",
                element: <HomePage/>
            },
            {
                path: '/login',
                element: <LoginPage/>
            },
            {
                path: '/signup',
                element: <SignupPage/>
            },
            {
                path: '/dashboard',
                element: <RequireAuth><DashboardPage/></RequireAuth>,
            },
            {
                path: '/vehicles',
                element: <RequireAuth><VehiclesPage/></RequireAuth>,
            },
            {
                path: '/log-service',
                element: <RequireAuth><LogServicePage/></RequireAuth>,
            },
            {
                path: '/mechanics',
                element: <RequireAuth><MechanicsPage/></RequireAuth>,
            },
            {
                path: '*',
                element: <Navigate to="/" replace/>,
            },
        ]
    }
]);
