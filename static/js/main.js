document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const startGameBtn = document.getElementById('gameStart');
    const restartBtn = document.getElementById('restartButton');
    const joinForm = document.getElementById('joinForm');
    const gameRoomInput = document.getElementById('gameRoom');
    const playerNameInput = document.getElementById('playerName');
    const connectedPlayers = document.getElementById('connected_players');
    const msgArea = document.getElementById('msg-area');
    const messageInput = document.getElementById('message');
    const sendMsgBtn = document.getElementById('send');
    const gameBoardContainer = document.getElementById('gameBoardContainer');
    let currentPlayer = 'X'; // X starts the game
    let gameMoves = Array(9).fill(null); // To track moves
    let gameActive = false;
    let socket = io(); // Initialize Socket.IO

    let gameRoom = '';
    let playerName = '';

    // Listen for form submission to join the game room
    joinForm.addEventListener('submit', (e) => {
        e.preventDefault();
        gameRoom = gameRoomInput.value.trim();
        playerName = playerNameInput.value.trim();

        if (gameRoom && playerName) {
            socket.emit('joinRoom', { room: gameRoom, playerName });
            joinForm.style.display = 'none'; // Hide form after joining
        }
    });

    // Listen for game updates from the server
    socket.on('gameStart', () => {
        gameActive = true;
        document.querySelector('.greetings').style.display = 'none'; // Hide greetings view
        gameBoardContainer.style.display = 'block'; // Show game board
    });

    socket.on('updatePlayers', (players) => {
        connectedPlayers.innerHTML = `Connected Players: ${players.join(', ')}`;
    });

    function checkWinner() {
        const winningCombos = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ];

        for (const combo of winningCombos) {
            const [a, b, c] = combo;
            if (gameMoves[a] && gameMoves[a] === gameMoves[b] && gameMoves[a] === gameMoves[c]) {
                return gameMoves[a];
            }
        }
        return gameMoves.includes(null) ? null : 'Draw'; // Draw if no winner
    }

    function resetGame() {
        gameMoves.fill(null);
        cells.forEach(cell => {
            cell.textContent = '';
            cell.classList.remove('text-green-500', 'text-red-500');
        });
        gameActive = true;
        currentPlayer = 'X';
    }

    // Start game when the "Start Game" button is clicked
    startGameBtn.addEventListener('click', () => {
        socket.emit('startGame', gameRoom);
        resetGame();
    });

    // Handle cell click events
    cells.forEach((cell, index) => {
        cell.addEventListener('click', () => {
            if (!gameActive || cell.textContent) return;

            // Mark the cell
            cell.textContent = currentPlayer;
            cell.classList.add(currentPlayer === 'X' ? 'text-green-500' : 'text-red-500');
            gameMoves[index] = currentPlayer;

            const result = checkWinner();
            if (result) {
                gameActive = false;
                socket.emit('gameOver', { winner: result, room: gameRoom });
                alert(result === 'Draw' ? "It's a draw!" : `Player ${result} wins!`);
            } else {
                currentPlayer = currentPlayer === 'X' ? 'O' : 'X'; // Toggle player
                socket.emit('playerTurn', { player: currentPlayer, room: gameRoom });
            }
        });
    });

    // Listen for game over event
    socket.on('gameOver', (data) => {
        alert(data.winner === 'Draw' ? "It's a draw!" : `Player ${data.winner} wins!`);
    });

    // Restart the game
    restartBtn.addEventListener('click', () => {
        resetGame();
        socket.emit('restartGame', gameRoom);
    });

    // Handle chat messages
    sendMsgBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            socket.emit('chatMessage', { room: gameRoom, message, player: playerName });
            messageInput.value = '';
        }
    });

    // Listen for incoming chat messages
    socket.on('chatMessage', (data) => {
        const msgDiv = document.createElement('div');
        msgDiv.textContent = `${data.player}: ${data.message}`;
        msgArea.appendChild(msgDiv);
    });
});
