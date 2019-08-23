from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from getBlueprintData import checkPickle, buildService, getBlueprints
from esiAPI import getMarketPrices, getMarketOrderPrices, getSellPrice
from databaseConn import create_connection, getBlueprintIO
from openpyxl import load_workbook

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

def getReactionBPs():
    wb = load_workbook(filename = 'eve_industry.xlsx')
    sheet_ranges = wb['MasterPrice_Reactions']
    bpIDsCells = sheet_ranges['A6:A50']
    bpIDs = []
    for bp in bpIDsCells:
        bpIDs.append(bp[0].value)
    return bpIDs

def main():    
    conn = create_connection("test.db")
    reactionBPIDs = getReactionBPs()
    
    print("Calculating...")
    for bp in reactionBPIDs:
        bp.setIO(conn)

if __name__ == '__main__':
    main()