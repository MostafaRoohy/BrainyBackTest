import pandas as pd
import numpy  as np
import random



############################################################################################################
# An Indicator is a data processor that indicates and shows the core logic of market conditions.
# It can be applies to two datas:    1) Market data    2) Another indicatored data.
# Parameters:
# dataMarket: Raw Data to be processed on.
# dataIndicator: Indicatored Data to be processed on.
# countBuffers: Data containers for the drawing datas.
# typeDraw: Line, Arrow, to be developed more types...
# typeWindow: The indicator chart to be int seperate window or in the market chart.
############################################################################################################



class Buffer:


    def __init__(self, sizeBuff:int, numBuff:int, titleBuff:str):
        
        self.sizeBuff  = sizeBuff
        self.numBuff   = numBuff
        self.titleBuff = titleBuff

        self.valuesBuff = np.full(sizeBuff, np.nan)
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




    def SetBufferType(self, numberBuffer, nameBuffer, digitsBuffer, typeDrawBuffer=('MiddleCalculations','None','Line','Arrow','Histogram1','Histogram2','Section','ZigZag','Filling','Bars','Candles')):
                  
        pass
    #




    def SetBufferMeanlessValue(self, whichBuffer:int, newName:str):

        self.data.rename(columns={'Buffer_'+str(whichBuffer) : newName}, inplace=True)
    #




    def MainIterator(self):

        for bufferNum in range(len(self.buffersList)):

            self.buffersList[bufferNum] = talib.SMA(self.closes, timeperiod=10*(bufferNum+1))
        #
    #
   
   


    def Indicate(self):

        self.MainIterator()
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
#