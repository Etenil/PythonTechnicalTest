from unittest import TestCase

from bonds.gleif import get_entity_name, LeiRequestError, InvalidLeiError


class GleifTestCase(TestCase):
    """
    Tests for the very basic gleif API query module
    """
    def test_goes_fetch_a_valid_lei_name(self):
        name = get_entity_name('R0MUWSFPU8MPRO8K5P83')
        self.assertEqual(name, 'BNP PARIBAS')

    def test_wont_request_with_invalid_param(self):
        self.assertRaises(InvalidLeiError, lambda: get_entity_name(None))
        self.assertRaises(InvalidLeiError, lambda: get_entity_name(''))

    def test_raises_on_query_errors(self):
        self.assertRaises(LeiRequestError, lambda: get_entity_name('foobar'))
