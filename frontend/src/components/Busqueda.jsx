import React from "react";

const Busqueda = ({ busqueda, setBusqueda }) => {
  const handleChange = (e) => {
    setBusqueda(e.target.value);
  };

  return (
    <div>
      <div className="input-group mb-3">
        <div className="input-group-prepend">
          <span className="input-group-text" id="basic-addon3" style={{backgroundColor: '#1a8754', color: '#fff'}}>Buscar</span>
        </div>
        <input
          type="text"
          className="form-control"
          placeholder="Buscar por curso, ciclo, título, autor, año, lugar de publicación..."
          id="basic-url"
          aria-describedby="basic-addon3"
          value={busqueda}
          onChange={handleChange}
        />
      </div>
    </div>
    
  );
};

export default Busqueda;