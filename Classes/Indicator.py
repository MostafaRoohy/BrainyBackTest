import pandas as pd
import numpy  as np
import talib
import random
from colour import Color



############################################################################################################
# A Buffer is a sequence that the Brain will take actions on it.
# Actions like Drawing line, Drawing Arrows, Opening Closing Modifying Trades and etc...
############################################################################################################
class Buffer:




    _BuffersFingerprints = []




    def __init__(self, numBuffer:int, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), typeWindow=('SamePanel','SeperatePanel','SeperateChart')):
        

        while (True):

            newFingerPrint = random.randint(1000000, 10000000-1)

            if(newFingerPrint not in Buffer._BuffersFingerprints):
                
                Buffer._BuffersFingerprints.append(newFingerPrint)
                break
            #
        #
        self.fingerprintBuffer = Buffer._BuffersFingerprints[-1]

        self.numBuffer         = numBuffer
        self.sizeBuffer        = 0
        self.titleBuffer       = titleBuffer
        self.jobBuffer         = jobBuffer
        self.widthBuffer       = widthBuffer
        self.colorBuffer       = colorBuffer
        self.typeWindow        = typeWindow

        self.valuesBuffer = [None for _ in range(0)]
    #




    def ResizeBuffer(self, newSize):

        self.sizeBuffer  = newSize

        if len(self.valuesBuffer) < newSize:

            self.valuesBuffer.extend([None] * (newSize - len(self.valuesBuffer)))
        #
    #
#




class Indicator:




    _IndicatorsFingerprints = []




    def __init__(self, nameIndicator:str):


        while (True):

            newFingerPrint = random.randint(1000000, 10000000-1)

            if(newFingerPrint not in Indicator._IndicatorsFingerprints):
                
                Indicator._IndicatorsFingerprints.append(newFingerPrint)
                break
            #
        #
        self.fingerprintIndicator    = Indicator._IndicatorsFingerprints[-1]
        self.name                    = nameIndicator

        self.buffersDict = dict()

        self.applyingData = None
        self.times        = None
        self.opens        = None
        self.highs        = None
        self.lows         = None
        self.closes       = None
        self.spreads      = None
        self.volumes      = None

        self.functionOnStart = None
        self.functionOnTick  = None
    #




    def SetNewBuffer(self, numBuffer:int, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), typeWindow=('SamePanel','SeperatePanel','SeperateChart')):
        
        newBuffer = Buffer(numBuffer, titleBuffer, jobBuffer, widthBuffer, colorBuffer, typeWindow)
        self.buffersDict[numBuffer] = newBuffer
    #




    def FeedInitialData(self, initialData:pd.DataFrame):

        self.applyingData = initialData
        self.times        = initialData['time'].to_numpy()
        self.opens        = initialData['open'].to_numpy()
        self.highs        = initialData['high'].to_numpy()
        self.lows         = initialData['low'].to_numpy()
        self.closes       = initialData['close'].to_numpy()
        self.spreads      = initialData['spread'].to_numpy()
        self.volumes      = initialData['volume'].to_numpy()
        
        for key, buffer in self.buffersDict:

            buffer.ResizeBuffer(len(initialData))
        #
    #




    def SefValueBufferAtIndex(self, numBuffer:int, indexBuffer:int, valueBuffer:float):
        
        (self.buffersDict[numBuffer]).valuesBuffer[indexBuffer] = valueBuffer
    #




    def SefValueBufferAtTime(self, numBuffer:int, indexBuffer:int, valueBuffer:float):
        
        pass
    #




    def GetValueBufferAtIndex(self, numBuffer:int, indexBuffer:int):

        return ((self.buffersDict[numBuffer]).valuesBuffer[indexBuffer])
    #




    def GetValueBufferAtTime(self, numBuffer:int, indexBuffer:int):

        pass
    #




    def SetFunctionOnStart(self, functionOnStart):

        self.functionOnStart = functionOnStart
    #




    def SetFunctionOnTick(self, functionOnTick):

        self.functionPnTick = functionOnTick
    #




    def OnStart(self):

        self.functionOnStart(self, self.times, self.opens, self.highs, self.lows, self.closes, self.spreads, self.volumes)
    #




    def OnTick(self):

        self.functionPnTick
    #
#