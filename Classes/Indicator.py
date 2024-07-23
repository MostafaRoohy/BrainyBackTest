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


    def __init__(self, numBuffer:int, sizeBuffer:int, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), typeWindow=('SamePanel','SeperatePanel','SeperateChart')):
        

        while (True):

            newFingerPrint = random.randint(1000000, 1000000-1)

            if(newFingerPrint not in Buffer._BuffersFingerprints):
                
                Buffer._BuffersFingerprints.append(newFingerPrint)
                break
            #
        #
        self.fingerprintBuffer = Buffer._BuffersFingerprints[-1]

        self.numBuffer         = numBuffer
        self.sizeBuffer        = sizeBuffer
        self.titleBuffer       = titleBuffer
        self.jobBuffer         = jobBuffer
        self.widthBuffer       = widthBuffer
        self.colorBuffer       = colorBuffer
        self.typeWindow        = typeWindow
        
        self.valuesBuffer = np.full(sizeBuffer, np.nan)
    #
#




class Indicator:


    _IndicatorsFingerprints = []


    def __init__(self, applyingData:pd.DataFrame, countBuffers:int, typeWindow=('SamePanel','SeperatePanel','SeperateChart')):


        while (True):

            newFingerPrint = random.randint(1000000, 1000000-1)

            if(newFingerPrint not in Indicator._IndicatorsFingerprints):
                
                Indicator._IndicatorsFingerprints.append(newFingerPrint)
                break
            #
        #
        self.fingerprintIndicator    = Indicator._IndicatorsFingerprints[-1]

        self.times   = self.applyingData['time'].to_numpy()
        self.opens   = self.applyingData['open'].to_numpy()
        self.highs   = self.applyingData['high'].to_numpy()
        self.lows    = self.applyingData['low'].to_numpy()
        self.closes  = self.applyingData['close'].to_numpy()
        self.spreads = self.applyingData['spread'].to_numpy()
        self.volumes = self.applyingData['volume'].to_numpy()
        self.times.flags.writeable   = False
        self.opens.flags.writeable   = False
        self.highs.flags.writeable   = False
        self.lows.flags.writeable    = False
        self.closes.flags.writeable  = False
        self.spreads.flags.writeable = False
        self.volumes.flags.writeable = False

        self.buffersList = []
    #




    def SetNewBuffer(self, numBuffer:int, titleBuffer:str, jobBuffer=('MiddleCalculations','DrawLine','DrawArrowUps','DrawArrowDns','DrawHistogram','DrawZigZag','DrawFilling','DrawCandles','DrawBars','Signal'), widthBuffer=1, colorBuffer=Color('white'), typeWindow=('SamePanel','SeperatePanel','SeperateChart')):
        
        newBuffer = Buffer(numBuffer, len(self.applyingData), titleBuffer, jobBuffer, widthBuffer, colorBuffer, typeWindow)
        self.buffersList.append(newBuffer)
    #



   
    def Indicated(self):

        theDF = pd.DataFrame()

        theDF['time']   = self.times
        theDF['open']   = self.opens
        theDF['high']   = self.highs
        theDF['low']    = self.lows
        theDF['close']  = self.closes
        theDF['spread'] = self.spreads
        theDF['volume'] = self.volumes

        for bufferNum in range(len(self.buffersList)):

            theDF['Buffer_'+str(bufferNum)] = pd.Series(self.buffersList[bufferNum])
        #


        return (theDF)
    # 




    def PrintData(self):

        print(self.data)
    #

 


    def MainIterator(self):

        for bufferNum in range(len(self.buffersList)):

            self.buffersList[bufferNum] = talib.SMA(self.closes, timeperiod=10*(bufferNum+1))
        #
    #
   
   


    def Indicate(self):

        self.MainIterator()
    #  
#