import React, { useState, useEffect } from "react";
import axios from 'axios';
import jwtDecode from "jwt-decode";
import Libro from "../components/Libro";
import Busqueda from "../components/Busqueda";
import Paginacion from "../components/Paginacion";
import FiltroCarrera from "../components/FiltroCarrera";
import FiltroCiclo from "../components/FiltroCiclo";
import ModalEliminar from "../components/ModalEliminarLibro";
import '../styles/ListaLibros.css'; // Asegúrate de tener el archivo CSS correctamente importado

// Crear instancia del mock de Axios
const mock = new MockAdapter(axios);

// Simular obtener lista de libros
mock.onGet('http://localhost:4000/api/libros').reply(200, [
  { _id: '1', titulo: 'Libro A', autor: 'Autor 1', carrera: 'Ingeniería', ciclo: 'VI', lugar: 'Lima', tipo: 'Texto', curso: 'Algoritmos', categoria: 'Ciencia' },
  { _id: '2', titulo: 'Libro B', autor: 'Autor 2', carrera: 'Medicina', ciclo: 'IV', lugar: 'Cusco', tipo: 'Referencia', curso: 'Anatomía', categoria: 'Salud' },
  // Agrega más libros si es necesario
]);

// Simular eliminar libro
mock.onDelete(/\/api\/libros\/\d+/).reply(200, {
  message: 'Libro eliminado correctamente (fake)',
});

// Simular decodificación de token (JWT)
mock.onGet('http://localhost:4000/api/usuario').reply(200, {
  usuario: { nombre: 'Usuario Prueba' }
});


const ListaLibros = () => {
  const [lista, setLista] = useState([]);
  const [mostrarModal, setMostrarModal] = useState(false);
  const [idEliminarLibro, setIdEliminarLibro] = useState(null);
  const [usuario, setUsuario] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [filtroCarrera, setFiltroCarrera] = useState("Todas");
  const [filtroCiclo, setFiltroCiclo] = useState("Todos");
  const [currentPage, setCurrentPage] = useState(1);
  const librosPorPagina = 9; // Número de libros por página

  useEffect(() => {
    const obtenerUsuario = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const decoded = jwtDecode(token);
          setUsuario(decoded.usuario);
        }
      } catch (error) {
        console.error('Error al decodificar el token:', error);
      }
    };
    obtenerUsuario();
  }, []);

  useEffect(() => {
    if (usuario) {
      console.log(`Bienvenido, ${usuario.nombre}`);
      obtenerLibros();
    }
  }, [usuario]);

  const obtenerLibros = async () => {
    try {
      const res = await axios.get('http://localhost:4000/api/libros');
      console.log('Datos obtenidos del servidor:', res.data);
      setLista(res.data);
    } catch (error) {
      console.error("Error al obtener los libros:", error);
    }
  };

  const handleMostrarModal = (id) => {
    setIdEliminarLibro(id);
    setMostrarModal(true);
  };

  const handleCerrarModal = () => {
    setMostrarModal(false);
    setIdEliminarLibro(null);
  };

  const eliminarLibro = async () => {
    if (idEliminarLibro) {
      try {
        await axios.delete(`http://localhost:4000/api/libros/${idEliminarLibro}`);
        setLista(prevLista => prevLista.filter(libro => libro._id !== idEliminarLibro));
      } catch (error) {
        console.error("Error al eliminar el libro:", error);
      } finally {
        handleCerrarModal();
      }
    }
  };

  // Filtrado de libros por búsqueda, carrera y ciclo
  const librosFiltrados = lista.filter(libro => {
    const titulo = libro.titulo ? libro.titulo.toLowerCase() : "";
    const autor = libro.autor ? libro.autor.toLowerCase() : "";
    const lugar = libro.lugar ? libro.lugar.toLowerCase() : "";
    const curso = libro.curso ? libro.curso.toLowerCase() : "";
    const tipo = libro.tipo ? libro.tipo.toLowerCase() : "";
    const categoria = libro.categoria ? libro.categoria.toLowerCase() : "";
    const carrera = libro.carrera ? libro.carrera.toLowerCase() : "";
    const ciclo = libro.ciclo ? libro.ciclo.toLowerCase() : "";

    const busquedaLower = busqueda.toLowerCase();

    return (
      (filtroCarrera === "Todas" || carrera.includes(filtroCarrera.toLowerCase())) &&
      (filtroCiclo === "Todos" || ciclo.includes(filtroCiclo.toLowerCase())) &&
      (titulo.includes(busquedaLower) ||
       autor.includes(busquedaLower) ||
       lugar.includes(busquedaLower) ||
       tipo.includes(busquedaLower) ||
       categoria.includes(busquedaLower) ||
       curso.includes(busquedaLower)
      )
    );
  });

  // Obtener libros actuales según la paginación
  const indexOfLastLibro = currentPage * librosPorPagina;
  const indexOfFirstLibro = indexOfLastLibro - librosPorPagina;
  const librosActuales = librosFiltrados.slice(indexOfFirstLibro, indexOfLastLibro);

  // Cambiar página
  const paginate = pageNumber => setCurrentPage(pageNumber);

  return (
    <div className="lista-libros-container">
      {usuario ? <h2 style={{ marginBottom: '30px' }}>Saludos, {usuario.nombre}</h2> : <h2 style={{ marginBottom: '30px' }}>Saludos.</h2>}
      <Busqueda busqueda={busqueda} setBusqueda={setBusqueda} />
      <FiltroCarrera libros={lista} filtro={filtroCarrera} setFiltro={setFiltroCarrera} />
      <FiltroCiclo libros={lista} filtro={filtroCiclo} setFiltro={setFiltroCiclo} />
      <h2 style={{ marginTop: '30px' }}>Lista de Libros</h2>

      <div className="row">
        {librosActuales.map(libro => (
          <Libro
            key={libro._id}
            libro={libro}
            usuario={usuario}
            handleMostrarModal={handleMostrarModal}
          />
        ))}
      </div>

      <Paginacion
        currentPage={currentPage}
        totalPages={Math.ceil(librosFiltrados.length / librosPorPagina)}
        onPageChange={paginate}
      />

      <ModalEliminar
        show={mostrarModal}
        handleClose={handleCerrarModal}
        handleConfirm={eliminarLibro}
      />
    </div>
  );
};

export default ListaLibros;