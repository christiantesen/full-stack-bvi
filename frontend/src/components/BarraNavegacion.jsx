import React, { useContext, useEffect, useState } from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';
import { AuthContext } from '../context/AuthContext';
import {jwtDecode} from 'jwt-decode';

const BarraNavegacion = () => {
  const { logout, loggedInUser } = useContext(AuthContext);
  const usuario = loggedInUser

  const handleLogout = () => {
    localStorage.removeItem('token');
    logout();
    window.location.href = '/login';
  };

  return (
    <Navbar expand="lg" className="bg-success mb-3">
      <Container fluid>
        <Navbar.Brand className="text-white" href="#">Estantería Virtual - Biblioteca Virtual de Ingeniería</Navbar.Brand>
        <Navbar.Toggle aria-controls="offcanvasNavbar-expand-lg" />
        <Navbar.Collapse id="navbarNav">
          <Nav className="justify-content-end flex-grow-1">
            {loggedInUser ? (
              <>
                <Nav.Link href="/">Lista de Libros</Nav.Link>
                <Nav.Link href="/mis-libros">Mis Libros</Nav.Link>
                {usuario && usuario.role === 'admin' && (<Nav.Link href="/AgregarLibro">Agregar Libro</Nav.Link>)}
                <Nav.Link onClick={handleLogout}>Cerrar Sesión</Nav.Link>
              </>
            ) : (
              <>
                <Nav.Link href="/Login">Iniciar Sesión</Nav.Link>
                <Nav.Link href="/Register">Registrar</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default BarraNavegacion;