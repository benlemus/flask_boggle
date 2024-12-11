from boggle import Boggle
from flask import Flask, render_template, session, jsonify, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydogmilo03'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.debug = True
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

app.highscore = {}

@app.route('/')
def show_board(): 
    '''Uses boggle.py class to create game board, creates flask session storage variables on first load and shows the game board'''

    if 'board' not in session:
        game_board = boggle_game.make_board()
        session['board'] = game_board
        session['result'] = ''
        session['points'] = 0
        session['highscores'] = {}
        session['game_num'] = 1
    
    return render_template('game.html', board=session['board'])

def get_points(guess, result):
    '''Returns the amount of points given to a correct answer.'''

    if result == 'ok':
        return len(guess)
    else:
        return 0

@app.route('/handle-form', methods=["POST"])
def handle_form():
    '''Starts a 60 second countdown and ends guessing when 0.'''

    guess = request.json.get('guess')
    session['result'] = boggle_game.check_valid_word(session['board'], guess)

    session['points'] += get_points(guess, session['result'])
    
    return jsonify({'result': session['result'], 'points': session['points']}) 

@app.route('/update-highscores')
def get_highscores():
    '''Sorts global list of highscores and sends top 5 highscores to app.js'''
    
    highscore = app.highscore

    sortedScores = dict(sorted(highscore.items(), key=lambda x:x[1], reverse=True))
    maxNumOfScores = []
    finalHighScores = {}

    for key, value in sortedScores.items():
        if len(maxNumOfScores) < 5:
            maxNumOfScores.append(key)
            finalHighScores[key] = value

    session['highscores'] = finalHighScores
    return jsonify(session['highscores'])

@app.route('/reset-game')
def reset_game():
    '''Stores score, resets flask session variables and creates new game board.'''

    get_num = session['game_num']
    app.highscore[f'{get_num}'] = session['points']

    game_board = boggle_game.make_board()
    session['board'] = game_board
    session['result'] = ''
    session['points'] = 0
    session['game_num'] += 1
    return redirect('/')


