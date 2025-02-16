import backtrader as bt
from datetime import datetime
import ta
#import pyfolio as pf
from strategies import HighestHighStrategy
import matplotlib

def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    #Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    #Print the rows
    print_list = [h1,r1,h2,r2]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('',*row))

        

# Create a cerebro entity
cerebro = bt.Cerebro(cheat_on_open=True)

<<<<<<< HEAD
store = bt.stores.IBStore(host="127.0.0.1", port=7496, clientId= 5)

cerebro.broker.set_coc(True)
cerebro.broker.setcash(300000.0)
cerebro.broker.setcommission(commission=0.0012)
# Add a strategy
cerebro.addstrategy(HighestHighStrategy)

stockkwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        compression =10,
        rtbar=False,  # use RealTime 5 seconds bars
        historical=True,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        fromdate=datetime(2019, 2, 2),  # get data from..
        todate=datetime(2020, 10, 29),  # get data from..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target
        tz="Asia/Kolkata"
    )

data0 = store.getdata(dataname="TCS-STK-NSE-INR", **stockkwargs)

for da in data0:
    print(da)
=======
# RUN WITH IBKR 
# store = bt.stores.IBStore(host="127.0.0.1", port=7496, clientId= 4)

# # Add a strategy
# cerebro.addstrategy(SmallStrategy)

# stockkwargs = dict(
#         timeframe=bt.TimeFrame.Minutes,
#         compression =5,
#         rtbar=False,  # use RealTime 5 seconds bars
#         historical=True,  # only historical download
#         qcheck=0.5,  # timeout in seconds (float) to check for events
#         fromdate=datetime(2020, 8, 1),  # get data from..
#         todate=datetime(2020, 9, 20),  # get data from..
#         latethrough=False,  # let late samples through
#         tradename=None,  # use a different asset as order target
#         tz="Asia/Kolkata"
#     )

# data0 = store.getdata(dataname="RELIANCE-FUT-NSE-INR", **stockkwargs)
# cerebro.replaydata(data0, timeframe=bt.TimeFrame.Days, compression=1)

# cerebro.run()

# -----------------------------

# # Add a strategy
cerebro.addstrategy(NR3Strategy)

# Create a Data Feed
data = bt.feeds.YahooFinanceData(
    dataname='TCS.NS',
    fromdate = datetime(2017,1,1),
    todate = datetime(2020,9,1),
    buffered= True
    )
>>>>>>> 4b7d6f94a05b48c610ff7715934ba37aac1255b9
    
cerebro.adddata(data0)

<<<<<<< HEAD
cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#cerebro.plot()
=======
# Add the Data Feed to Cerebro
cerebro.adddata(data)

cerebro.broker.setcash(300000.0)
# # Set the commission - 0.1% ... divide by 100 to remove the %
#cerebro.broker.setcommission(commission=200, margin=100000, mult=75)

# # Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")

# Run over everything
strategies = cerebro.run()
firstStrat = strategies[0]

# # print the analyzers
printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())

# # Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
>>>>>>> 4b7d6f94a05b48c610ff7715934ba37aac1255b9
