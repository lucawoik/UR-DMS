import Login from './pages/Login'

import AbstractPage from './components/AbstractPage'
import Dashboard from "./pages/Dashboard";

const authorized = false;

const App = () => {
  return (
    <AbstractPage>
        {authorized ? <></>  : <Login />}
        <Dashboard />
    </AbstractPage>
  );
}

export default App;
