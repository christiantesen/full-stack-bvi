import axios from 'axios';
import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import React from 'react';
import { jwtDecode } from 'jwt-decode';
import Card from 'react-bootstrap/Card';
import { Button, Dropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import MockAdapter from 'axios-mock-adapter';

// Creamos una instancia del mock adapter y la asociamos con axios
const mock = new MockAdapter(axios);
// Definimos las respuestas simuladas para las rutas
mock.onPost(/\/api\/usuarios\/\d+\/favoritos/).reply(200, {
    message: 'Libro añadido a favoritos (fake)'
});
mock.onPost(/\/api\/usuarios\/\d+\/masTarde/).reply(200, {
    message: 'Libro añadido a leer más tarde (fake)'
});

const Libro = ({ libro, usuario, handleMostrarModal }) => {
    const { loggedInUser } = useContext(AuthContext);
    // console.log(loggedInUser);
    const user = loggedInUser;
    const colorMapping = {
        "CIVIL": "warning",
        "INFORMÁTICA": "primary",
        "INDUSTRIAL": "success",
        "MECATRÓNICA": "danger",
        "ELECTRÓNICA": "secondary",
    };

    const cardColor = colorMapping[libro.carrera] || "light";

    // Función para añadir a favoritos
    const handleAñadirFavorito = async (libroId) => {
        try {
            const res = await axios.post(`http://localhost:4000/api/usuarios/${user.id}/favoritos`, { libroId });
            console.log('Añadido a favoritos:', res.data);
        } catch (error) {
            console.error('Error al añadir a favoritos:', error);
        }
    };

    // Función para añadir a leer más tarde
    const handleLeerMasTarde = async (libroId) => {
        try {
            const res = await axios.post(`http://localhost:4000/api/usuarios/${user.id}/masTarde`, { libroId });
            console.log('Añadido a leer más tarde:', res.data);
        } catch (error) {
            console.error('Error al añadir a leer más tarde:', error);
        }
    };

    return (
        <div className="col-md p-3 mx-auto" key={libro._id}>
            <Card className="col-md p-3 mx-auto"
                style={{ width: '20rem' }}
                bg={cardColor}
                text={cardColor === 'light' || cardColor === 'warning' ? 'dark' : 'white'}
                border='dark'>
                <Card.Header style={{ display: 'flex' }}>
                    {/* actualizar formato de libro (plan, profesores)*/}
                    INGENIERÍA {libro.carrera} | PLAN: {libro.plan} | CICLO: {libro.ciclo} | CURSO: {libro.curso}
                    <Dropdown>
                        <Dropdown.Toggle variant="dark" id="dropdown-basic"></Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item onClick={() => handleAñadirFavorito(libro._id)}>Agregar a favoritos</Dropdown.Item>
                            <Dropdown.Item onClick={() => handleLeerMasTarde(libro._id)}>Leer más tarde</Dropdown.Item>
                            <Dropdown.Item href="#/action-3">Conseguir libro</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </Card.Header>
                <Card.Img variant="top" style={{ height: '200px', objectFit: 'contain', padding: '10px' }} src={libro.portada ? libro.portada : "https://www.urp.edu.pe/img/thumbnails/wm/451/hm/162/we/451/he/162/x/0/y/0/s/0/q/90/zc/3/f/0/rgb/000000/src/37375/n/logo-urp.png"} />
                <Card.Body className="d-flex flex-column justify-content-around">
                    <Card.Title>{libro.titulo}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">{libro.autor}</Card.Subtitle>
                    <Card.Subtitle>Publicado en: {libro.lugar}</Card.Subtitle>
                    <Card.Text>Clase: {libro.categoria}</Card.Text>
                    {libro.sugeridoPorProfesor ? (<Card.Text>Sugerido por: {libro.sugeridoPorProfesor}</Card.Text>) : ("")}
                    <Card.Link className="mb-3 btn btn-dark border-light" href={libro.enlace}>Lea el libro dando click aquí.</Card.Link>
                    {usuario && usuario.role === 'admin' && (
                        <Card.Footer className="d-flex justify-content-around">
                            <>
                                <Button className="btn btn-danger" onClick={() => handleMostrarModal(libro._id)}>
                                    Eliminar libro
                                </Button>
                                <Link className="btn btn-success" to={`/edit/${libro._id}`}>
                                    Editar
                                </Link>
                            </>
                        </Card.Footer>
                    )}
                </Card.Body>
            </Card>
        </div>
    );
};

export default Libro;