import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import HomePage from "../pages/HomePage.jsx";
import DashboardPage from '../pages/DashboardPage.jsx';
import LoginPage from '../pages/LoginPage.jsx';
import LogServicePage from '../pages/LogServicePage.jsx';
import MechanicsPage from '../pages/MechanicsPage.jsx';
import SignupPage from '../pages/SignupPage.jsx';
import VehiclesPage from '../pages/VehiclesPage.jsx';

function RequireAuth({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export const appRouter = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />
    },
  { path: '/login', element: <LoginPage /> },
  { path: '/signup', element: <SignupPage /> },
  {
    path: '/',
    element: <RequireAuth><DashboardPage /></RequireAuth>,
  },
  {
    path: '/vehicles',
    element: <RequireAuth><VehiclesPage /></RequireAuth>,
  },
  {
    path: '/log-service',
    element: <RequireAuth><LogServicePage /></RequireAuth>,
  },
  {
    path: '/mechanics',
    element: <RequireAuth><MechanicsPage /></RequireAuth>,
  },
]);
