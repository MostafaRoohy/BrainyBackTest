import pandas as pd
import numpy  as np
import talib
import random
from colour import Color
from BrainyBackTest.fingerprint import Fingerprint




class Buffer:


    def __init__(self, numBuffer:int, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), windowBuffer=('SamePanel','SeperatePanel','SeperateChart')):
        

        self.fingerprint = Fingerprint().new_fingerprint()

        self.num         = numBuffer
        self.size        = 0
        self.title       = titleBuffer
        self.job         = jobBuffer
        self.width       = widthBuffer
        self.color       = colorBuffer
        self.typeWindow  = windowBuffer

        self.values = np.full(0, np.nan)
        self.times  = np.full(0, np.nan)
    #


    def resize_buffer(self, newSize):


        if len(self.size) < newSize:

            np.append(self.values, np.full(newSize-self.size, np.nan))
            np.append(self.times,  np.full(newSize-self.size, np.nan))

            self.size  = newSize
        #
    #
#




class Indicator:


    def __init__(self, nameIndicator:str, applyingData=None):


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

        self.functionOnStart = None
        self.functionOnTick  = None


        self.feed_initial_data(self.applyingData)
    #


    def set_new_buffer(self, numBuffer:int, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), windowBuffer=('SameChart','SeperatePanel','SeperateChart')):
        
        newBuffer = Buffer(numBuffer, titleBuffer, jobBuffer, widthBuffer, colorBuffer, windowBuffer)
        self.buffers[numBuffer] = newBuffer
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
                self.buffers.times = initialData['time'].to_numpy()
            #
        #
    #


    def set_value_buffer_at_index(self, numBuffer:int, indexBuffer:int, valueBuffer:float):
        
        (self.buffers[numBuffer]).values[indexBuffer] = valueBuffer
    #


    def set_value_buffer_at_time(self, numBuffer:int, indexBuffer:int, valueBuffer:float):
        
        pass
    #


    def __setitem__(self, key, value):

        pass
    #


    def get_value_buffer_at_index(self, numBuffer:int, indexBuffer:int):

        return ((self.buffers[numBuffer]).values[indexBuffer])
    #


    def get_value_buffer_at_time(self, numBuffer:int, indexBuffer:int):

        pass
    #


    def __getitem__(self, key):

        pass
    #


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