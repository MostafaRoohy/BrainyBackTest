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

            for buffer in indicator.buffersDict.values():

                if (buffer.jobBuffer=='DrawLine'):

                    title = str(indicator.name+"_"+buffer.titleBuffer)
                    self.knowledge[title] = pd.Series(buffer.valuesBuffer)
                    self.chart.create_line(name=(title), color=buffer.colorBuffer, price_label=False, price_line=False).set(self.knowledge)
                #
                elif (buffer.jobBuffer=='DrawArrowUps'):

                    pass
                #
                elif (buffer.jobBuffer=='DrawArrowDns'):

                    pass
                #
                elif (buffer.jobBuffer=='Signal'):

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
