import numpy as np
import pandas as pd
import random
import Candle as cd
import Indicator as ind



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




    def Think(self):

        pass
    #

    def Speak(self):

        pass
    #

    def Imagine(self):

        pass
    #

    def ThinkSpeak(self):

        pass
    #

    def ThinkImagine(self):

        pass
    #

    def ThinkSpeakImagine(self):

        pass
    #




    def NewData(self, newData:cd.CandleStick):

        pass
    #

    def NewData(self, newData:cd.Tick):

        pass
    #

    def NewData(self, newData:cd.CandleTick):

        pass
    #
#
