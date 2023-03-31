import Login from './pages/Login'

import AbstractPage from './components/AbstractPage'

const authorized = false;

const App = () => {
  return (
    <AbstractPage>
        {authorized ? <></>  : <Login />}
    </AbstractPage>
  );
}

export default App;
