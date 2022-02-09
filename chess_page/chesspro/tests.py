from django.test import SimpleTestCase

class SimpleTest(SimpleTestCase):
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_json_response(self):
        response = self.client.get('/jsonresp/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {})

    def test_list_moves(self):
        response = self.client.get('/api/v1/pawn/a2/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'availableMoves': ['a3', 'a4'], 'error': None, 'figure': 'pawn', 'currentField': 'a2'})

    def test_dest_moves_pawn(self):
        response = self.client.get('/api/v1/pawn/a2/a3/')
        self.assertEqual(response.status_code, 200)

    def test_dest_moves_knight(self):
        response = self.client.get('/api/v1/knight/b1/c3/')
        self.assertEqual(response.status_code, 200)

    def test_bad_link1(self):
        response = self.client.get('/api/v1/pawn/x2/')
        self.assertEqual(response.status_code, 409)

    def test_bad_link2(self):
        response = self.client.get('/api/v1/pawnn/a2/')
        self.assertEqual(response.status_code, 404)

    def test_bad_link3(self):                    #Złe pole
        response = self.client.get('/api/v1/pawn/a5/')
        self.assertEqual(response.status_code, 500)













