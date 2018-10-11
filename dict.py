#!/bin/python

dict = {'currency': 'USD', 'symbol': 'AAPL', 'exchangeName': 'NMS', 'instrumentType': 'EQUITY', 'firstTradeDate': 345459600, 'gmtoffset': -14400, 'timezone': 'EDT', 'exchangeTimezoneName': 'America/New_York', 'chartPreviousClose': 216.36, 'priceHint': 2, 'currentTradingPeriod': {'pre': {'timezone': 'EDT', 'start': 1539244800, 'end': 1539264600, 'gmtoffset': -14400}, 'regular': {'timezone': 'EDT', 'start': 1539264600, 'end': 1539288000, 'gmtoffset': -14400}, 'post': {'timezone': 'EDT', 'start': 1539288000, 'end': 1539302400, 'gmtoffset': -14400}}, 'dataGranularity': '3mo', 'validRanges': ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']}

print(dict.get("symbol"))