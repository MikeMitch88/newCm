import React, { useEffect, useState } from 'react';
import Col from './Col';
import backgroundImage from '../assets/image.jpeg';

function Game() {
  const [board, setBoard] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [playerCaptures, setPlayerCaptures] = useState(0);
  const [computerCaptures, setComputerCaptures] = useState(0);
  const [lastPlayerMove, setLastPlayerMove] = useState(null); // Track last player move

  useEffect(() => {
    getBoard();
  }, []);

  // Fetch initial board state from the server
  const getBoard = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/game');
      if (!response.ok) {
        throw new Error('Failed to fetch board');
      }
      const boardData = await response.json();
      setBoard(boardData.board);
      setPlayerCaptures(boardData.player_captures);
      setComputerCaptures(boardData.computer_captures);
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  };

  // Handle cell click event
  const handleCellClick = (rowIndex, colIndex) => {
    // If no cell is selected, select the clicked cell
    if (!selectedCell) {
      setSelectedCell({ row: rowIndex, col: colIndex });
    } else {
      // Otherwise, try to move the piece
      movePiece(selectedCell.row, selectedCell.col, rowIndex, colIndex);
      setSelectedCell(null); // Clear selected cell after move attempt
    }
  };

  // Move piece function
   const movePiece = async (startRow, startCol, endRow, endCol) => {
     try {
      // Validate the move (must be a diagonal move and valid within the board bounds)
      // if (!isValidMove(startRow, startCol, endRow, endCol)) {
      //   console.error('Invalid move');
      //   return;
      // }

      const myHeaders = new Headers();
      myHeaders.append('Content-Type', 'application/json');

      const requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: JSON.stringify({ start_row: startRow, start_col: startCol, end_row: endRow, end_col: endCol }),
        redirect: 'follow',
      };

      const response = await fetch('http://127.0.0.1:5000/game', requestOptions);
      if (!response.ok) {
        throw new Error('Failed to move piece');
      }

      const result = await response.json();
      console.log('Move result:', result);

      // Update the board state with the new board configuration
      setBoard(result.board);
      setPlayerCaptures(result.player_captures);
      setComputerCaptures(result.computer_captures);
      setLastPlayerMove({ from: { row: startRow, col: startCol }, to: { row: endRow, col: endCol } }); // Update last player move
    } catch (error) {
      console.error('Error moving piece:', error);
    }
  };

  // Validate if the move is diagonal and within bounds
  const isValidMove = (startRow, startCol, endRow, endCol) => {
    const diffRow = Math.abs(startRow - endRow);
    const diffCol = Math.abs(startCol - endCol);
    return diffRow === 1 && diffCol === 1; // Diagonal move validation
  };

  return (
    <div
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: 'cover',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div>
        {/* <div>
            <marquee>{username.alias}! Welcome, its fun here.Enjoy</marquee>
        </div> */}
        <div>
          <button className="w3-btn w3-round w3-yellow ">New Game</button>
          <a> <button className="w3-btn w3-round w3-brown w3-margin-left" id="logout" href="/logout">Logout</button></a>
        </div>
      </div>
      <div>
        <h1 style={{ color: 'white', marginBottom: '20px' }}>Checkers Game</h1>
      </div>
      <div>
        <p style={{ color: 'white' }}>Player Captures: {playerCaptures}</p>
        <p style={{ color: 'white' }}>Computer Captures: {computerCaptures}</p>
      </div>
      <div>
        {board.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            {board.map((row, rowIndex) => (
              <div key={rowIndex} style={{ display: 'flex' }}>
                {row.map((cell, colIndex) => (
                  <Col
                    key={colIndex}
                    rowindex={rowIndex}
                    colindex={colIndex}
                    cell={cell}
                    handleClick={handleCellClick}
                    selected={selectedCell && selectedCell.row === rowIndex && selectedCell.col === colIndex}
                    showLastMove={lastPlayerMove && lastPlayerMove.to.row === rowIndex && lastPlayerMove.to.col === colIndex} // Pass showLastMove prop to Col
                  />
                ))}
              </div>
            ))}
          </div>
        ) : ( 
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
}

export default Game;
