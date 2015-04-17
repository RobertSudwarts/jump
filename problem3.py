
# we'll use python's csv package to contruct the starting portfolio from a file

import csv
from decimal import *
getcontext().prec = 8


class Portfolio(object):

    assets = []
    # cash by ccy really should be driven by the
    # (set of) assets in the portfolio but I'll ignore
    # that and make it static for clarity.
    cash = {'USD': Decimal('0'), 'CAD': Decimal('0'), 'GBp': Decimal('0')}

    def display(self, day):
        print "\n### " + day + "\n"
        for asset in self.assets:
            print asset
        print
        print "portfolio_value", self.portfolio_value()
        print "cash", self.cash

    def asset_by_code(self, code):
        for a in self.assets:
            if a.code == code:
                return a

    def portfolio_value(self):
        '''
        Compute the Total Value of the positions per currency
        '''
        v = {}
        for asset in self.assets:
            if asset.ccy in v:
                v[asset.ccy] += asset.total_val
            else:
                v[asset.ccy] = asset.total_val

        return v

    def base_ccy_portfolio_value(self, fx):
        '''
        given an fx rate, you could value assets accordingly etc.
        '''
        pass


class Asset(object):
    def __init__(self, **kw):
        self.code = kw['Symbol']
        self.description = kw['Description']
        self.country = kw['Country']
        self.qty = int(kw['Shares'])
        self.px = float(kw['Price'])
        self.ccy = kw['Currency']
        self.total_val = Decimal(kw['Total Value'])

    def ssplit(self, ratio):
        '''Adjust quantity, price

        The change in liquidity will have a secondary
        impact on the price and hence total value
        but I'll conveniently ignore that(!) and
        assume that total value remains unchanged

        ratio would be for example
            '3:1' => (3 for 1),
            '1:3' => (1 for 3)
        '''
        n, d = ratio.split(':')
        r = float(n) / int(d)
        self.qty *= r
        self.px /= r

    def cash_div(self, div):
        '''
        * adjust the price by dividend as a % of current price
        * adjust total value accordingly
        * return cash dividend amount
        '''
        self.px = self.px * (1 - (div / self.px))
        self.total_val = Decimal(str(self.qty * self.px))

        # return amnt to be added to portfolio cash
        return self.qty * div

    def stock_div(self, div):
        '''
        fractional shares (even though these can't be bought
        in the market) may result from stock divs.

        As with stock splits the change in liquidity has,
        in practice, a consequent impact on the price
        -- I'll assume total value remains unchanged
        '''
        self.qty = self.qty + (self.qty * div)
        self.px *= 1 / (1 + div)

    def name_change(self, name):
        self.description = name

    def code_change(self, code):
        self.code = code

    def __repr__(self):
        return "<Asset(code='%s', descr='%s', ctry='%s', qty=%d, px=%0.4f, ccy='%s', val=%s)>" \
            % (self.code, self.description, self.country, self.qty, self.px, self.ccy, self.total_val)

def main():
    portfolio = Portfolio()

    with open('portfolio.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Symbol']:
                # make an `Asset` and add it to the portfolio
                asset = Asset(**row)
                portfolio.assets.append(asset)

    # T0
    portfolio.display('T0')

    # Monday
    # BAC  Cash dividend - $0.02/share
    asset = portfolio.asset_by_code('BAC')
    delta_cash = asset.cash_div(0.02)
    portfolio.cash[asset.ccy] += Decimal(delta_cash)

    # REX  Stock split - 9 for 10
    asset = portfolio.asset_by_code('REX')
    asset.ssplit('9:10')

    # RIM  Symbol change - new symbol is BB
    asset = portfolio.asset_by_code('RIM')
    asset.code_change('BB')

    # RIM/BB Name change - new name is "Blackberry"
    asset.name_change('Blackberry')

    portfolio.display('Monday')

    # Tuesday

    # INTC Cash dividend - $0.21/share
    asset = portfolio.asset_by_code('INTC')
    delta_cash = asset.cash_div(0.21)
    portfolio.cash[asset.ccy] += Decimal(delta_cash)

    # POT  Cash dividend - 0.07 CAD/share
    asset = portfolio.asset_by_code('POT')
    delta_cash = asset.cash_div(0.07)
    portfolio.cash[asset.ccy] += Decimal(delta_cash)

    # BARC Cash dividend - 3 GBp/share
    asset = portfolio.asset_by_code('BARC')
    delta_cash = asset.cash_div(0.03)
    portfolio.cash[asset.ccy] += Decimal(delta_cash)

    portfolio.display('Tuesday')

    # Wednesday
    # GOOG  Stock split - 3 for 1
    asset = portfolio.asset_by_code('GOOG')
    asset.ssplit('3:1')

    # SIRI  Stock split - 1 for 3
    asset = portfolio.asset_by_code('SIRI')
    asset.ssplit('1:3')

    portfolio.display('Wednesday')

    # Thursday
    #  T  Stock dividend - 1.075/share
    asset = portfolio.asset_by_code('T')
    asset.stock_div(1.075)

    portfolio.display('Thursday')

    # Friday

    # QQQ  Cash dividend - $0.4125/share
    asset = portfolio.asset_by_code('QQQ')
    delta_cash = asset.cash_div(0.4125)
    portfolio.cash[asset.ccy] += Decimal(delta_cash)

    portfolio.display('Friday')

if __name__ == '__main__':
    main()
