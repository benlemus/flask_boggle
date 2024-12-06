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

highscore = {}

@app.route('/')
def show_board(): 
    if 'board' not in session:
        game_board = boggle_game.make_board()
        session['board'] = game_board
        session['result'] = ''
        session['points'] = 0
        session['highscores'] = {}
        session['game_num'] = 1
    
    return render_template('game.html', board=session['board'])

def get_points(guess, result):
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
    
    session['highscores'] = dict(sorted(highscore.items(), key=lambda x:x[1], reverse=True))
    
    return jsonify(session['highscores'])


@app.route('/reset-game')
def reset_game():
    get_num = session['game_num']
    highscore[f'{get_num}'] = session['points']

    game_board = boggle_game.make_board()
    session['board'] = game_board
    session['result'] = ''
    session['points'] = 0
    session['game_num'] += 1
    return redirect('/')


