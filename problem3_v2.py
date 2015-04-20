
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
        for asset in self.assets:
            if asset.code == code:
                return asset

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

        The change in liquidity will have a secondary impact on the
        price and hence total value but I'll conveniently ignore that(!)
        and assume that total value remains unchanged

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

        As with stock splits, the change in liquidity has, in practice,
        a consequent impact on the price -- which I'll ignore(!)
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


def get_corporate_actions():
    '''
    iterate through the corportate actions file to create a dict of:
       day -> code -> [actions]

    the nested dict (although a little more complicated) means that the
    asset only needs to be 'queried' once per day.
    '''
    corporate_actions = {}
    with open('corporate_actions.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)  # ignore header row
        for rw in reader:
            day = rw[0]
            code = rw[1]
            if day not in corporate_actions:
                corporate_actions[day] = {}
                corporate_actions[day][code] = [rw[2:]]
            else:
                if code not in corporate_actions[day]:
                    corporate_actions[day][code] = [rw[2:]]
                else:
                    corporate_actions[day][code].append(rw[2:])

    return corporate_actions


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

    corporate_actions = get_corporate_actions()

    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:

        print '\ncorporate actions: (%s)' % day

        for code in corporate_actions[day]:

            asset = portfolio.asset_by_code(code)

            for _type, div, ccy in corporate_actions[day][code]:
                print "\t", code, _type, div, ccy

                if _type == 'Cash dividend':
                    delta_cash = asset.cash_div(float(div))
                    portfolio.cash[asset.ccy] += Decimal(delta_cash)

                elif _type == 'Stock dividend':
                    asset.stock_div(float(div))

                elif _type == 'Stock split':
                    asset.ssplit(div)

                elif _type == 'Name change':
                    asset.name_change(div)

                elif _type == 'Symbol change':
                    asset.code_change(div)

                else:
                    raise AttributeError("unhandled corporate action type")

        portfolio.display(day)

if __name__ == '__main__':
    main()
