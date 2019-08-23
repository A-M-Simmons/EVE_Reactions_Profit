from databaseConn import getBlueprintIO
from esiAPI import getHistoricalMarketData
import urllib.request, json 
import ssl

class Blueprint():
    def __init__(self, type_id):
        self.id = type_id
    
    def setIO(self, conn):
        i, o = getBlueprintIO(conn, self.id)
        self.inputs = i
        self.output = o       

    def getBaseCostPrice(self, marketPrices):
        basecostprice = 0
        for i in self.inputs:
            basecostprice += marketPrices[i[0]]['adjusted_price']*i[1]
        return(basecostprice)

    def getOutputJitaPrice(self):
        buyPrice = 0
        sellPrice = 0
        context = ssl._create_unverified_context()

        # Buy Price
        orders = []
        urlSwagger = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=buy&page=1&type_id={self.output[0]}"
        with urllib.request.urlopen(urlSwagger, context=context) as url:
            data = json.loads(url.read().decode())
            for d in data:
                orders.append( (d['price'], d['volume_remain']) )
            orders.sort(key=lambda tup: tup[0], reverse=True)
        buyPrice = orders[0][0]
    
        # Sell Price
        orders = []
        urlSwagger = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=sell&page=1&type_id={self.output[0]}"
        with urllib.request.urlopen(urlSwagger, context=context) as url:
            data = json.loads(url.read().decode())
            for d in data:
                orders.append( (d['price'], d['volume_remain']) )
            orders.sort(key=lambda tup: tup[0])
        sellPrice = orders[0][0]

        return buyPrice, sellPrice
    
    def getPrice(self, marketPrices, mtype):
        amount = 0
        if mtype == "Buy":
            for i in self.inputs:
                amount += marketPrices[i[0]]['average_price']*i[1]
        if mtype == "Sell":
            amount = marketPrices[self.output[0]]['average_price']*self.output[1]
        return(amount)
    
    def obtainHistorical(self):
        self.HistoricalPrices = getHistoricalMarketData(self.output[0])

    def getHistorical(self, N):
        l = []
        for d in self.HistoricalPrices.data[-N:]:
            l.append((d['average'],d['volume']/self.output[1]))
        return l