import unittest
from ProductionCode.command_line import *
from app import app

class test_app(unittest.TestCase):
    def setUp(self):
            """This runs BEFORE every single test function."""
            self.app = app.test_client()
            self.app.testing = True

    def test_valid_load(self):
        """Test that data is loaded correctly from the 2003.csv file."""
        data = load_csv("2003.csv")

        self.assertGreater(len(data), 0)
        self.assertEqual(data[0][0], "Common Name (Scientific Name)")

    def test_route(self):
        self.app = app.test_client() 
        response = self.app.get('/', follow_redirects=True) 
        self.assertEqual(b'Welcome to the Carleton Bird Tracker Website!', response.data) 

    def test_sightings_route_valid(self):
        response = self.app.get('/sightings/American Crow (Corvus brachyrhynchos) /1/2003')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"American Crow (Corvus brachyrhynchos)  was sighted 1 times at stop 1 in 2003.", response.data)

    def test_popular_stop_route(self):
        """Test the popular stop route."""
        response = self.app.get('/popular/2000')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The most popular stop", response.data)

    def test_invalid_sighting_name(self):
        response = self.app.get('/sightings/American Crow/1/2003')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The url is wrong", response.data)

    def test_invalid_sighting_stop(self):
        response = self.app.get('/sightings/American Crow (Corvus brachyrhynchos) /222/2000')
        self.assertIn(b"The url is wrong", response.data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_sighting_year(self):
        response = self.app.get('/sightings/American Crow (Corvus brachyrhynchos) /1/22222')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The url is wrong', response.data)
    
    def test_invalid_year(self):
        response = self.app.get('/popular/22222')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The url is wrong", response.data)

if __name__ == '__main__':
    unittest.main()