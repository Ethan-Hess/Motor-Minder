import { createBrowserRouter } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage.jsx';
import VehiclesPage from '../pages/VehiclesPage.jsx';
import LogServicePage from '../pages/LogServicePage.jsx';
import MechanicsPage from '../pages/MechanicsPage.jsx';

export const appRouter = createBrowserRouter([
  { path: '/', element: <DashboardPage /> },
  { path: '/vehicles', element: <VehiclesPage /> },
  { path: '/log-service', element: <LogServicePage /> },
  { path: '/mechanics', element: <MechanicsPage /> },
]);
