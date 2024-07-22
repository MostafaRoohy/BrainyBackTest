import pandas as pd
import numpy  as np
import random
from Classes.Candle import *




############################################################################################################
# A SignalRequest is like a clue that the Indicator generates, so the Brain can act upon these clues.
############################################################################################################
class SignalRequest:

    _SignalRequestFigerprints = []


    def __init__(self, action=('NewOrder','CloseAll','Close','ModifyTrigger','ModifyTP','ModifySL'), byFingerprint=0):
        
        self.action        = action
        self.byFingerprint = byFingerprint

        if (action=='NewOrder'):

            while (True):

                newFingerPrint = random.randint(1000000, 1000000-1)

                if(newFingerPrint not in SignalRequest._SignalRequestFigerprints):
                    
                    SignalRequest._SignalRequestFigerprints.append(newFingerPrint)
                    break
                #
            #
        #
    #
#




############################################################################################################
# An Order is a command that TheSignalerModule sends to the platform.
############################################################################################################
class Order:


    def __init__(self, indexSignaled, valueVolume, priceOpen, priceSL=0, priceTP=0, priceTrigger=0, enumDirection=('BuyLong','SellShort'), enumType=('Limit','TriggerLimit','Market','TriggerMarket')):

        self.indexSignaled = indexSignaled


        self.valueVolume      = valueVolume
        self.priceOpen        = priceOpen
        self.priceSL          = priceSL
        self.priceTP          = priceTP
        self.priceTrigger     = priceTrigger
        self.istrigered       = (True) if (enumType=='Limit' or enumType=='Market') else (False)

        self.ticketOrder      = None

        self.enumDirection    = enumDirection
        self.enumType         = enumType

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



        newTrade = Trade(self.ticketOrder, self.indexOpened, self.timestampOpened, self.valueVolume, self.openedPrice, self.priceSL, self.priceTP, self.enumDirection)
        
        # if (backtesterType=='TwoWay'):
            
        #     newPosition = Position()
        #     newPosition.IncreaseTrade(newTrade)
        #     backtesterPositions.append(newPosition)
        #
        # elif (backtesterType=='OneWay'):
        #     pass
        #
    #
    
    


    def TryOpen(self, aCandlestick: CandleStick):

        if (self.enumDirection=='BuyLong'):


            if (self.enumType=='TrigerLimit'):

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
            elif (self.enumType=='TrigerMarket'):

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
            elif (self.enumType=='Market'):

                self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, (aCandlestick.low + aCandlestick.slippage))
                return
            #
            elif (self.enumType=='Limit'):
                    
                if (aCandlestick.high + aCandlestick.slippage >= self.priceOpen):

                    self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, self.priceOpen)
                    return
                #
            #
        #
        elif (self.enumDirection=='SellShort'):


            if (self.enumType=='TrigerLimit'):

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
            elif (self.enumType=='TrigerMarket'):

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
            elif (self.enumType=='Market'):

                self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, (aCandlestick.low))
                return
            #
            elif (self.enumType=='Limit'):
                    
                if (aCandlestick.low <= self.priceOpen):

                    self.NowOpen(aCandlestick.index, aCandlestick.timestampOpened, self.priceOpen)
                    return
                #
            #
        #
    #




    def TryOpen(self, aTick: Tick):

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




    def TryOpen(self, aCandleTick: CandleTick):

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

    
    def __init__(self, ticketOrder, indexOpened, valueVolume, priceOpened, priceSL=0, priceTP=0, enumDirection=('BuyLong','SellShort')):

        self.ticketOrder   = ticketOrder

        self.indexOpened   = indexOpened
        self.valueVolume   = valueVolume
        self.priceOpened   = priceOpened
        self.priceSL       = priceSL
        self.priceTP       = priceTP
        self.enumDirection = enumDirection

        self.ticketTrade   = None

        self.isTradeAlive  = False
        self.isTradeDead   = False

        self.ClosedPrice   = None

        self.valuePnL      = 0
    #




    def PrintTraded(self):

        print("Trade Ticket: ", self.ticketTrade, "\t", "PnL= ", self.valuePnL)
    #





    def GenerateTradeTicket(self):

        pass
    #




    def KillTrade(self, killingAtPrice):

        self.isTradeAlive = False
        self.isClosed     = True
        self.ClosedPrice  = killingAtPrice

        self.CalculateTradePnL(self.ClosedPrice)
    #
    

    

    def CalculateTradePnL(self, calculatingAtPrice):

        result = 0.0

        if(self.enumDirection=='BuyLong'):

            openedQuality    = (self.valueVolume*self.priceOpened)
            thisPriceQuality = (self.valueVolume*calculatingAtPrice)

            result = (thisPriceQuality-openedQuality)
        #
        elif (self.enumDirection=='SellShort'):

            openedQuality    = (self.valueVolume*self.priceOpened)
            thisPriceQuality = (self.valueVolume*calculatingAtPrice)

            result = (openedQuality-thisPriceQuality)
        #




        self.valuePnL = result
        return (result)
    #



    
    def RefreshStatus(self, aCandleStick: CandleStick):

        if (self.enumDirection=='BuyLong'):

            if (aCandleStick.low <= self.priceSL and self.priceSL!=0):

                self.KillTrade(self.priceSL)
                return
            #
            elif (aCandleStick.high+aCandleStick.slippage >= self.priceTP and self.priceTP!=0):

                self.KillTrade(self.priceTP)
                return
            #

            self.CalculateTradePnL(aCandleStick.low)
        #
        elif (self.enumDirection=='SellShort'):

            if (aCandleStick.high+aCandleStick.slippage >= self.priceSL and self.priceSL!=0):

                self.KillTrade(self.priceSL)
                return
            #
            elif (aCandleStick.low+aCandleStick.slippage <= self.priceTP and self.priceTP!=0):

                self.KillTrade(self.priceTP)
                return
            #

            self.CalculateTradePnL(aCandleStick.high+aCandleStick.slippage)
        #
    #




    def RefreshStatus(self, aTick: Tick):

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




    def RefreshStatus(self, aCandleTick: CandleTick):

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
