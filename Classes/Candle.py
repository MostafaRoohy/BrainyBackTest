import pandas as pd
import numpy  as np
import random




############################################################################################################
# Three classes for BackTest modes.

# 1) CandleStick class for CandleStick based BackTesting: Fast, but very in complicated situations can become inaccurate. use when very accurate spreads calculations doesn't matter too much.
# 3) Tick class for Tick based BackTesting: Very slow and has extremely heavy calculation, but the most accurate.
# 2) CandleTick class for CandleTick based BackTesting: Slow and has heavy calculation, but accurate. use when accurate spreads calculations matters.

# Tick data contains detailed information about every individual trade that occurs
############################################################################################################




class CandleStick:

    def __init__(self, candleIndex, candleTimestampA, candleTimestampB, candleOpen, candleHigh, candleLow, candleClose, candleVolume, candleSpread, marketPoints):

        self.index = candleIndex


        self.timestampA = candleTimestampA
        self.timestampB = candleTimestampB


        self.open   = candleOpen
        self.high   = candleHigh
        self.low    = candleLow
        self.close  = candleClose
        self.volume = candleVolume


        self.averagespread   = (candleSpread)
        self.averageslippage = (candleSpread*marketPoints)
    #
#




class Tick:

    def __init__(self, tickTimestamp:int, tickPrice:float, tickVolume:float, bidPrice:float, askPrice:float, bidVolume:float, askVolume:float, tickWaitMS:int):

        self.timestamp = tickTimestamp


        self.price     = tickPrice
        self.volume    = tickVolume

        self.askPrice  = askPrice
        self.bidPrice  = bidPrice

        self.askVolume = askVolume
        self.bidVolume = bidVolume


        self.waitMS  = tickWaitMS
    #
#




class CandleTick:

    def __init__(self, candleTimestampA, candleTimestampB, candleIndex, candleOpen, candleHigh, candleLow, candleClose, candleVolume, candleTicks: np.array):

        self.index = candleIndex


        self.timestampA = candleTimestampA
        self.timestampA = candleTimestampB

        self.open   = candleOpen
        self.high   = candleHigh
        self.low    = candleLow
        self.close  = candleClose
        self.volume = candleVolume



        self.ticks = candleTicks
    #
#