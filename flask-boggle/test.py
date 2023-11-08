from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle


class FlaskTests(TestCase):
    def test_make_board(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Welcome to the Boggle Game!</h1>',html)

    def test_check_guess(self):
        with app.test_client() as client:
            res = client.post('/check-guess', data=json.dumps({'guess': 'valid'}), content_type='application/json')
            data = json.loads(res.data.decode('utf-8'))

            self.assertIs(data['result'], 'ok')

    def test_end_game(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['games_played'] = 9
                change_session['highest_score'] = 9

                self.assertEqual(session['games_played'], 10)
                self.assertEqual(session['highest_score'], 10)