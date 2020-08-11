#!/usr/bin/env python
# coding: utf-8

def parse_webhook(webhook_data):
    import ast
    data = ast.literal_eval(webhook_data)
    return data


def order_execution(data):
    from bybit import bybit
    from bitmex import bitmex
    import requests
    import json
    import warnings
    warnings.simplefilter("ignore")
    if data['Exchange'] == 'Bybit':
        #Input your Bybit API credentials here
        api_key = 'YOUR API KEY HERE'
        api_secret = 'YOUR API SECRET HERE'
        
        client = bybit(test=False,api_key=api_key,
                       api_secret=api_secret)
        
        #Get Current Open Position Data
        try:
            OPENPOSITION = [x for x in client.Positions.Positions_myPosition().result()[0]['result'] if x['symbol'] == 'BTCUSD' and x['side'] != 'None'][0]
        except IndexError:
            OPENPOSITION = 'None'
            
        if OPENPOSITION != 'None':
            SIDE = OPENPOSITION['side']
        else:
            SIDE = 'None'
        
        if SIDE != data['Side']:
            if SIDE != 'None':
                #Execute Close Orders if in Position
                SIZE = OPENPOSITION['size']
                if SIDE == 'Buy':
                    client.Order.Order_newV2(symbol='BTCUSD', side='Sell', order_type='Market', qty=SIZE, time_in_force='GoodTillCancelled').result();
                else:
                    client.Order.Order_newV2(symbol='BTCUSD', side='Buy', order_type='Market', qty=SIZE, time_in_force='GoodTillCancelled').result();
            
            #Update Balance and Set Leverage to 1x
            balance = client.Wallet.Wallet_getBalance(coin='BTC').result()[0]['result']['BTC']['equity']
            client.Positions.Positions_saveLeverage(symbol='BTCUSD', leverage='1').result()
            
            #Open New Position
            if data['Side'] == 'Sell':
                market_price = float([x['bid_price'] for x in requests.get('https://api.bybit.com/v2/public/tickers?symbol=BTCUSD').json()['result']][0])
            else:
                market_price = float([x['ask_price'] for x in requests.get('https://api.bybit.com/v2/public/tickers?symbol=BTCUSD').json()['result']][0])
            size = int(((market_price + (market_price*0.0015))*balance)*0.995)
            client.Order.Order_newV2(symbol='BTCUSD', side=data['Side'], order_type='Market', qty=size, time_in_force='GoodTillCancelled').result();
            
            msg = 'Bybit '+data['Side']+' Order Executed'
        else:
            msg = 'Bybit '+data['Side']+' False Signal'
    
    elif data['Exchange'] == 'Bitmex':
        #Input your Bitmex API credentials here
        api_key = 'YOUR API KEY HERE'
        api_secret = 'YOUR API SECRET HERE'
        
        client = bitmex(test=False,api_key=api_key,
                       api_secret=api_secret)
        
        #Get Current Open Position Data
        try:
            OPENPOSITION = client.Position.Position_get(filter=json.dumps({'isOpen': True, 'symbol': 'XBTUSD'})).result()[0][0]
        except IndexError:
            OPENPOSITION = 'None'
            SIDE = 'None'
            
        if OPENPOSITION != 'None':
            SIZE = OPENPOSITION['currentQty']
            if SIZE > 0:
                SIDE = 'Buy'
            else:
                SIDE = 'Sell'
        if SIDE != data['Side']:
            if SIDE == 'Buy':
                client.Order.Order_new(symbol='XBTUSD', execInst='Close', side='Sell').result();
                balance = client.User.User_getWalletHistory().result()[0][0]['walletBalance']/100000000
                market_price = client.Instrument.Instrument_get(symbol='XBTUSD').result()[0][0]['askPrice']
                size = int(((market_price + (market_price*0.0015))*balance)*0.995)
                client.Order.Order_new(symbol='XBTUSD', orderQty=size, ordType='Market', side='Sell').result();
            elif SIDE == 'Sell':
                client.Order.Order_new(symbol='XBTUSD', execInst='Close', side='Buy').result()
                balance = client.User.User_getWalletHistory().result()[0][0]['walletBalance']/100000000
                market_price = client.Instrument.Instrument_get(symbol='XBTUSD').result()[0][0]['bidPrice']
                size = int(((market_price + (market_price*0.0015))*balance)*0.995)
                client.Order.Order_new(symbol='XBTUSD', orderQty=size, ordType='Market', side='Buy').result();
            else:
                balance = client.User.User_getWalletHistory().result()[0][0]['walletBalance']/100000000
                if data['Side'] == 'Buy':
                    market_price = client.Instrument.Instrument_get(symbol='XBTUSD').result()[0][0]['bidPrice']
                    size = int(((market_price + (market_price*0.0015))*balance)*0.995)
                    client.Order.Order_new(symbol='XBTUSD', orderQty=size, ordType='Market', side='Buy').result();
                else:
                    market_price = client.Instrument.Instrument_get(symbol='XBTUSD').result()[0][0]['askPrice']
                    size = int(((market_price + (market_price*0.0015))*balance)*0.995)
                    client.Order.Order_new(symbol='XBTUSD', orderQty=size, ordType='Market', side='Sell').result();
            msg = 'Bitmex '+data['Side']+' Order Executed'
        else:
            msg = 'Bitmex '+data['Side']+' False Signal'
    return msg

