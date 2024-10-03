import pandas as pd
import numpy  as np
import talib
import random
from colour import Color
from BrainyBackTest.fingerprint import Fingerprint




class Buffer:


    def __init__(self, numBuffer:int, nullValue:float, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), windowBuffer=('SamePanel','SeperatePanel','SeperateChart')):
        

        self.fingerprint = Fingerprint().new_fingerprint()

        self.num         = numBuffer
        self.nullValue   = nullValue
        self.size        = 0
        self.title       = titleBuffer
        self.job         = jobBuffer
        self.width       = widthBuffer
        self.color       = colorBuffer
        self.typeWindow  = windowBuffer


        if (jobBuffer=='Signal'):

            self.values = np.full(shape=0, fill_value=nullValue, dtype=object)
            # self.times  = np.full(shape=0, fill_value=nullValue, dtype=object)
        #
        else:

            self.values = np.full(shape=0, fill_value=nullValue, dtype=np.float64)
            # self.times  = np.full(shape=0, fill_value=nullValue, dtype=np.float64)
        #
    #


    def resize_buffer(self, newSize):


        if (self.size < newSize):

            self.values = np.append(self.values, np.full(shape=newSize-self.size, fill_value=self.nullValue))
            self.size  = newSize
        #
    #

    #########################################################################################################
    #########################################################################################################
    #########################################################################################################

    def __setitem__(self, at, val):

        self.values[at] = val
    #


    def __getitem__(self, at):

        return (self.values[at])
    #
#




class Indicator:


    def __init__(self, nameIndicator:str, functionOnStart=None, functionOnTick=None, applyingData=None):


        self.fingerprint     = Fingerprint().new_fingerprint()
        self.name            = nameIndicator
        self.applyingData    = applyingData
        self.buffers         = list()


        self.times           = None
        self.opens           = None
        self.highs           = None
        self.lows            = None
        self.closes          = None
        self.spreads         = None
        self.volumes         = None

        self.functionOnStart = functionOnStart
        self.functionOnTick  = functionOnTick


        self.feed_initial_data(self.applyingData)
    #


    def set_new_buffer(self, numBuffer:int, nullValue:float, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), windowBuffer=('SameChart','SeperatePanel','SeperateChart')):
        
        newBuffer = Buffer(numBuffer, nullValue, titleBuffer, jobBuffer, widthBuffer, colorBuffer, windowBuffer)
        self.buffers.append(newBuffer)
    #


    def feed_initial_data(self, initialData:pd.DataFrame):


        if (initialData is not None):

            self.applyingData = initialData

            self.times        = initialData['time'].to_numpy()
            self.opens        = initialData['open'].to_numpy()
            self.highs        = initialData['high'].to_numpy()
            self.lows         = initialData['low'].to_numpy()
            self.closes       = initialData['close'].to_numpy()
            self.spreads      = initialData['spread'].to_numpy()
            self.volumes      = initialData['volume'].to_numpy()
            

            for buffer in self.buffers:

                buffer.resize_buffer(len(initialData))
            #
        #

    #

    #########################################################################################################
    #########################################################################################################
    #########################################################################################################

    def set_value_buffer_at_index(self, numBuffer:int, indexBuffer:int, valueBuffer:float):
        
        (self.buffers[numBuffer]).values[indexBuffer] = valueBuffer
    #


    def set_value_buffer_at_time(self, numBuffer:int, indexBuffer:int, valueBuffer:float):
        
        pass
    #


    def __setitem__(self, at, val):

        i, j = at

        (self.buffers[i]).values[j] = val
    #

    #########################################################################################################
    #########################################################################################################
    #########################################################################################################

    def get_value_buffer_at_index(self, numBuffer:int, indexBuffer:int):

        return ((self.buffers[numBuffer]).values[indexBuffer])
    #


    def get_value_buffer_at_time(self, numBuffer:int, indexBuffer:int):

        pass
    #


    def __getitem__(self, at):

        i, j = at

        return ((self.buffers[i]).values[j])
    #

    #########################################################################################################
    #########################################################################################################
    #########################################################################################################


    def set_function_OnStart(self, functionOnStart):

        self.functionOnStart = functionOnStart
    #


    def set_function_OnTick(self, functionOnTick):

        self.functionOnTick = functionOnTick
    #


    def OnStart(self):

        self.functionOnStart(self, self.times, self.opens, self.highs, self.lows, self.closes, self.spreads, self.volumes)
    #


    def OnTick(self):

        self.functionOnTick
    #
#




