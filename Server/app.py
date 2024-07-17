import logging
import random
from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from models import db, User
from board import Board
from computer import ComputerMove
from movepiece import MovePiece
from models import db, User, GameMove

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '112'  # Secret key for session management
bcrypt = Bcrypt(app)
db.init_app(app)
CORS(app)

logging.basicConfig(filename='game.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing username, email, or password'}), 400

    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({'message': 'Username already exists. Please choose a different one.'}), 409
    elif existing_email:
        return jsonify({'message': 'Email address already registered. Please use a different email.'}), 409
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Account created successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Login unsuccessful. Please check your username and password.'}), 401

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully!'}), 200

@app.route("/profile", methods=['GET'])
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    else:
        return jsonify({'message': 'Authentication required to access this resource.'}), 401

@app.route("/game", methods=['GET', 'POST'])
def play_game():

    if 'board' not in session or check_game_over(session['board']):
        session['board'] = Board().board
        session['player_captures'] = 0
        session['computer_captures'] = 0
        session['last_player_move'] = None
        session['last_computer_move'] = None

    board = session['board']
   

    if request.method == 'GET':
        return jsonify({
            'board': board,
            'player_captures': session['player_captures'],
            'computer_captures': session['computer_captures'],
            'last_player_move': session.get('last_player_move', None),
            'last_computer_move': session.get('last_computer_move', None)
        }), 200

    if request.method == 'POST':
        data = request.get_json()
        start_row = data.get('start_row')
        start_col = data.get('start_col')
        end_row = data.get('end_row')
        end_col = data.get('end_col')

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return jsonify({'message': 'Invalid move. Out of board bounds.'}), 400

        if abs(start_row - end_row) != 1 or abs(start_col - end_col) != 1:
            return jsonify({'message': 'Invalid move. Must be diagonal.'}), 400

        if is_valid_move(board, start_row, start_col, end_row, end_col):
            if abs(start_row - end_row) == 2:
                captured_row = (start_row + end_row) // 2
                captured_col = (start_col + end_col) // 2
                captured_piece = board[captured_row][captured_col]

                if captured_piece == 'p':
                    session['player_captures'] += 1
                elif captured_piece == 'c':
                    session['computer_captures'] += 1

                board[captured_row][captured_col] = ' '

            MovePiece.move_piece(board, board[start_row][start_col], start_row, start_col, end_row, end_col)


            session['board'] = board
            session['last_player_move'] = {'from': {'row': start_row, 'col': start_col}, 'to': {'row': end_row, 'col': end_col}}

            # Log the player's move
            user_id = session.get('user_id')
            if user_id:
                new_move = GameMove(user_id=user_id, start_row=start_row, start_col=start_col,
                                    end_row=end_row, end_col=end_col)
                db.session.add(new_move=new_move)
                db.session.commit()

            if check_game_over(board):
                return jsonify({'message': 'Game over!', 'board': board}), 200

            if check_game_over(board):
                return jsonify({'message': 'Game over!', 'board': board}), 200
    

            # After player's move, computer makes a move
            computer_move = ComputerMove.get_random_computer_move(board)
            if computer_move:
                _, comp_start_row, comp_start_col, comp_end_row, comp_end_col = computer_move

                if abs(comp_start_row - comp_end_row) == 2:
                    captured_row = (comp_start_row + comp_end_row) // 2
                    captured_col = (comp_start_col + comp_end_col) // 2
                    captured_piece = board[captured_row][captured_col]

                    if captured_piece == 'p':
                        session['player_captures'] += 1
                    elif captured_piece == 'c':
                        session['computer_captures'] += 1

                    board[captured_row][captured_col] = ' '

                MovePiece.move_piece(board, board[comp_start_row][comp_start_col], comp_start_row, comp_start_col, comp_end_row, comp_end_col)

                session['board'] = board
                session['last_player_move'] = {'from': {'row': comp_start_row, 'col': comp_start_col}, 'to': {'row': comp_end_row, 'col': comp_end_col}}

                if check_game_over(board):
                    return jsonify({'message': 'Game over!', 'board': board}), 200

            response = {
                'message': 'Move successful',
                'board': board,
                'last_player_move': session.get('last_player_move', None),
                'last_computer_move': session.get('last_computer_move', None),
                'player_captures': session['player_captures'],
                'computer_captures': session['computer_captures']
            }

            return jsonify(response), 200
        else:
            return jsonify({'message': 'Invalid move.'}), 400


@app.route("/reset_game", methods=['POST'])
def reset_game():
    try:
        session['board'] = Board().board
        session['player_captures'] = 0
        session['computer_captures'] = 0
        session['last_player_move'] = None
        session['last_computer_move'] = None
        return jsonify({'message': 'Game reset successfully!', 'board': session['board']}), 200
    except Exception as e:
        logging.error(f"Error resetting game: {str(e)}")
        return jsonify({'message': 'Failed to reset game.'}), 500

def is_valid_move(board, start_row, start_col, end_row, end_col):
    if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
        if board[end_row][end_col] == ' ':
            return True
    elif abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
        captured_row = (start_row + end_row) // 2
        captured_col = (start_col + end_col) // 2
        if board[captured_row][captured_col] in ('p', 'c'):
            return True
    return False

def check_game_over(board):
    player_pieces = 0
    computer_pieces = 0

    for row in board:
        for piece in row:
            if piece == 'p' or piece == 'P':
                player_pieces += 1
            elif piece == 'c' or piece == 'C':
                computer_pieces += 1

    if player_pieces == 0 or computer_pieces == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)
