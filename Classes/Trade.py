import pandas as pd
import numpy  as np
import random
from Classes.Candle import *




############################################################################################################
# A SignalRequest is like a clue that is inside an Indicator's buffer, so the Brain can act upon these clues.
############################################################################################################
class SignalRequest:


    _SignalRequestFigerprints = []


    def __init__(self, action=('NewOrderLimit','NewOrderTriggerLimit','NewOrderMarket','NewOrderTriggerMarket','CloseAll','Close','ModifyTrigger','ModifyTP','ModifySL'), direction=('BuyLong','SellShort'), priceTrigger=0.0, priceOpen=0.0, priceTP=0.0, priceSL=0.0, valueVolume=0.0, byFingerprint=0):
        
        self.action        = action
        self.direction     = direction

        self.priceTrigger  = priceTrigger
        self.priceOpen     = priceOpen
        self.priceTP       = priceTP
        self.priceSL       = priceSL
        self.valueVolume   = valueVolume

        self.byFingerprint = byFingerprint



        while (True):

            newFingerPrint = random.randint(1000000, 1000000-1)

            if(newFingerPrint not in SignalRequest._SignalRequestFigerprints):
                
                SignalRequest._SignalRequestFigerprints.append(newFingerPrint)
                
                break
            #
        #
    #
#




############################################################################################################
# An Order is a command that the Brain generates and sends to the platform.
############################################################################################################
class Order:




    _Fingerprints = []




    def __init__(self, indexPlaced, timestampPlaced, type=('Limit','TriggerLimit','Market','TriggerMarket'), direction=('BuyLong','SellShort'), valueVolume=0, priceTrigger=0, priceOpen=0, priceSL=0, priceTP=0):


        while (True):

            newFingerPrint = random.randint(1000000, 10000000-1)

            if(newFingerPrint not in Order._Fingerprints):
                
                Order._Fingerprints.append(newFingerPrint)
                break
            #
        #
        self.fingerprint        = Order._Fingerprints[-1]


        self.indexPlaced       = indexPlaced
        self.timestampPlaced   = timestampPlaced


        self.type              = type
        self.direction         = direction

        self.valueVolume       = valueVolume
        self.priceTrigger      = priceTrigger
        self.priceOpen         = priceOpen
        self.priceSL           = priceSL
        self.priceTP           = priceTP


        self.istrigered       = (True) if (type=='Limit' or type=='Market') else (False)
        self.isOrderAlive     = False
        self.isOrderDead      = False
        self.isOrderCancelled = False
        self.isOrderOpened    = False
        self.indexOpened      = None
        self.timestampOpened  = None
        self.priceOpened      = None
    #
    



    def NowOpen(self, indexOpening, timestampOpening, priceOpening):

        self.indexOpened     = indexOpening
        self.timestampOpened = timestampOpening
        self.isOpened        = True
        self.isOrderAlive    = False
        self.isOrderDead     = True
        self.openedPrice     = priceOpening



        newTrade = Trade(self.fingerprint, self.indexOpened, self.timestampOpened, self.valueVolume, self.openedPrice, self.priceSL, self.priceTP, self.direction)

        return (newTrade)
    #
    
    


    def Refresh(self, aCandlestick: CandleStick):

        if (self.direction=='BuyLong'):


            if (self.type=='TrigerLimit'):

                if (self.trigered==True):

                    if (aCandlestick.high + aCandlestick.slippage >= self.priceOpen):

                        self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, self.priceOpen)
                        return
                    #
                #
                elif (self.trigered==False):

                    if (aCandlestick.high >= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aCandlestick)
                        return
                    #
                #
            #
            elif (self.type=='TrigerMarket'):

                if (self.trigered==True):

                    self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, (aCandlestick.low + aCandlestick.slippage))
                    return
                #
                elif (self.trigered==False):

                    if (aCandlestick.high >= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aCandlestick)
                        return
                    #
                #
            #
            elif (self.type=='Market'):

                
                return (self.NowOpen(aCandlestick.index, aCandlestick.timestampA, (aCandlestick.low + aCandlestick.slippage)))
            #
            elif (self.type=='Limit'):
                    
                if (aCandlestick.high + aCandlestick.averageslippage >= self.priceOpen):

                    return (self.NowOpen(aCandlestick.index, aCandlestick.timestampA, self.priceOpen))
                #
            #
        #
        elif (self.direction=='SellShort'):


            if (self.type=='TrigerLimit'):

                if (self.trigered==True):

                    if (aCandlestick.low <= self.priceOpen):

                        self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, self.priceOpen)
                        return
                    #
                #
                elif (self.trigered==False):

                    if (aCandlestick.low <= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aCandlestick)
                        return
                    #
                #
            #
            elif (self.type=='TrigerMarket'):

                if (self.trigered==True):

                    self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, (aCandlestick.low))
                    return
                #
                elif (self.trigered==False):

                    if (aCandlestick.low <= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aCandlestick)
                        return
                    #
                #
            #
            elif (self.type=='Market'):

                return (self.NowOpen(aCandlestick.index, aCandlestick.timestampA, (aCandlestick.low)))
            #
            elif (self.type=='Limit'):
                    
                if (aCandlestick.low <= self.priceOpen):

                    return (self.NowOpen(aCandlestick.index, aCandlestick.timestampA, self.priceOpen))
                #
            #
        #



        return (None)
    #




    def Refresh(self, aTick: Tick):

        if (self.direction=='BuyLong'):


            if (self.enumType=='TrigerLimit'):

                if (self.trigered==True):

                    if (aTick.askPrice>= self.priceOpen):

                        self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                        return
                    #
                #
                elif (self.trigered==False):

                    if (aTick.tradedprice >= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aTick)
                        return
                    #
                #
            #
            elif (self.enumType=='TrigerMarket'):

                if (self.trigered==True):

                    self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                    return
                #
                elif (self.trigered==False):

                    if (aTick.tradedprice >= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aTick)
                        return
                    #
                #
            #
            elif (self.enumType=='Market'):

                self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                return
            #
            elif (self.enumType=='Limit'):

                if (aTick.askPrice >= self.priceOpen):

                    self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                    return
                #
            #
        #
        elif (self.direction=='SellShort'):


            if (self.enumType=='TrigerLimit'):

                if (self.trigered==True):

                    if (aTick.bidPrice <= self.priceOpen):

                        self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                        return
                    #
                #
                elif (self.trigered==False):

                    if (aTick.tradedprice <= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aTick)
                        return
                    #
                #
            #
            elif (self.enumType=='TrigerMarket'):

                if (self.trigered==True):

                    self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                    return
                #
                elif (self.trigered==False):

                    if (aTick.tradedprice <= self.priceTrigger):

                        self.trigered = True
                        self.TryOpen(aTick)
                        return
                    #
                #
            #
            elif (self.enumType=='Market'):

                self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                return
            #
            elif (self.enumType=='Limit'):

                if (aTick.bidPrice <= self.priceOpen):

                    self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                    return
                #
            #
        #



        return (None)
    #




    def Refresh(self, aCandleTick: CandleTick):

        for aTick in aCandleTick.ticks:

            if (self.enumDirection=='BuyLong'):


                if (self.enumType=='TrigerLimit'):

                    if (self.trigered==True):

                        if (aTick.askPrice>= self.priceOpen):

                            self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                            return
                        #
                    #
                    elif (self.trigered==False):

                        if (aTick.tradedprice >= self.priceTrigger):

                            self.trigered = True
                            self.TryOpen(aTick)
                            return
                        #
                    #
                #
                elif (self.enumType=='TrigerMarket'):

                    if (self.trigered==True):

                        self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                        return
                    #
                    elif (self.trigered==False):

                        if (aTick.tradedprice >= self.priceTrigger):

                            self.trigered = True
                            self.TryOpen(aTick)
                            return
                        #
                    #
                #
                elif (self.enumType=='Market'):

                    self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                    return
                #
                elif (self.enumType=='Limit'):

                    if (aTick.askPrice >= self.priceOpen):

                        self.NowOpen(aTick.index, aTick.timestamp, aTick.askPrice)
                        return
                    #
                #
            #
            elif (self.enumDirection=='SellShort'):


                if (self.enumType=='TrigerLimit'):

                    if (self.trigered==True):

                        if (aTick.bidPrice <= self.priceOpen):

                            self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                            return
                        #
                    #
                    elif (self.trigered==False):

                        if (aTick.tradedprice <= self.priceTrigger):

                            self.trigered = True
                            self.TryOpen(aTick)
                            return
                        #
                    #
                #
                elif (self.enumType=='TrigerMarket'):

                    if (self.trigered==True):

                        self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                        return
                    #
                    elif (self.trigered==False):

                        if (aTick.tradedprice <= self.priceTrigger):

                            self.trigered = True
                            self.TryOpen(aTick)
                            return
                        #
                    #
                #
                elif (self.enumType=='Market'):

                    self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                    return
                #
                elif (self.enumType=='Limit'):

                    if (aTick.bidPrice <= self.priceOpen):

                        self.NowOpen(aTick.index, aTick.timestamp, aTick.bidPrice)
                        return
                    #
                #
            #
        #



        return (None)
    #




    def CancelOrder(self):

        self.indexOpened      = 0
        self.timestampOpened  = 0
        self.isOrderAlive     = False
        self.isOrderDead      = True
        self.isOrderCancelled = True
        self.openedPrice      = 0
    #
#




############################################################################################################
# A Trade is an Opened Order.
############################################################################################################
class Trade:
    



    _Fingerprints = []



    
    def __init__(self, indexOpened, timestampOpened, direction, valueVolume, priceOpened, priceSL, priceTP):


        while (True):

            newFingerPrint = random.randint(1000000, 10000000-1)

            if(newFingerPrint not in Trade._Fingerprints):
                
                Trade._Fingerprints.append(newFingerPrint)
                break
            #
        #
        self.fingerprint      = Trade._Fingerprints[-1]


        self.indexOpened      = indexOpened
        self.timestampOpened  = timestampOpened


        self.direction        = direction


        self.valueVolume      = valueVolume
        self.priceOpened      = priceOpened
        self.priceSL          = priceSL
        self.priceTP          = priceTP


        self.isTradeAlive     = False
        self.isTradeDead      = False
        self.ClosedPrice      = None


        self.valuePnL         = 0
    #




    def PrintTraded(self):

        print("Trade Ticket: ", self.ticketTrade, "\t", "PnL= ", self.valuePnL)
    #




    def EndTrade(self, EndingAtPrice):

        self.isTradeAlive = False
        self.isClosed     = True
        self.ClosedPrice  = EndingAtPrice

        self.CalculateTradePnL(self.ClosedPrice)
    #
    

    

    def CalculateTradePnL(self, calculatingAtPrice):

        result = 0.0

        if(self.direction=='BuyLong'):

            openedQuality    = (self.valueVolume*self.priceOpened)
            thisPriceQuality = (self.valueVolume*calculatingAtPrice)

            result = (thisPriceQuality-openedQuality)
        #
        elif (self.direction=='SellShort'):

            openedQuality    = (self.valueVolume*self.priceOpened)
            thisPriceQuality = (self.valueVolume*calculatingAtPrice)

            result = (openedQuality-thisPriceQuality)
        #




        self.valuePnL = result
        return (result)
    #



    
    def Refresh(self, aCandleStick: CandleStick):

        if (self.direction=='BuyLong'):

            if (aCandleStick.low <= self.priceSL and self.priceSL!=0):

                self.EndTrade(self.priceSL)
                return
            #
            elif (aCandleStick.high+aCandleStick.averageslippage >= self.priceTP and self.priceTP!=0):

                self.EndTrade(self.priceTP)
                return
            #

            self.CalculateTradePnL(aCandleStick.low)
        #
        elif (self.direction=='SellShort'):

            if (aCandleStick.high+aCandleStick.averageslippage >= self.priceSL and self.priceSL!=0):

                self.EndTrade(self.priceSL)
                return
            #
            elif (aCandleStick.low+aCandleStick.averageslippage <= self.priceTP and self.priceTP!=0):

                self.EndTrade(self.priceTP)
                return
            #

            self.CalculateTradePnL(aCandleStick.high+aCandleStick.averageslippage)
        #
    #




    def Refresh(self, aTick: Tick):

        if (self.enumDirection=='BuyLong'):

            if (aTick.bidPrice <= self.priceSL and self.priceSL!=0):

                self.KillTrade(aTick.bidPrice)
                return
            #
            elif (aTick.bidPrice >= self.priceTP and self.priceTP!=0):

                self.KillTrade(aTick.bidPrice)
                return
            #

            self.CalculateTradePnL(aTick.bidPrice)
        #
        elif (self.enumDirection=='SellShort'):

            if (aTick.askPrice >= self.priceSL and self.priceSL!=0):

                self.KillTrade(aTick.askPrice)
                return
            #
            elif (aTick.askPrice <= self.priceTP and self.priceTP!=0):

                self.KillTrade(aTick.askPrice)
                return
            #

            self.CalculateTradePnL(aTick.askPrice)
        # 
    #




    def Refresh(self, aCandleTick: CandleTick):

        for aTick in aCandleTick.ticks:

            if (self.enumDirection=='BuyLong'):

                if (aTick.bidPrice <= self.priceSL and self.priceSL!=0):

                    self.KillTrade(aTick.bidPrice)
                    return
                #
                elif (aTick.bidPrice >= self.priceTP and self.priceTP!=0):

                    self.KillTrade(aTick.bidPrice)
                    return
                #

                self.CalculateTradePnL(aTick.bidPrice)
            #
            elif (self.enumDirection=='SellShort'):

                if (aTick.askPrice >= self.priceSL and self.priceSL!=0):

                    self.KillTrade(aTick.askPrice)
                    return
                #
                elif (aTick.askPrice <= self.priceTP and self.priceTP!=0):

                    self.KillTrade(aTick.askPrice)
                    return
                #

                self.CalculateTradePnL(aTick.askPrice)
            # 
        #
    #
#




############################################################################################################
# In two-way accounts, every trade is considered as seperate position.
# In one-way accounts, we will have only one position that any new trade will increase and any closing trade will decrease the position's volume.
############################################################################################################
class Position:
        

    def __init__(self):

        self.containingTrades = []
        self.overallVolume    = 0

        self.ticketPosition   = None

        self.isPositionAlive  = False
        self.isPositionDead   = False

        self.valuePositionPnL = 0
    #



    def GeneratePositionTicket(self):

        return (random.randint(9999, 999999999999))
    #




    def IncreaseTrade(self, newTrade):

        self.containingTrades.append(newTrade)
        self.CanculateOverallVolume(self)

        self.isPositionAlive = True
        self.isPositionDead  = False
    #




    def DecreaseTrade(self, closingTrade):

        self.CalculatePositionPnL()
        self.CanculateOverallVolume()

        self.trades = [trade for trade in self.trades if (trade.ticketTrade != closingTrade.ticketTrade)]

        self.CanculateOverallVolume()


        if (self.overallVolume==0):

            self.KillPosition()
        #
    #




    def KillPosition(self):

        self.isPositionAlive = False
        self.isPositionDead  = True
    #




    def CalculatePositionPnL(self):

        for trade in self.containingTrades:

            self.valuePositionPnL += trade.CalculatePositionPnL()
        #
    #




    def CanculateOverallVolume(self):

        for trade in self.containingTrades:
            
            self.overallVolume += (trade.enumDirection=='BuyLong') if (trade.valueVolume) else (trade.valueVolume*-1) 
        #
    #




    def RefreshStatus(self, aCandleStick: CandleStick):
        
        for trade in self.containingTrades:

            trade.RefreshStatus(aCandleStick)
        #
    #




    def RefreshStatus(self, aTick: Tick):

        for trade in self.containingTrades:

            trade.RefreshStatus(aTick)
        #
    #




    def RefreshStatus(self, aCandleTick: CandleTick):

        for trade in self.containingTrades:

            trade.RefreshStatus(aCandleTick)
        #
    #
#
