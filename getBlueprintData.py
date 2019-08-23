from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from databaseConn import getBlueprintIO

class Blueprint():
    def __init__(self, data):
        self.name = data[0]
        self.id = data[1]
        self.type = data[2]
        self.subtype = data[3]
        self.qty = data[4]
        self.time = data[5]
        self.me = data[6]
        self.te = data[7]
        self.compvol = data[8]
        self.prodvol = data[9]
    
    def setIO(self, conn):
        i, o = getBlueprintIO(conn, self.id)
        self.inputs = i
        self.output = o       

    def getBaseCostPrice(self, marketPrices):
        basecostprice = 0
        for i in self.inputs:
            basecostprice += marketPrices[i[0]]['adjusted_price']*i[1]
        return(basecostprice)
    
    def getPrice(self, marketPrices, mtype):
        amount = 0
        if mtype == "Buy":
            for i in self.inputs:
                amount += marketPrices[i[0]]['average_price']*i[1]
        if mtype == "Sell":
            amount = marketPrices[self.output[0]]['average_price']*self.output[1]
        return(amount)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def checkPickle(SCOPES):    
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def buildService(creds):
    service = build('sheets', 'v4', credentials=creds)
    return service

def getBlueprints(SAMPLE_SPREADSHEET_ID, service):
    SAMPLE_RANGE_NAME = 'Blueprints!A2:M'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    blueprints = []
    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            blueprints.append(Blueprint(row))
    return blueprints
