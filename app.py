from boggle import Boggle
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mydogmilo03'

app.debug = True
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_board():
    board = boggle_game.make_board()

    return render_template('game.html', board=board)
