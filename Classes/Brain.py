import numpy as np
import pandas as pd
from lightweight_charts import JupyterChart
import random

from Classes.Candle import *
from Classes.Indicator import *
from Classes.Trade import *


class Brain:




    def __init__(self, chartData:pd.DataFrame, valueCapital:int):

        self.valueCapital = valueCapital
        
        self.knowledge  = chartData
        self.indicators = []

        self.orders    = []
        self.trades    = []

        self.chart = JupyterChart(inner_width=0.5, inner_height=0.5, width=1300, height=500, toolbox=True)
        self.chart.set(chartData)
    #




    def AddIndicator(self, newIndicator:Indicator):

        self.indicators.append(newIndicator)
        self.indicators[-1].FeedInitialData(self.knowledge)
    #




    def Think(self):

        for indicator in self.indicators:

            indicator.OnStart()
        #


        for indicator in self.indicators:

            for buffer in indicator.buffers.values():

                if (buffer.job=='Signal'):

                    for i, signal in enumerate(buffer.values):
                        
                        if (signal is not None):

                            newOrder = Order(indexPlaced=i, timestampPlaced=buffer.times[i], type=signal.action, direction=signal.direction, valueVolume=signal.valueVolume, priceSL=signal.priceSL, priceTP=signal.priceTP)

                            self.orders.append(newOrder)
                        #
                    #
                #
            #
        #


        for i in range(len(self.knowledge)):

            timeA  =  self.knowledge['time'].iloc[i]
            open   =  self.knowledge['open'].iloc[i]
            high   =  self.knowledge['high'].iloc[i]
            low    =  self.knowledge['low'].iloc[i]
            close  =  self.knowledge['close'].iloc[i]
            volume =  self.knowledge['volume'].iloc[i]
            spread =  self.knowledge['spread'].iloc[i]

            candle = CandleStick(i, timeA, 0, open, high, low, close, volume, spread, 0.1)

            for order in self.orders:

                if (order.isAlive):

                    tmp = order.Refresh(candle)
                    # print(tmp)
                    if (tmp is not None):

                        self.trades.append(tmp)
                    #
                #
            #

            for trade in self.trades:

                if (trade.isAlive):

                    trade.Refresh(candle)
                #
            #
    #




    def Imagine(self):

        for indicator in self.indicators:

            for buffer in indicator.buffers.values():

                if (buffer.job=='DrawLine'):

                    title = str(indicator.name+"_"+buffer.title)
                    self.knowledge[title] = pd.Series(buffer.values)
                    self.chart.create_line(name=title, color=buffer.color, price_label=False, price_line=False).set(self.knowledge)
                #


                if (buffer.job=='DrawArrowUps'):

                    for i, arrow in enumerate(buffer.values):

                        if (arrow is not None):

                            self.chart.marker(time=buffer.times[i], position='below', shape='arrow_up', color=str(buffer.color))
                        #
                    #
                #


                if (buffer.job=='DrawArrowDns'):

                    for i, arrow in enumerate(buffer.values):

                        if (arrow is not None):

                            self.chart.marker(time=buffer.times[i], position='above', shape='arrow_down', color=str(buffer.color))
                        #
                    #
                #
            #
        #


        self.chart.load()
    #




    def Speak(self):

        for trade in self.trades:

            print(trade.valuePnL)
        #
    #
#
