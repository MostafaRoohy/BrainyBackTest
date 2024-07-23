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
    #




    def AddIndicator(self, newIndicator:ind.Indicator):

        self.indicators.append(newIndicator)
        self.indicators[-1].FeedInitialData(self.knowledge)
    #




    def Think(self):

        for indicator in self.indicators:

            indicator.OnStart()
        #
    #




    def Imagine(self):

        chart = JupyterChart(inner_width=0.5, inner_height=0.5, width=1300, height=500, toolbox=True)
        chart.set(self.knowledge)


        for indicator in self.indicators:

            for bufferNum, buffer in indicator.buffersDict:

                if (buffer.jobBuffer=='DrawLine'):

                    self.knowledge[buffer.titleBuffer] = pd.Series(buffer.valuesBuffer)

                    chart.create_line(name='Buffer_'+str(buffersCount), color='rgba(255, 0, 0, 0.6)', price_label=False, price_line=False).set(processed)
                #
            #
        #
    #




    def Speak(self):

        pass
    #
#
