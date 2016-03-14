from django.test import Client
import unittest

class SimpleTest(unittest.TestCase):
	def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/temps/')
        self.assertEqual(response.status_code, 200)

    def test_view_batches(self):
        response = self.client.get('/temps/view_user_batches/1')
        self.assertEqual(response.status_code, 200)

    def test_view_batch(self):
    	response = self.client.get('/temps/view_batch/1')
    	self.assertEqual(response.status_code, 200)
    	self.assertEqual(len(response.context['customers']), 5)

    def test_edit_batch(self):
    	response = self.client.get('/temps/edit_batch/1')
    	self.assertEqual(response.status_code, 200)

    def test_serve_compare_chart(self):
    	response = self.client.get('/temps/serve_compare_chart/1/2')
    	self.assertEqual(response.status_code, 200)
