from boggle import Boggle
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.config['SECRET-KEY'] = 'secret-key-boggle'

if 'games_played' not in session:
    session['games_played'] = 0

if 'highest_score' not in session:
    session['highest_score'] = 0

boggle_game = Boggle()


@app.route('/')
def make_board():
    """Renders the game board."""

    board = boggle_game.make_board()
    session['board'] = board

    return render_template('/index', board = board)

@app.route('/check-guess', methods=['POST'])
def check_guess():
    """Checks if word id valid on board and in dictionary."""
    word = request.json.get('word')
    if not boggle_game.is_word_in_dict(word):
        return jsonify(result="not-a-word")
    
    board = session.get('board')
    if not boggle_game.check_valid_word(board, word):
        return jsonify(result="not-on-board")

    return jsonify(result="ok")

@app.route('/end-game', methods=['POST'])
def end_game():
    """Keeps track of how many games have been played and updates the high score."""
    score = request.json.get('score')

    session['games_played'] += 1

    if score > session['highest_score']:
        session['highest_score'] = score

    return jsonify(result="success")