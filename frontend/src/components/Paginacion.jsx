import React from 'react';
import { Pagination } from 'react-bootstrap';

const Paginacion = ({ currentPage, totalPages, onPageChange }) => {
  const MAX_PAGES_DISPLAYED = 25; // Número máximo de páginas visibles a la vez

  // Calcula el rango de páginas que se mostrarán
  let startPage = Math.max(1, currentPage - Math.floor(MAX_PAGES_DISPLAYED / 2));
  let endPage = Math.min(totalPages, startPage + MAX_PAGES_DISPLAYED - 1);

  // Ajusta el inicio si el rango está demasiado cerca del final
  if (endPage - startPage + 1 < MAX_PAGES_DISPLAYED) {
    startPage = Math.max(1, endPage - MAX_PAGES_DISPLAYED + 1);
  }

  const pageNumbers = [];
  for (let i = startPage; i <= endPage; i++) {
    pageNumbers.push(i);
  }

  return (
    <Pagination style={{justifyContent: 'center', marginBottom: '20px', marginTop: '20px'}}>
      <Pagination.First onClick={() => onPageChange(1)} disabled={currentPage === 1} />
      <Pagination.Prev onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 1} />
      {startPage > 1 && (
        <>
          <Pagination.Item onClick={() => onPageChange(1)}>1</Pagination.Item>
          {startPage > 2 && <Pagination.Ellipsis />}
        </>
      )}
      {pageNumbers.map(number => (
        <Pagination.Item key={number} active={number === currentPage} onClick={() => onPageChange(number)}>
          {number}
        </Pagination.Item>
      ))}
      {endPage < totalPages && (
        <>
          {endPage < totalPages - 1 && <Pagination.Ellipsis />}
          <Pagination.Item onClick={() => onPageChange(totalPages)}>{totalPages}</Pagination.Item>
        </>
      )}
      <Pagination.Next onClick={() => onPageChange(currentPage + 1)} disabled={currentPage === totalPages} />
      <Pagination.Last onClick={() => onPageChange(totalPages)} disabled={currentPage === totalPages} />
    </Pagination>
  );
};

export default Paginacion;
