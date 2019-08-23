from __future__ import print_function
import pickle
import os.path
import csv
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
from getBlueprintData import checkPickle, buildService, getBlueprints
from esiAPI import getMarketPrices, getMarketOrderPrices, getSellPrice, getHistoricalMarketData
from databaseConn import create_connection, getBlueprintIO
from openpyxl import load_workbook
from models import Blueprint

def updateJITABuySellPrice(BPs):
    # Market Prices for components
    compMarketPrices =  getMarketOrderPrices(BPs)
    marketPrices = getMarketPrices()
    buyPrices = []
    sellPrices = []
    baseCosts = []
    lines = []
    for bp in BPs:
        bcp = bp.getBaseCostPrice(marketPrices)
        compB = bp.getPrice(compMarketPrices, "Buy")
        buyP, sellP = bp.getOutputJitaPrice()
        lines.append(f"{bp.id},{bcp},{compB},{sellP},{buyP}\n")

    with open('jitaPrices.csv', 'w', newline='') as f:
            f.writelines(lines)

def updatePricesVolsCSV(BPs):
    priceLines = []
    volLines = []
    for bp in BPs:
        l = bp.getHistorical(30)
        prices, vols = updateReactions30dAvgPrice(l)
        priceLines.append(f"{bp.id},{prices}\n")
        volLines.append(f"{bp.id},{vols}\n")
    
    with open('prices.csv', 'w', newline='') as f:
        for line in priceLines:
            f.writelines(line)

    with open('volumes.csv', 'w', newline='') as f:
        for line in volLines:
            f.writelines(line)

def updateReactions30dAvgPrice(l):
    prices = ""
    vols = ""
    for t in l:
        prices += f"{t[0]},"
        vols += f"{t[1]},"
    return prices, vols


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
        bpIDs.append(Blueprint(bp[0].value))
    return bpIDs

def main():    
    conn = create_connection("blueprintDatabase.db")
    reactionBPIDs = getReactionBPs()
    
    print("Calculating...")
    for bp in reactionBPIDs:
        bp.setIO(conn)
        #bp.obtainHistorical()

    updateJITABuySellPrice(reactionBPIDs)


if __name__ == '__main__':
    main()