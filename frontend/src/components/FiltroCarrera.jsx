import React from "react";
import { Form } from "react-bootstrap";
import { AuthContext } from "../context/AuthContext";
import { useContext } from "react";

const FiltroCarrera = ({ libros, filtro, setFiltro }) => {
    const { loggedInUser } = useContext(AuthContext);
    // console.log(loggedInUser);
    const user = loggedInUser;
    // Obtener todas las carreras disponibles
    const carreras = [...new Set(libros.map(libro => libro.carrera))];

    // Función para manejar el cambio en el selector de carrera
    const handleChange = (event) => {
        setFiltro(event.target.value);
    };

    return (
        <div className="container mt-4">
            <div className="form-group">
                <label htmlFor="carreraSelector">Selecciona una carrera:</label>
                <Form.Select
                    id="carreraSelector"
                    className="form-control"
                    value={filtro} // Usamos filtro en lugar de carreraSeleccionada
                    onChange={handleChange}
                >
                    <option value="Todas">Todas las carreras</option>
                    <option value={user?.carrera}>MI CARRERA  ({user?.carrera})</option>
                    {carreras.map((carrera, index) => (
                        <option key={index} value={carrera}>{carrera}</option>
                    ))}
                </Form.Select>
            </div>
        </div>
    );
};

export default FiltroCarrera;