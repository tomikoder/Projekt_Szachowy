from django.test import SimpleTestCase

possible_errors = {1: 'Zła pozycja figury szachowej.',
                   2: 'Zły kolor figury szachowej.',
                   3: 'Złe argumenty do tworzenia szachownicy',
                   4: 'Złe dane wejściowe. Podałeś źle pozycje figury./n Podaj "pawn/A2" np.',
                   5: 'Podałeś złą literową pozycję. Dostępne są litery od a-h.',
                   6: 'Podałeś złą numeryczną pozycję. Dostępne są cyfry od 1-8.',
                   7: 'Podałeś złą nazwę figry. Użyj np "pawn".',
                   8: 'Dana figura nie znajduje się na danym polu.',
                   9: 'Liczba argumentów jest nie wystarczająca, lub jest za duża.'
                   }

class SimpleTest(SimpleTestCase):
    def test_list_moves_papwn(self):
        response = self.client.get('/api/v1/pawn/a2/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'availableMoves': ['a3', 'a4'], 'error': None, 'figure': 'pawn', 'currentField': 'a2'})

    def test_dest_moves_pawn(self):
        response = self.client.get('/api/v1/pawn/a2/a3/')
        self.assertEqual(response.status_code, 200)

    def test_dest_moves_knight(self):
        response = self.client.get('/api/v1/knight/b1/c3/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'move': "valid", 'error': None, 'figure': 'knight', 'currentField': 'b1', 'destField': 'c3'})
        self.assertJSONNotEqual(response.content, {'move': "valid", 'error': None, 'figure': 'knight', 'currentField': 'B1', 'destField': 'C3'})

    def test_bad_link1(self):
        response = self.client.get('/api/v1/pawn/x2/')
        self.assertJSONEqual(response.content, {'availableMoves': None, 'error': 'Podałeś złą literową pozycję. Dostępne są litery od a-h.', 'figure': None, 'currentField': None})
        self.assertEqual(response.status_code, 409)

    def test_bad_link2(self):
        response = self.client.get('/api/v1/pawn/a2/x2')
        self.assertJSONEqual(response.content, {'move': None, 'error': 'Destination Field Error\n' + possible_errors[7], 'figure': None,  'currentField': None, 'destField': None})
        self.assertEqual(response.status_code, 409)

    def test_bad_link2(self):
        response = self.client.get('/api/v1/pawnn/a2/')
        self.assertEqual(response.status_code, 404)

    def test_bad_link3(self):                    #Złe pole
        response = self.client.get('/api/v1/pawn/a5/')
        self.assertEqual(response.status_code, 500)













