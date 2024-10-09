import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

interface ConfirmDeleteModalProps {
    show: boolean;
    handleClose: () => void;
    handleConfirm: () => void;
}

const ModalEliminar: React.FC<ConfirmDeleteModalProps> = ({ show, handleClose, handleConfirm }) => {
    return (
        <div
            className="modal show"
            style={{ display: 'block', position: 'initial' }}
        >
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>¿Seguro que quiere eliminar el libro?</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <p>Si lo elimina, los alumnos y docentes que lo requieran para sus actividades, no podrán acceder a él.</p>
                </Modal.Body>

                <Modal.Footer>
                    <Button className='mx-auto' variant="secondary" onClick={handleClose}>Cancelar</Button>
                    <Button className='mx-auto' variant="danger" onClick={handleConfirm}>Aceptar</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}

export default ModalEliminar;