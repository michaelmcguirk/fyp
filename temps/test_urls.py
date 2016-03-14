# Michael McGuirk - D13123389 - DT228/4 - FYP
# Test class to test the mapping of URLs to Views.
from django.test import Client
import unittest
from django.core.urlresolvers import resolve, reverse

class SimpleTest(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_new_batch(self):
        url = reverse('new_batch')
        self.assertEqual(url, '/temps/new_batch/')
        resolver = resolve('/temps/new_batch/')
        self.assertEqual(resolver.view_name, 'new_batch')

    def test_edit_batch(self):
        url = reverse('edit_batch', args=[1])
        self.assertEqual(url, '/temps/edit_batch/1/')
        resolver = resolve('/temps/edit_batch/1/')
        self.assertEqual(resolver.view_name, 'edit_batch')

    def test_view_batch(self):
        url = reverse('view_batch', args=[1])
        self.assertEqual(url, '/temps/view_batch/1/')
        resolver = resolve('/temps/view_batch/1/')
        self.assertEqual(resolver.view_name, 'view_batch')

    def test_compare(self):
        url = reverse('compare', args=[1])
        self.assertEqual(url, '/temps/compare/1/')
        resolver = resolve('/temps/compare/1/')
        self.assertEqual(resolver.view_name, 'compare')

    def test_start_batch(self):
        url = reverse('start_batch')
        self.assertEqual(url, '/temps/start_batch/')
        resolver = resolve('/temps/start_batch/')
        self.assertEqual(resolver.view_name, 'start_batch')

    def test_stop_batch(self):
        url = reverse('stop_batch')
        self.assertEqual(url, '/temps/stop_batch/')
        resolver = resolve('/temps/stop_batch/')
        self.assertEqual(resolver.view_name, 'stop_batch')

    def test_serve_compare_chart(self):
        url = reverse('serve_compare_chart', args=[1,1])
        self.assertEqual(url, '/temps/serve_compare_chart/1/1/')
        resolver = resolve('/temps/serve_compare_chart/1/1/')
        self.assertEqual(resolver.view_name, 'serve_compare_chart')

    def test_view_user_batches(self):
        url = reverse('view_user_batches', args=[1])
        self.assertEqual(url, '/temps/view_user_batches/1/')
        resolver = resolve('/temps/view_user_batches/1/')
        self.assertEqual(resolver.view_name, 'view_user_batches')

    def test_register(self):
        url = reverse('register')
        self.assertEqual(url, '/temps/register/')
        resolver = resolve('/temps/register/')
        self.assertEqual(resolver.view_name, 'register')

    def test_login(self):
        url = reverse('login')
        self.assertEqual(url, '/temps/login/')
        resolver = resolve('/temps/login/')
        self.assertEqual(resolver.view_name, 'login')
