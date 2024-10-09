import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ListaLibros from './pages/ListaLibros';
import AgregarLibro from './pages/AgregarLibro';
import BarraNavegacion from './components/BarraNavegacion';
import Login from './pages/Login';
import Register from './pages/Register';
import { AuthProvider } from './context/AuthContext';
import { jwtDecode } from 'jwt-decode';
import { DecodedToken } from './types/DecodedToken';
import { useState } from 'react';
import MisLibros from './pages/MisLibros';

function App() {
  const [loggedInUser, setLoggedInUser] = useState<DecodedToken['usuario'] | null>(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded: DecodedToken = jwtDecode(token);
        return decoded.usuario;
      } catch (error) {
        console.error('Error al decodificar el token:', error);
        return null;
      }
    }
    return null;
  });

  return (
    <AuthProvider>
      <Router>
        <>
          <BarraNavegacion />
          <div className='container'>
            <Routes>
              <Route path="/" element={loggedInUser ? <ListaLibros /> : <Navigate to="/login" />} />
              <Route path="/AgregarLibro" element={loggedInUser ? <AgregarLibro /> : <Navigate to="/login" />} />
              <Route path="/login" element={<Login setLoggedInUser={setLoggedInUser} />} />
              <Route path="/register" element={<Register />} />
              <Route path="/edit/:id" element={<AgregarLibro />} />
              <Route path="/mis-libros" element={<MisLibros />} />
            </Routes>
          </div>
        </>
      </Router>
    </AuthProvider>
  );
}

export default App;