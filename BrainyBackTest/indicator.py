import pandas as pd
import numpy  as np
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
        #
        else:

            self.values = np.full(shape=0, fill_value=nullValue, dtype=np.float64)
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


    def __init__(self, nameIndicator:str="", numIndicator:int=0, functionOnStart=None, functionOnTick=None, chartData:pd.DataFrame=None):

        self.fingerprint     = Fingerprint().new_fingerprint()

        self.name            = nameIndicator
        self.num             = numIndicator
        self.functionOnStart = functionOnStart
        self.functionOnTick  = functionOnTick
        self.knowledge       = chartData

        self.times           = None
        self.opens           = None
        self.highs           = None
        self.lows            = None
        self.closes          = None
        self.spreads         = None
        self.volumes         = None
        self.buffers         = list()


        self.feed_initial_data(self.knowledge)


        if (self.knowledge is not None):

            self.think()
        #
    #


    def feed_initial_data(self, initialData:pd.DataFrame=None):

        if (initialData is not None):

            self.knowledge    = initialData

            self.times        = initialData['time'].to_numpy(dtype=np.float64)
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


    def set_new_buffer(self, numBuffer:int=0, nullValue:float=0, titleBuffer:str="", jobBuffer:str=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer:int=1, colorBuffer:Color=Color('white'), windowBuffer:str=('SameChart','SeperatePanel','SeperateChart')):
        
        newBuffer = Buffer(numBuffer, nullValue, titleBuffer, jobBuffer, widthBuffer, colorBuffer, windowBuffer)
        self.buffers.append(newBuffer)


        for buffer in self.buffers:

            buffer.resize_buffer(len(self.knowledge))
        #
    #


    def get_knowledge(self):

        if (self.knowledge is None):

            print("The indicator is empty")
        #
        elif (isinstance(self.knowledge, pd.DataFrame)):

            return (self.knowledge)
        #
        else:

            return (pd.DataFrame(self.knowledge))
        #
    #

    #########################################################################################################
    #########################################################################################################
    #########################################################################################################

    def think(self):

        self.OnStart()

        for buffer in self.buffers:

            if (buffer.job!='Signal'):

                title = str(self.name+"_"+buffer.title)
                self.knowledge[title] = pd.Series(buffer.values)
            #
            elif (buffer.job=='Signal'):

                signalFingerprint = np.full(shape=len(self.knowledge), fill_value=0, dtype=np.int64)
                signalAction      = np.full(shape=len(self.knowledge), fill_value="", dtype=str)
                signalDir         = np.full(shape=len(self.knowledge), fill_value="", dtype=str)
                signalTrigger     = np.full(shape=len(self.knowledge), fill_value=0, dtype=np.float64)
                signalOpen        = np.full(shape=len(self.knowledge), fill_value=0, dtype=np.float64)
                signalTP          = np.full(shape=len(self.knowledge), fill_value=0, dtype=np.float64)
                signalSL          = np.full(shape=len(self.knowledge), fill_value=0, dtype=np.float64)
                signalVol         = np.full(shape=len(self.knowledge), fill_value=0, dtype=np.float64)

                for i in range(len(self.knowledge)):

                    if (buffer.values[i]!=buffer.nullValue):

                        signalFingerprint[i] = buffer.values[i].fingerprint
                        signalAction[i]      = buffer.values[i].action
                        signalDir[i]         = buffer.values[i].direction
                        signalTrigger[i]     = buffer.values[i].priceTrigger
                        signalOpen[i]        = buffer.values[i].priceOpen
                        signalTP[i]          = buffer.values[i].priceTP
                        signalSL[i]          = buffer.values[i].priceSL
                        signalVol[i]         = buffer.values[i].valueVolume
                    #
                #

                self.knowledge["Fingerprint"] = pd.Series(signalFingerprint)
                self.knowledge["Action"]      = pd.Series(signalAction)
                self.knowledge["Dir"]         = pd.Series(signalDir)
                self.knowledge["Trigger"]     = pd.Series(signalTrigger)
                self.knowledge["Open"]        = pd.Series(signalOpen)
                self.knowledge["TP"]          = pd.Series(signalTP)
                self.knowledge["SL"]          = pd.Series(signalSL)
                self.knowledge["Vol"]         = pd.Series(signalVol)
            #
        #
    #


    def imagine(self):

        pass
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


        if (isinstance(at, tuple)):

            i, j = at
            (self.buffers[i]).values[j] = val
        #
        elif (isinstance(at, int)):

            i = at
            (self.buffers[i].values[:]) = val
        #
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

        if (isinstance(at, tuple)):

            i, j = at
            return ((self.buffers[i]).values[j])
        #
        elif (isinstance(at, int)):

            i = at
            return (self.buffers[i].values[:])
        #
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