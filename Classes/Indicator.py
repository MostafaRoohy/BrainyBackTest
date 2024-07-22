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


    def __init__(self, applyingData:pd.DataFrame, countBuffers:int, typeWindow=('SamePanel','SeperatePanel','SeperateChart')):

        self.idHandler    = random.randint(10000, 100000-1)

        self.applyingData = applyingData
        self.countBuffers = countBuffers
        self.typeWindow   = typeWindow

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
        for n in range(countBuffers):

            self.buffersList.append(Buffer(len(applyingData), n, str(n)))
        #
    #




    def SetBufferType(self, numberBuffer, nameBuffer, digitsBuffer, typeDrawBuffer=('MiddleCalculations','Trade','None','Line','Arrow','ZigZag','Histogram1','Histogram2','Section','Filling','Bars','Candles')):
                  
        pass
    #




    def SetBufferMeanlessValue(self, whichBuffer:int, newName:str):

        self.data.rename(columns={'Buffer_'+str(whichBuffer) : newName}, inplace=True)
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