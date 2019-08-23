from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from getBlueprintData import checkPickle, buildService, getBlueprints
from esiAPI import getMarketPrices, getMarketOrderPrices, getSellPrice
from databaseConn import create_connection, getBlueprintIO

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''

def updateReactions30dAvgPrice():
    pass

def updateBaseCost(service, spreadsheet_id, v):
    values = v
    body = {
        'values': values
    }
    range_name = 'Blueprint_Market!C2:E'
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name, valueInputOption="RAW", body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def main():    
    print("Connecting to database")
    conn = create_connection("test.db")
    print("Gathering Market Prices")
    marketPrices = getMarketPrices()
    
    print("Acquiring Google Sheets Blueprints")
    creds = checkPickle(SCOPES)
    service = buildService(creds)
    blueprints = getBlueprints(SAMPLE_SPREADSHEET_ID, service)
    
    BCP = []
    print("Calculating...")
    for bp in blueprints:
        bp.setIO(conn)
    
    compMarketPrices =  getMarketOrderPrices(blueprints)
    for bp in blueprints:
        bcp = bp.getBaseCostPrice(marketPrices)
        buyP = bp.getPrice(compMarketPrices, "Buy")
        sellP = getSellPrice(bp.output[0])*bp.output[1]
        BCP.append([buyP, sellP, bcp])


    print("Updating Google Sheet")
    updateBaseCost(service, SAMPLE_SPREADSHEET_ID, BCP)
if __name__ == '__main__':
    main()