from flask_socketio import emit, join_room, leave_room

# Temporary storage for board state
board = [None] * 9

def register_socket_events(socketio):
    @socketio.on('join_game')
    def on_join_game(data):
        room = data.get('room')  # Room ID for the game session
        join_room(room)
        emit('player_joined', {"message": "A player has joined the room"}, to=room)

    @socketio.on('make_move')
    def on_make_move(data):
        room = data.get('room')
        move = data.get('move')  # The move details sent by the client
        emit('update_board', move, to=room)

        # Logic to check game over
        if check_winner():
            emit('game_over', {'message': 'Player X wins!'}, to=room)

    def check_winner():
        # Check rows, columns, diagonals for a winner
        for i in range(0, 9, 3):
            if board[i] == board[i+1] == board[i+2] != None:
                return True
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] != None:
                return True
        if board[0] == board[4] == board[8] != None:
            return True
        if board[2] == board[4] == board[6] != None:
            return True
        return False

    @socketio.on('leave_game')
    def on_leave_game(data):
        room = data.get('room')
        leave_room(room)
        emit('player_left', {"message": "A player has left the room"}, to=room)
