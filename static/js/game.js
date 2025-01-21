document.addEventListener('DOMContentLoaded', function() {
    const gameBoard = document.getElementById('game-board');
    const gameState = ['','','','','','','','',''];  // Represents a 3x3 Tic-Tac-Toe board

    function renderBoard() {
        gameBoard.innerHTML = '';
        gameState.forEach((cell, index) => {
            const cellDiv = document.createElement('div');
            cellDiv.textContent = cell;
            cellDiv.onclick = () => makeMove(index);
            gameBoard.appendChild(cellDiv);
        });
    }

    function makeMove(index) {
        if (gameState[index] === '') {
            gameState[index] = 'X';  // Player 'X' for simplicity
            renderBoard();
            // Send move to the backend for validation
        }
    }

    renderBoard();
});
