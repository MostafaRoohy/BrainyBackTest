import numpy as np
import pandas as pd
from lightweight_charts import JupyterChart
import random
from Classes import Candle as cd
from Classes import Indicator as ind



class Brain:




    def __init__(self, chartData:pd.DataFrame, valueCapital:int, modeHedge=('TwoWay','OneWay')):

        self.valueCapital = valueCapital
        self.modeHedge    = modeHedge
        
        self.knowledge  = chartData
        self.indicators = []

        self.orders    = []
        self.trades    = []
        self.Positions = []

        self.chart = JupyterChart(inner_width=0.5, inner_height=0.5, width=1300, height=500, toolbox=True)
        self.chart.set(chartData)
    #




    def AddIndicator(self, newIndicator:ind.Indicator):

        self.indicators.append(newIndicator)
        self.indicators[-1].FeedInitialData(self.knowledge)
    #




    def Think(self):

        for indicator in self.indicators:

            indicator.OnStart()
        #


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

                            self.chart.marker(time=buffer.times[i], position='below', shape='arrow_up')
                        #
                    #
                #


                if (buffer.job=='DrawArrowDns'):

                    for i, arrow in enumerate(buffer.values):

                        if (arrow is not None):

                            self.chart.marker(time=buffer.times[i], position='above', shape='arrow_down')
                        #
                    #
                #


                if (buffer.job=='Signal'):

                    pass
                #
            #
        #
    #




    def Imagine(self):

        self.chart.load()
    #




    def Speak(self):

        pass
    #
#
