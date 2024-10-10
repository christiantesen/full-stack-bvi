import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { Libro } from '../types/Libro';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { Container } from 'react-bootstrap';


// Crear una instancia del mock de axios
const mock = new MockAdapter(axios);

// Simular obtener un libro
mock.onGet(/\/api\/libros\/\d+/).reply((config) => {
  const id = config.url?.split('/').pop();
  return [
    200,
    {
      _id: id,
      carrera: 'Ingeniería de Software',
      plan: '2021',
      ciclo: 'VIII',
      curso: 'Sistemas Distribuidos',
      autor: 'John Doe',
      titulo: 'Programación Distribuida',
      lugar: 'Lima',
      tipo: 'Libro de texto',
      categoria: 'Tecnología',
      enlace: 'http://ejemplo.com/libro.pdf',
      portada: 'http://ejemplo.com/portada.jpg',
      sugeridoPorProfesor: 'Sí',
    },
  ];
});

// Simular la creación de un libro
mock.onPost('/api/libros').reply(201, {
  message: 'Libro creado correctamente (fake)',
});

// Simular la actualización de un libro
mock.onPut(/\/api\/libros\/\d+/).reply(200, {
  message: 'Libro actualizado correctamente (fake)',
});

const CrearLibro: React.FC = () => {
  const { id } = useParams<{ id: string }>(); // Check this line for correct TypeScript syntax
  const navigate = useNavigate();
  const [validated, setValidated] = useState(false);

  const [libro, setLibro] = useState<Libro>({
    _id: '',
    carrera: '',
    plan: '',
    ciclo: '',
    curso: '',
    autor: '',
    titulo: '',
    lugar: '',
    tipo: '',
    categoria: '',
    enlace: '',
    portada: '',
    sugeridoPorProfesor: '',
  });

  useEffect(() => {
    if (id) {
      obtenerLibro(id);
    }
  }, [id]);

  const obtenerLibro = async (valorId: string) => {
    try {
      const res = await axios.get(`http://localhost:4000/api/libros/${valorId}`);
      if (res.data) {
        setLibro({
          _id: valorId,
          carrera: res.data.carrera || '',
          plan: res.data.plan || '',
          ciclo: res.data.ciclo || '',
          curso: res.data.curso || '',
          autor: res.data.autor || '',
          titulo: res.data.titulo || '',
          lugar: res.data.lugar || '',
          tipo: res.data.tipo || '',
          categoria: res.data.categoria || '',
          enlace: res.data.enlace || '',
          portada: res.data.portada || '',
          sugeridoPorProfesor: res.data.sugeridoPorProfesor || '',
        });
      } else {
        console.error('No se encontraron datos para el libro con id:', valorId);
      }
    } catch (error) {
      console.error('Error al obtener el libro:', error);
    }
  };

  const capturarDatos = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLibro({ ...libro, [name]: value });
  };


  const handleSubmit = async (event: any) => {
    const form = event.currentTarget;
    setValidated(true);
    event.preventDefault();

    if (form.checkValidity() === false) {
      event.stopPropagation();
    } else {
      try {
        if (id) {
          await axios.put(`http://localhost:4000/api/libros/${id}`, libro);
          alert('Libro actualizado correctamente');
        } else {
          await axios.post('http://localhost:4000/api/libros', libro);
          alert('Libro creado correctamente');
        }
        navigate('/');
      } catch (error) {
        console.error('Error al guardar el libro:', error);
        alert('Error al guardar el libro');
      }
    }
  };


  return (
    <Container>
      <h2>{id ? 'Editar Libro' : 'Agregar Libro'}</h2>
      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        
        <Row className="mb-3">
          <Form.Group as={Col} md="6" controlId="formCarrera">
            <Form.Label>Carrera</Form.Label>
            <Form.Control
              as="select"
              name="carrera"
              onChange={capturarDatos}
              value={libro.carrera}
              required
            >
              <option value="">Seleccionar Carrera</option>
              <option value="INFORMÁTICA">INFORMÁTICA</option>
              <option value="CIVIL">CIVIL</option>
              <option value="INDUSTRIAL">INDUSTRIAL</option>
              <option value="ELECTRÓNICA">ELECTRÓNICA</option>
              <option value="MECATRÓNICA">MECATRÓNICA</option>
            </Form.Control>
            <Form.Control.Feedback type="invalid">
              Por favor, seleccione una carrera.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} md="6" controlId="formPlan">
            <Form.Label>Plan</Form.Label>
            <Form.Control
              as="select"
              name="plan"
              onChange={capturarDatos}
              value={libro.plan}
              required
            >
              <option value="">Seleccionar Plan</option>
              <option value="2015-II">2015-II</option>
              <option value="2024-I">2024-I</option>
            </Form.Control>
            <Form.Control.Feedback type="invalid">
              Por favor, seleccione un plan.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} md="6" controlId="formCiclo">
            <Form.Label>Semestre</Form.Label>
            <Form.Control
              as="select"
              name="ciclo"
              onChange={capturarDatos}
              value={libro.ciclo}
              required
            >
              <option value="">Seleccionar Semestre</option>
              {Array.from({ length: 10 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>
                  {num}
                </option>
              ))}
            </Form.Control>
            <Form.Control.Feedback type="invalid">
              Por favor, seleccione un semestre.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} md="6" controlId="formCurso">
            <Form.Label>Curso</Form.Label>
            <Form.Control
              type="text"
              placeholder="Curso"
              name="curso"
              onChange={capturarDatos}
              value={libro.curso}
              required
            />
            <Form.Control.Feedback type="invalid">
              Por favor, ingrese el nombre del curso.
            </Form.Control.Feedback>
          </Form.Group>
        </Row>

        <Row className="mb-3">
          <Form.Group as={Col} md="6" controlId="formTitulo">
            <Form.Label>Título</Form.Label>
            <Form.Control
              type="text"
              placeholder="Título"
              name="titulo"
              onChange={capturarDatos}
              value={libro.titulo}
              required
            />
            <Form.Control.Feedback type="invalid">
              Por favor, ingrese el título del libro.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} md="6" controlId="formAutor">
            <Form.Label>Autor y Año</Form.Label>
            <Form.Control
              type="text"
              placeholder="Autor. (año)"
              name="autor"
              onChange={capturarDatos}
              value={libro.autor}
              required
            />
            <Form.Control.Feedback type="invalid">
              Por favor, ingrese el autor y año de publicación.
            </Form.Control.Feedback>
          </Form.Group>
        </Row>

        <Row className="mb-3">
          <Form.Group as={Col} md="6" controlId="formLugar">
            <Form.Label>Lugar</Form.Label>
            <Form.Control
              type="text"
              placeholder="Editorial, País"
              name="lugar"
              onChange={capturarDatos}
              value={libro.lugar}
              required
            />
            <Form.Control.Feedback type="invalid">
              Por favor, ingrese el lugar de publicación.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} md="6" controlId="formCategoria">
            <Form.Label>Categoría</Form.Label>
            <Form.Control
              type="text"
              placeholder="Libro, Monografía, Artículo..."
              name="categoria"
              onChange={capturarDatos}
              value={libro.categoria}
              required
            />
            <Form.Control.Feedback type="invalid">
              Por favor, ingrese la categoría del documento.
            </Form.Control.Feedback>
          </Form.Group>
        </Row>

        <Row className="mb-3">
          <Form.Group as={Col} md="6" controlId="formTipo">
            <Form.Label>Tipo</Form.Label>
            <Form.Control
              type="text"
              placeholder="Documento PDF, página web..."
              name="tipo"
              onChange={capturarDatos}
              value={libro.tipo}
              required
            />
            <Form.Control.Feedback type="invalid">
              Por favor, ingrese el tipo de documento.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} controlId="formProfesor">
            <Form.Label>Sugerido por profesor(es):</Form.Label>
            <Form.Control
              type="text"
              placeholder="Profesor que sugiere el libro"
              name="sugeridoPorProfesor"
              onChange={capturarDatos}
              value={libro.sugeridoPorProfesor}
            />
            <Form.Control.Feedback type="invalid">
              Ingrese profesor(es) que sugiere(n) el libro.
            </Form.Control.Feedback>
          </Form.Group>
        </Row>

        <Row className="mb-3">
          <Form.Group as={Col} controlId="formEnlace">
            <Form.Label>Enlace</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enlace de acceso al libro"
              name="enlace"
              onChange={capturarDatos}
              value={libro.enlace}
              required
            />
            <Form.Control.Feedback type="invalid">
              Por favor, ingrese el enlace de acceso al libro.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group as={Col} controlId="formPortada">
            <Form.Label>Portada</Form.Label>
            <Form.Control
              type="text"
              placeholder="Portada del libro"
              name="portada"
              onChange={capturarDatos}
              value={libro.portada}
            />
            <Form.Control.Feedback type="invalid">
              Ingrese portada del libro.
            </Form.Control.Feedback>
          </Form.Group>
        </Row>

        <Button type="submit">{id ? 'Actualizar' : 'Guardar'}</Button>
      </Form>
    </Container>
  );
};

export default CrearLibro;