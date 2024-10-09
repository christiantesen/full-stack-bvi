import React, { useContext, useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import MockAdapter from 'axios-mock-adapter';

const mock = new MockAdapter(axios);

const Login = ({ setLoggedInUser }) => {
  const { login } = useContext(AuthContext);
  const [codigo, setCodigo] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false); // Estado de carga
  const navigate = useNavigate();

   // Simulación de las respuestas del API
   useEffect(() => {
    mock.onPost('http://localhost:4000/api/usuarios/login').reply(200, {
      token: 'fake_token',
      usuario: {
        id: 1,
        nombre: 'Juan Perez',
      },
    });

    mock.onGet(/\/api\/usuarios\/login\/.*/).reply(200, {
      usuario: {
        id: 1,
        nombre: 'Juan Perez',
      },
    });
  }, []);

  const handleChange = (e) => {
    if (e.target.name === 'codigo') {
      setCodigo(e.target.value);
    } else if (e.target.name === 'password') {
      setPassword(e.target.value);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); // Activar el estado de carga
  
    try {
      const res = await axios.post('http://localhost:4000/api/usuarios/login', { codigo, password });
      localStorage.setItem('token', res.data.token);
      
      // Hacer una solicitud GET para obtener los datos del usuario
      const token = res.data.token;
      const userDataRes = await axios.get(`http://localhost:4000/api/usuarios/login/${token}`);
      setLoggedInUser(userDataRes.data);
      login(userDataRes.data.usuario);
      navigate('/'); // Redirige al usuario a la lista de libros después del inicio de sesión exitoso
  
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          setError(error.response.data.msg);
        } else if (error.request) {
          setError('No se recibió respuesta del servidor.');
        } else {
          setError('Error al iniciar sesión.');
        }
      }
    } finally {
      setLoading(false); // Desactivar el estado de carga cuando finaliza la solicitud
    }
  };
  

  return (
    <Container>
      <h2>Iniciar Sesión</h2>
      {loading ? ( // Mostrar mensaje de carga si se está cargando
        <p>Cargando...</p>
      ) : (
        <Form onSubmit={handleSubmit}>
          <Row className="mb-3">
            <Form.Group as={Col} md="6" controlId="formCodigo">
              <Form.Label>Código</Form.Label>
              <Form.Control
                type="text"
                placeholder="Ingrese su código"
                name="codigo"
                value={codigo}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group as={Col} md="6" controlId="formPassword">
              <Form.Label>Contraseña</Form.Label>
              <Form.Control
                type="password"
                placeholder="Ingrese su contraseña"
                name="password"
                value={password}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Row>
          <Button variant="primary" type="submit">
            Iniciar Sesión
          </Button>
          <p className="mt-3">¿No tienes una cuenta? <Link to="/register">Regístrate aquí</Link></p>
        </Form>
      )}
      {error && <p>{error}</p>}
    </Container>
  );
};

export default Login;