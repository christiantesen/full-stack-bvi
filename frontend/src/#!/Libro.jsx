import React from "react";
import '../styles/Libros.css'

const Libro = ({ libro, usuario, handleMostrarModal }) => {
  return (
    <div className="libro-container">
      <a href={libro.enlace}><img src={libro.portada ? libro.portada : "https://www.urp.edu.pe/img/thumbnails/wm/451/hm/162/we/451/he/162/x/0/y/0/s/0/q/90/zc/3/f/0/rgb/000000/src/37375/n/logo-urp.png"} alt={libro.titulo} /></a>
      <div className="libro" key={libro._id}>
        <div className="libro-body">
          <a href={libro.enlace}><p className="libro-title">{libro.titulo}</p></a>
          <p className="libro-author">{libro.autor}</p>
          <p className="libro-text">{libro.lugar}</p>
          <p className="libro-text">{libro.tipo}</p>
          <p className="libro-text">{libro.categoria}</p>
        </div>
        <div className="libro-footer">
          {usuario && usuario.role === 'admin' && (
            <>
              <button className="btn btn-danger" onClick={() => handleMostrarModal(libro._id)}>Eliminar libro</button>
              <button className="btn btn-success" onClick={() => window.location.href = `/edit/${libro._id}`}>Editar</button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Libro;