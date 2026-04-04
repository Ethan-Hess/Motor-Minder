import {RouterProvider} from 'react-router-dom';
import {appRouter} from './app/router.jsx';
import {AuthProvider} from './context/AuthContext.jsx';

function App() {
    return (
        <AuthProvider>
            <RouterProvider router={appRouter}/>
        </AuthProvider>
    );
}

export default App;
