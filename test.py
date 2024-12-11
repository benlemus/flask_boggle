from unittest import TestCase
from app import app, get_points
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def test_show_board(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="boardContainer">', html)

    def test_get_points(self):
        self.assertEqual(get_points('b', 'ok'), 1)
    
    def test_handle_form(self):
        with app.test_client() as client:
            self.boggle_game = Boggle()

            with client.session_transaction() as sess:
                sess['board'] = self.boggle_game.make_board()
                sess['points'] = 0  
                sess['result'] = ''
        
            res = client.post('/handle-form', json={'guess': 'TEST'})

            self.assertEqual(res.status_code, 200)

            data = res.get_json()
            
            self.assertIn('result', data)
            self.assertIn('points', data)

            with client.session_transaction() as sess:
                self.assertEqual(sess['result'], self.boggle_game.check_valid_word(sess['board'], 'TEST'))
                self.assertEqual(sess['points'], get_points('TEST', sess['result']))
        
    def test_update_highscores(self):
        self.mock_highscores = {
                    '1': 100,
                    '2': 200,
                    '3': 150,
                    '4': 250,
                    '5': 300,
                    '6': 50
                }
        with app.test_client() as client:
            with app.app_context():
                app.highscore.update(self.mock_highscores)

            res = client.get('/update-highscores')

            self.assertEqual(res.status_code, 200)

            data = res.get_json()
            self.assertEqual(len(data), 5)

            scores = sorted(list(data.values()), reverse=True)

            self.assertEqual(scores, sorted(scores, reverse=True))

            with client.session_transaction() as sess:
                self.assertEqual(sess['highscores'], data)
    
    def test_reset_game(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['game_num'] = 1
                sess['points'] = 10
        
            res = client.get('/reset-game', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            
            self.assertIn('<div class="boardContainer">', html)

            with client.session_transaction() as sess:
                self.assertEqual(sess['game_num'], 2) 
                self.assertEqual(sess['points'], 0)  
                self.assertTrue('board' in sess)      
                self.assertEqual(sess['result'], '')  

