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

    def __init__(self, candleTimestampOpened, candleTimestampClosed, candleIndex, candleOpen, candleHigh, candleLow, candleClose, candleVolume, candleSpread, marketPoints):

        self.index = candleIndex


        self.timestampOpened = candleTimestampOpened
        self.timestampClosed = candleTimestampClosed


        self.open   = candleOpen
        self.high   = candleHigh
        self.low    = candleLow
        self.close  = candleClose
        self.volume = candleVolume


        self.spread   = (candleSpread)
        self.slippage = (self.spread*marketPoints)
    #
#




class Tick:

    def __init__(self, tickTimestamp, tickIndex, tickPrice, tickVolume, bidPrice, askPrice, bidVolume, askVolume, marketPoints):

        self.index = tickIndex


        self.timestamp = tickTimestamp


        self.tradedprice = tickPrice
        self.volume      = tickVolume

        self.askPrice  = askPrice
        self.bidPrice  = bidPrice
        self.askVolume = askVolume
        self.bidVolume = bidVolume
    #
#




class CandleTick:

    def __init__(self, candleTimestampOpened, candleTimestampClosed, candleIndex, candleOpen, candleHigh, candleLow, candleClose, candleTicks: np.array, candleSpread, marketPoints):

        self.candleIndex = candleIndex


        self.timestampOpened = candleTimestampOpened
        self.timestampClosed = candleTimestampClosed


        self.open  = candleOpen
        self.high  = candleHigh
        self.low   = candleLow
        self.close = candleClose


        self.ticks = candleTicks


        self.spread   = (candleSpread)
        self.slippage = (self.spread*marketPoints)
    #
#