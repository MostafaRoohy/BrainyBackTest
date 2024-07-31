import pandas as pd
import numpy  as np
import random
from Classes.Candle import *




############################################################################################################
# A SignalRequest is like a clue that is inside an Indicator's buffer, so the Brain can act upon these clues.
############################################################################################################
class SignalRequest:


    _Fingerprints = []


    def __init__(self, action=('Limit','TriggerLimit','Market','TriggerMarket','CloseAll','Close','ModifyTrigger','ModifyTP','ModifySL'), direction=('BuyLong','SellShort'), priceTrigger=0.0, priceOpen=0.0, priceTP=0.0, priceSL=0.0, valueVolume=0.0, byFingerprint=0):
        
        self.action        = action
        self.direction     = direction

        self.priceTrigger  = priceTrigger
        self.priceOpen     = priceOpen
        self.priceTP       = priceTP
        self.priceSL       = priceSL
        self.valueVolume   = valueVolume

        self.byFingerprint = byFingerprint



        while (True):

            newFingerPrint = random.randint(1000000, 10000000-1)

            if(newFingerPrint not in SignalRequest._Fingerprints):
                
                SignalRequest._Fingerprints.append(newFingerPrint)
                
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
        self.isAlive          = True
        self.isDead           = False
        self.isCancelled      = False
        self.isOrderOpened    = False
        self.indexOpened      = None
        self.timestampOpened  = None
        self.priceOpened      = None
    #


    def NowOpen(self, indexOpening, timestampOpening, priceOpening):

        self.indexOpened     = indexOpening
        self.timestampOpened = timestampOpening
        self.isOpened        = True
        self.isAlive         = False
        self.isDead          = True
        self.openedPrice     = priceOpening



        newTrade = Trade(self.fingerprint, self.indexOpened, self.timestampOpened, self.type, self.direction, self.valueVolume, self.priceTrigger, self.openedPrice, self.priceSL, self.priceTP)

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

                    self.NowOpen(aCandlestick.index, aCandlestick.timestampA, (aCandlestick.low + aCandlestick.averageSlippage))
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

                
                return (self.NowOpen(aCandlestick.index, aCandlestick.timestampA, (aCandlestick.low + aCandlestick.averageSlippage)))
            #
            elif (self.type=='Limit'):
                    
                if (aCandlestick.high + aCandlestick.averageSlippage >= self.priceOpen):

                    return (self.NowOpen(aCandlestick.index, aCandlestick.timestampA, self.priceOpen))
                #
            #
        #
        elif (self.direction=='SellShort'):


            if (self.type=='TrigerLimit'):

                if (self.trigered==True):

                    if (aCandlestick.low <= self.priceOpen):

                        self.NowOpen(aCandlestick.index, aCandlestick.timestampA, self.priceOpen)
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

                    self.NowOpen(aCandlestick.index, aCandlestick.timestampA, (aCandlestick.low))
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


    def CancelOrder(self):

        self.indexOpened      = 0
        self.timestampOpened  = 0
        self.isAlive          = False
        self.isDead           = True
        self.isCancelled      = True
        self.openedPrice      = 0
    #
#




############################################################################################################
# A Trade is an Opened Order.
############################################################################################################
class Trade:
    

    _Fingerprints = []

    
    def __init__(self, fingerprint, indexOpened, timestampOpened, type, direction, valueVolume, priceTriggered, priceOpened, priceSL, priceTP):


        Trade._Fingerprints.append(fingerprint)
        #
        self.fingerprint      = Trade._Fingerprints[-1]


        self.indexOpened      = indexOpened
        self.timestampOpened  = timestampOpened


        self.type             = type
        self.direction        = direction

        self.valueVolume      = valueVolume
        self.priceTriggered   = priceTriggered
        self.priceOpened      = priceOpened
        self.priceSL          = priceSL
        self.priceTP          = priceTP


        self.isAlive          = True
        self.isDead           = False
        self.ClosedPrice      = None


        self.valuePnL         = 0
    #


    def PrintTraded(self):

        print("Trade Ticket: ", self.ticketTrade, "\t", "PnL= ", self.valuePnL)
    #


    def EndTrade(self, EndingAtPrice):

        self.isAlive      = False
        self.isDead       = True
        self.ClosedPrice  = EndingAtPrice

        self.CalculateTradePnL(EndingAtPrice)
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
            elif (aCandleStick.high+aCandleStick.averageSlippage >= self.priceTP and self.priceTP!=0):

                self.EndTrade(self.priceTP)
                return
            #

            self.CalculateTradePnL(aCandleStick.low)
        #
        elif (self.direction=='SellShort'):

            if (aCandleStick.high+aCandleStick.averageSlippage >= self.priceSL and self.priceSL!=0):

                self.EndTrade(self.priceSL)
                return
            #
            elif (aCandleStick.low+aCandleStick.averageSlippage <= self.priceTP and self.priceTP!=0):

                self.EndTrade(self.priceTP)
                return
            #

            self.CalculateTradePnL(aCandleStick.high+aCandleStick.averageSlippage)
        #
    #
#
