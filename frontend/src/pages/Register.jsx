import React, { useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import { Link } from 'react-router-dom';
import MockAdapter from 'axios-mock-adapter';

const mock = new MockAdapter(axios);

const Register = () => {
  const [formData, setFormData] = useState({
    nombre: '',
    carrera: '',
    ciclo: '',
    codigo: '',
    email: '',
    password: '',
    role: 'alumno'
  });
  const [error, setError] = useState('');

  const { nombre, carrera, ciclo, codigo, email, password } = formData;

  // Simulación de la respuesta del API al registrar un usuario
  useEffect(() => {
    mock.onPost('http://localhost:4000/api/usuarios').reply(config => {
      const { nombre, carrera, ciclo, codigo, email, password } = JSON.parse(config.data);
      // Simula la lógica de validación del registro
      if (codigo === '' || email === '') {
        return [400, { msg: 'Código y email son requeridos' }];
      }

      return [201, { msg: 'Registrado exitosamente' }];
    });
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
        await axios.post('http://localhost:4000/api/usuarios', formData); // Envía formData directamente
        setError('Registrado exitosamente'); // Si no hay error, muestra el mensaje de éxito
    } catch (error) {
        setError('Error al registrar, intente nuevamente'); // Si hay error, muestra un mensaje de error
    }
};

  return (
    <Container>
      <h2>Registro</h2>
      <Form onSubmit={handleSubmit}>
        <Row className="mb-3">
          <Form.Group as={Col} md="6" controlId="formNombre">
            <Form.Label>Nombre</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ingrese su nombre"
              name="nombre"
              value={nombre}
              onChange={handleChange}
              required
            />
          </Form.Group>
          <Form.Group as={Col} md="6" controlId="formCarrera">
            <Form.Label>Carrera</Form.Label>
            <Form.Control
              as="select"
              name="carrera"
              value={carrera}
              onChange={handleChange}
              required
            >
              <option value="">Seleccionar Carrera</option>
              <option value="INFORMÁTICA">INFORMÁTICA</option>
              <option value="CIVIL">CIVIL</option>
              <option value="INDUSTRIAL">INDUSTRIAL</option>
              <option value="ELECTRÓNICA">ELECTRÓNICA</option>
              <option value="MECATRÓNICA">MECATRÓNICA</option>
            </Form.Control>
          </Form.Group>

          <Form.Group as={Col} md="6" controlId="formCiclo">
            <Form.Label>Ciclo</Form.Label>
            <Form.Control
              as="select"
              name="ciclo"
              value={ciclo}
              onChange={handleChange}
              required
            >
              <option value="">Seleccionar Ciclo</option>
              {Array.from({ length: 10 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>
                  {num}
                </option>
              ))}
            </Form.Control>
          </Form.Group>
        </Row>

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

          <Form.Group as={Col} md="6" controlId="formEmail">
            <Form.Label>Correo electrónico</Form.Label>
            <Form.Control
              type="email"
              placeholder="Ingrese su correo electrónico"
              name="email"
              value={email}
              onChange={handleChange}
              required
            />
          </Form.Group>
        </Row>

        <Row className="mb-3">
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
          Registrarse
        </Button>
        <p className="mt-3">¿Ya tienes una cuenta? <Link to="/login">Inicia Sesión aquí</Link></p>
      </Form>

      {error && <p>{error}</p>}
    </Container>
  );
};

export default Register;