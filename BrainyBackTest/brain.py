import numpy as np
import pandas as pd
from lightweight_charts import JupyterChart
import random
from BrainyBackTest.candle import *
from BrainyBackTest.indicator import *
from BrainyBackTest.trade import *




class Brain:


    def __init__(self, valueCapital:int, chartData:pd.DataFrame):

        self.valueCapital = valueCapital
        
        self.knowledge    = chartData
        self.indicators   = list()
        self.chart        = None

        self.orders       = list()
        self.trades       = list()
    #


    def add_indicator(self, newIndicator:Indicator):

        self.indicators.append(newIndicator)
        self.indicators[-1].feed_initial_data(self.knowledge)
    #


    def think(self):

        for indicator in self.indicators:

            indicator.OnStart()
        #


        for i in range(len(self.knowledge)):

            timeA  =  self.knowledge['time'].iloc[i]
            open   =  self.knowledge['open'].iloc[i]
            high   =  self.knowledge['high'].iloc[i]
            low    =  self.knowledge['low'].iloc[i]
            close  =  self.knowledge['close'].iloc[i]
            volume =  0 #self.knowledge['volume'].iloc[i]
            spread =  0 #self.knowledge['spread'].iloc[i]

            candle = CandleStick(i, timeA, timeA, open, high, low, close, volume, spread, 0.1)


            for indicator in self.indicators:

                for buffer in indicator.buffers:

                    if (buffer.job=='Signal'):
                            
                        if (buffer.values[i] is not None):

                            signal = buffer.values[i]

                            newOrder = Order(indexPlaced=i, timestampPlaced=buffer.times[i], type=signal.action, direction=signal.direction, valueVolume=signal.valueVolume, priceSL=signal.priceSL, priceTP=signal.priceTP)

                            self.orders.append(newOrder)
                        #
                    #
                #
            #

            for order in self.orders:

                if (order.isAlive):

                    tmp = order.Refresh(candle)

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


    def speak(self):

        allPnL = 0

        for trade in self.trades:

            print(f'Trade--> index={trade.indexOpened}\t timeOpened={trade.timestampOpened}\t Direction={trade.direction}\t V={trade.valueVolume}\t Opened={trade.priceOpened}\t SL={trade.priceSL}\t TP={trade.priceTP}\t PnL={trade.valuePnL}')
            allPnL += trade.valuePnL
        #

        print("All PnL = ", allPnL)
    #


    def imagine(self):

        self.chart = JupyterChart(inner_width=0.5, inner_height=0.5, width=1300, height=500, toolbox=True)
        self.chart.set(self.knowledge)

        for indicator in self.indicators:

            for buffer in indicator.buffers:

                if (buffer.job=='DrawLine'):

                    title = str(indicator.name+"_"+buffer.title)
                    self.knowledge[title] = buffer.values
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
#