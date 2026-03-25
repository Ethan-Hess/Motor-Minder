import { Link } from 'react-router-dom';

function DashboardPage() {
  return (
    <main>
      <h1>MotorMinder Dashboard</h1>
      <p>React + Vite + Firebase scaffold is ready.</p>
      <nav>
        <ul>
          <li><Link to="/vehicles">Vehicles</Link></li>
          <li><Link to="/log-service">Log Service</Link></li>
          <li><Link to="/mechanics">Mechanics</Link></li>
        </ul>
      </nav>
    </main>
  );
}

export default DashboardPage;
