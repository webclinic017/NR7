import backtrader as bt

class MFIStrategy(bt.Strategy):
    
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        self.f.write('%s, %s\n' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].adjclose
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

        self.f = open("log.csv","w")
        if len(self.datas) == 1:
            # 1 data feed passed, must have components
            tprice = (self.data.close + self.data.low + self.data.high) / 3.0
            mfraw = tprice * self.data.volume
        else:
            # if more than 1 data feed, individual components in OHLCV order
            tprice = (self.data0 + self.data1 + self.data2) / 3.0
            mfraw = tprice * self.data3

        # No changes with regards to previous implementation
        flowpos = bt.ind.SumN(mfraw * (tprice > tprice(-1)), period=5)
        flowneg = bt.ind.SumN(mfraw * (tprice < tprice(-1)), period=5)

        mfiratio = bt.ind.DivByZero(flowpos, flowneg, zero=100.0)
        self.mfi = 100.0 - 100.0 / (1.0 + mfiratio)
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = 0
        self.sellprice = 0
        self.long = True
        self.buycomm = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.sellprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
        

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order or len(self) < 61:
            return

        # Check if we are in the market
        if not self.position:
            
            if (self.mfi[0] > 30 and self.mfi[-1] < 30):

                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                #self.order = self.buy(exectype=Order.StopLimit, price=self.datahigh[0], valid=self.datas[0].datetime.date(0) + datetime.timedelta(days=3))
                self.order = self.buy(size=1)
                self.long = True 
                
            if (self.mfi[0] < 70 and self.mfi[-1] > 70):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=1)
                self.long = False

        else:
            
            if((self.long == True and (self.dataclose[0] > (self.buyprice + 200) or self.mfi[0] > 70 or self.dataclose[0] < (self.buyprice - 90)))):
                self.log('SELL EXIT, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=1)
            
            if((self.long == False and (self.dataclose[0] < (self.buyprice - 200) or self.mfi[0] < 30 or self.dataclose[0] > (self.buyprice + 90)))):
                self.log('BUY EXIT, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy(size=1)



class NR3Strategy(bt.Strategy):
    
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        self.f.write('%s, %s\n' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].adjclose
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

        self.f = open("log.csv","w")

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = 0
        self.sellprice = 0
        self.long = True
        self.buycomm = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.sellprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
        

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order :
            return

        # Check if we are in the market
        if not self.position:
            condition1 = (self.datahigh[-1]-self.datalow[-1]) < (((self.datahigh[-2]-self.datalow[-2]) + (self.datahigh[-3]-self.datalow[-3]))/3)
            close20 = self.dataclose[0] > self.dataclose[-10]
            condition2 = self.rsi[0] > 50
            if (condition2 and condition1 and self.datahigh[0] > self.datahigh[-1] and close20):

                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                #self.order = self.buy(exectype=Order.StopLimit, price=self.datahigh[0], valid=self.datas[0].datetime.date(0) + datetime.timedelta(days=3))
                self.order = self.buy(size=1)
                self.long = True 
        else:
            
            if((self.datalow[0]<self.buyprice) or len(self) > 4):
                self.log('SELL EXIT, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.close(size=1)
            
            
class SmaStrategy(bt.Strategy):
    
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        self.f.write('%s, %s\n' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

        self.f = open("log.csv","w")

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = 0
        self.sellprice = 0
        self.long = True
        self.buycomm = None
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.sellprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
        

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order :
            return

        # Check if we are in the market
        if not self.position:
            condition1 = (self.datahigh[-1]-self.datalow[-1]) < (((self.datahigh[-2]-self.datalow[-2]) + (self.datahigh[-3]-self.datalow[-3]))/3)
            close20 = self.dataclose[0] > self.dataclose[-10]
            condition2 = self.rsi[0] > 50
            if (condition2 and condition1 and self.datahigh[0] > self.datahigh[-1] and close20):

                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                #self.order = self.buy(exectype=Order.StopLimit, price=self.datahigh[0], valid=self.datas[0].datetime.date(0) + datetime.timedelta(days=3))
                self.order = self.buy(size=1)
                self.long = True 
        else:
            
            if((self.datalow[0]<self.buyprice) or len(self) > 4):
                self.log('SELL EXIT, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.close(size=1)


<<<<<<< HEAD
    
class HighestHighStrategy(bt.Strategy):
=======
class SmallStrategy(bt.Strategy):
>>>>>>> 4b7d6f94a05b48c610ff7715934ba37aac1255b9
    
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        self.f.write('%s, %s\n' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
<<<<<<< HEAD
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

        self.f = open("log.csv","w")
        self.f.write('Datetime,Open,High,Low,Close,Action,,,\n')
=======
        self.dataclose = self.datas[0].adjclose
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.ma = bt.indicators.MovingAverageSimple(self.datas[0], period=20)

        self.f = open("log.csv","w")

>>>>>>> 4b7d6f94a05b48c610ff7715934ba37aac1255b9
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = 0
        self.sellprice = 0
        self.long = True
        self.buycomm = None
<<<<<<< HEAD
        self.sl = 0
        self.target = 0
        self.shares = None
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('%.2f, %.2f, %.2f, %.2f, BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (self.dataopen[0], 
                         self.datahigh[0], 
                         self.datalow[0], 
                         self.dataclose[0],
                         order.executed.price,
                         order.executed.value,
                         order.executed.comm))
               
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('%.2f, %.2f, %.2f, %.2f, SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % 
                        (self.dataopen[0], 
                         self.datahigh[0], 
                         self.datalow[0], 
                         self.dataclose[0],
                         order.executed.price,
                         order.executed.value,
                         order.executed.comm))
            
=======
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
>>>>>>> 4b7d6f94a05b48c610ff7715934ba37aac1255b9
                self.sellprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
        

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

<<<<<<< HEAD
        self.log(',,,,OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next_open(self):
        if not self.position:
            buy = True
            for x in range(1, 10):
                if(self.datahigh[0]<self.datahigh[-x]):
                    buy = False

            if (buy  and self.dataopen[0]> self.datalow[-1]):
                self.sl = self.datalow[-1]
                self.target = self.dataopen[0] + ((self.dataopen[0] - self.datalow[-1])*3)
            
                self.log('%.2f, %.2f, %.2f, %.2f, BUY CREATE, SL %.2f, Target %.2f' % 
                        (self.dataopen[0], 
                         self.datahigh[0], 
                         self.datalow[0], 
                         self.dataclose[0],
                         self.sl,
                         self.target))
                self.shares = round((self.broker.getcash()*0.02)/(self.dataopen[0] - self.datalow[-1]))
                self.buyprice = self.dataopen[0]
                self.order = self.buy(size=self.shares,coc=False)
                self.long = True 
                self.sl = self.datalow[-1]
                self.target = self.dataopen[0] + ((self.dataopen[0] - self.datalow[-1])*2.5)
            
    def next(self):
        self.log('%.2f, %.2f, %.2f, %.2f' % 
                (self.dataopen[0],
                 self.datahigh[0],
                 self.datalow[0], 
                 self.dataclose[0]))
=======
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

>>>>>>> 4b7d6f94a05b48c610ff7715934ba37aac1255b9
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order :
            return

<<<<<<< HEAD
        if self.position:
            if((self.datalow[0]<self.sl) or self.datahigh[0]>self.target):
                self.log('%.2f, %.2f, %.2f, %.2f, SELL EXIT' % 
                        (self.dataopen[0], 
                        self.datahigh[0],
                        self.datalow[0],
                        self.dataclose[0]))
                self.order = self.close(size=self.shares)


    
    
    
=======
        # Check if we are in the market
        if not self.position:
            condition1 = (self.dataclose[-1] < self.ma[-1])
            condition2 = (self.dataclose[0] > self.ma[0])
            if (condition2 and condition1):

                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                #self.order = self.buy(exectype=Order.StopLimit, price=self.datahigh[0], valid=self.datas[0].datetime.date(0) + datetime.timedelta(days=3))
                self.order = self.buy(size=1)
                self.long = True 
        else:
            
            if((self.datalow[0]<self.buyprice) or len(self) > 4):
                self.log('SELL EXIT, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.close(size=1)
>>>>>>> 4b7d6f94a05b48c610ff7715934ba37aac1255b9
