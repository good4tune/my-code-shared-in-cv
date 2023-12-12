import pandas as pd
import os
import datetime
from alphaVantageAPI.alphavantage import AlphaVantage
from pprint import pprint
import sys

import pymongo
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from alpha_vantage.timeseries import TimeSeries



detect = []

def calculation():
    global detect
    try:
        # yesterday's moving average
        A_50 = data_50.iloc[-2].loc['EMA']
        B_200 = data_200.iloc[-2].loc['EMA']
        Diff = A_50 - B_200
        pprint(A_50)
        pprint(B_200)
        pprint(Diff)
        
        
        #Today's Differential between EMA 200 and EMA 50
        A0_50 = data_50.iloc[-1].loc['EMA']
        B0_200 = data_200.iloc[-1].loc['EMA']
        Diff_T = A0_50 - B0_200
        pprint(A0_50)
        pprint(B0_200)
        pprint(Diff_T)

        #today's low price
        TLow = CLOSE.iloc[-1].loc['3. low']
        YLow = CLOSE.iloc[-2].loc['3. low']

        #Determining if the price has touched 50 moving average line
        if( YLow>A_50 and TLow <= A0_50):
            print(cell.value +' has touched 50 MA today')
                
        else:
            print('No touch')

        #Determining if it is a moving average golden cross
        if (Diff < 0 and Diff_T > 0) :
            pprint('EMA 50 crosses EMA 200! Buy')
            detect.append(STOCKS[x]+", ")          # Collecting Detected stock at global variable <detect>

        else:
            pprint(' ')

    except:
        pprint("Error occurred")




STOCKS = ['WORK', 'AMD', 'UBER', 'AMZN', 'DBX', 'SPOT', 'AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'AGN', 'AIG', 'ALL', 'AMGN', 'AMT', 'AMZN', 'AXP', 'BA', 'BAC', 'BIIB', 'BK', 'BKNG', 'BLK', 'BMY', 'BRK.B', 'C', 'CAT', 'CHTR', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CSCO', 'CVS', 'CVX', 'DD', 'DHR', 'DIS', 'DOW', 'DUK', 'EMR', 'EXC', 'F', 'FB', 'FDX', 'GD', 'GE', 'GILD', 'GM', 'GOOG', 'GOOGL', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KHC', 'KMI', 'KO', 'LLY', 'LMT', 'LOW', 'MA', 'MCD', 'MDLZ', 'MDT', 'MET', 'MMM', 'MO', 'MRK', 'MS', 'MSFT', 'NEE', 'NFLX', 'NKE', 'NVDA', 'ORCL', 'OXY', 'PEP', 'PFE', 'PG', 'PM', 'PYPL', 'QCOM', 'RTN', 'SBUX', 'SLB', 'SO', 'SPG', 'T', 'TGT', 'TMO', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VZ', 'WBA', 'WFC', 'WMT', 'XOM', 'ATVI', 'ADBE', 'AMD', 'ALXN', 'ALGN', 'GOOG', 'GOOGL', 'AMZN', 'AMGN', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ASML', 'ADSK', 'ADP', 'BIDU', 'BIIB', 'BMRN', 'BKNG', 'AVGO', 'CDNS', 'CDW', 'CERN', 'CHTR', 'CHKP', 'CTAS', 'CSCO', 'CTXS', 'CTSH', 'CMCSA', 'CPRT', 'COST', 'CSX', 'DXCM', 'DOCU', 'DLTR', 'EBAY', 'EA', 'EXC', 'EXPE', 'FB', 'FAST', 'FISV', 'FOX', 'FOXA', 'GILD', 'IDXX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JD', 'KLAC', 'LRCX', 'LBTYA', 'LBTYK', 'LULU', 'MAR', 'MXIM', 'MELI', 'MCHP', 'MU', 'MSFT', 'MRNA', 'MDLZ', 'MNST', 'NTES', 'NFLX', 'NVDA', 'NXPI', 'ORLY', 'PCAR', 'PAYX', 'PYPL', 'PEP', 'PDD', 'QCOM', 'REGN', 'ROST', 'SGEN', 'SIRI', 'SWKS', 'SPLK', 'SBUX', 'SNPS', 'TMUS', 'TTWO', 'TSLA', 'TXN', 'KHC', 'TCOM', 'ULTA', 'VRSN', 'VRSK', 'VRTX', 'WBA', 'WDC', 'WDAY', 'XEL', 'XLNX', 'ZM']
ts = AlphaVantage(api_key='XXXXXXXXXXXXXX4', datatype='pandas')
time = TimeSeries(key = 'XXXXXXXXXXXX4', output_format='pandas')



for x in range(0, len(STOCKS)):
    try:
 
        data_50 = ts.data(symbol=STOCKS[x], function = 'EMA', interval='daily', time_period=50, series_type='close')
        data_200 = ts.data(symbol=STOCKS[x], function = 'EMA', interval='daily', time_period=200, series_type='close')
        CLOSE, meta_data = time.get_daily(symbol=STOCKS[x], outputsize='full')
        
        pprint(STOCKS[x])

        calculation()

    except:
        print("A problem exists during connection to Alpha Vantage")





if (len(detect) >= 1):
    #Retrieving customers' email addresses from MongoDB and storing email addresses in variable <emaildata>
    emaildata =[]
    myclient = pymongo.MongoClient("mongodb+srv://MyIDforMongoDB:XXXXXXXXcluster0-gui48.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["stocktech"]
    mycol = mydb["users"]

    for x in mycol.find({"purchase":"y"},{ "_id": 0, "username": 1}):
        emaildata.append(x["username"])
    print(emaildata)   #Customer email addresses
    
    print(detect)       # Detected Stocks
    
# Trigger to send notification email using SendGrid template Email Delivery API
    message = Mail(
        from_email='goody@hotmail.com',
        to_emails=emaildata,
        html_content='<strong>Strong buy signal detected today!</strong>')
    message.dynamic_template_data = {
        'subject': 'Buy Signal Detected Today!',
        'name': detect
        
    }
    message.template_id = 'd-8dffXXXXXXXXXX4a99236'
    try:
        sendgrid_client = SendGridAPIClient(api_key='SG.UlXXXXXXXXXXXXXXXXXXXXXXXXQ6Osvw7Pyj5ymuNNCtEtRJMgLmEKZ7g')
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


 
else:
    print("nothing detected today")







