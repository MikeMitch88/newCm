import React from 'react';

const Col = ({ rowindex, colindex, cell, handleClick, selected }) => {
  return (
    <div
      className="cell"
      style={{
        width: '50px',
        height: '50px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        border: '1px solid black',
        background: (rowindex % 2 === 0 && colindex % 2 === 0) || (rowindex % 2 === 1 && colindex % 2 === 1) ? '#f0f0f0' : 'brown',
        cursor: 'pointer',
        opacity: selected ? 0.7 : 1,
      }}
      onClick={() => handleClick(rowindex, colindex)}
    >
      {cell}
    </div>
  );
};

export default Col;
