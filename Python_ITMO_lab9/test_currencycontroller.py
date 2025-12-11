import unittest
from unittest.mock import MagicMock, patch
from controllers.currencycontroller import CurrencyController

class TestCurrencyController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = CurrencyController(self.mock_db)

    def test_list_currencies(self):
        self.mock_db.read_currencies.return_value = [{"id":1, "char_code":"USD", "value":90}]
        result = self.controller.list_currencies()
        self.assertEqual(result[0]['char_code'], "USD")
        self.mock_db.read_currencies.assert_called_once()

    def test_update_currency(self):
        self.mock_db.read_currencies.return_value = [{"id":1, "char_code":"USD"}]
        self.mock_db.update_currency.return_value = True
        result = self.controller.update_currency("USD", 95.0)
        self.assertTrue(result)
        self.mock_db.update_currency.assert_called_once()

if __name__ == '__main__':
    unittest.main()
