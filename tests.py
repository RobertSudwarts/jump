import unittest
from decimal import Decimal
from problem3_v2 import Asset, Portfolio


class TestPortfolio(unittest.TestCase):

    def setUp(self):

        a = {'Symbol': 'x', 'Description': 'X', 'Country': 'US',
             'Shares': '10', 'Price': '6', 'Currency': 'USD',
             'Total Value': '60'}

        b = {'Symbol': 'y', 'Description': 'Y', 'Country': 'GB',
             'Shares': '250', 'Price': '12.5', 'Currency': 'GBp',
             'Total Value': '3125'}

        self.portfolio = Portfolio()
        self.portfolio.assets = [Asset(**a), Asset(**b)]

    def test_n_portfolio(self):
        self.assertEqual(len(self.portfolio.assets), 2)

    def test_cash_div(self):
        '''portfolio cash

        All this really demonstrates is that the code would be neater
        if, instead of returning a cash amount to be added to the
        portfolio, the 'Asset' changed its *parent's* cash value...
        '''
        asset = self.portfolio.asset_by_code('y')

        cash = asset.cash_div(2)
        self.assertEqual(cash, 500)


class TestAsset(unittest.TestCase):

    def setUp(self):

        a = {
            'Symbol': 'x',
            'Description': 'X',
            'Country': 'US',
            'Shares': '10',
            'Price': '6',
            'Currency': 'USD',
            'Total Value': '60'
        }

        self.asset = Asset(**a)

    def test_ssplit(self):

        self.asset.ssplit('3:1')

        # qty changes
        self.assertEqual(self.asset.qty, 30)
        # price changes
        self.assertEqual(self.asset.px, 2)
        # total value unchanged
        self.assertEqual(self.asset.total_val, 60)

    def test_cash_div(self):

        self.asset.cash_div(0.02)

        # qty remains unchanged
        self.assertEqual(self.asset.qty, 10)
        # price changes
        self.assertEqual(self.asset.px, 5.98)
        # total value changes
        # self.assertEqual(self.asset.total_val, 59.8)
        self.assertEqual(self.asset.total_val, Decimal('59.8'))

    def test_stock_div(self):

        self.asset.stock_div(0.50)

        # qty remains unchanged
        self.assertEqual(self.asset.qty, 15)
        # price changes
        self.assertEqual(self.asset.px, 4)
        # total value unchanged
        self.assertEqual(self.asset.total_val, 60)


if __name__ == '__main__':
    unittest.main()
