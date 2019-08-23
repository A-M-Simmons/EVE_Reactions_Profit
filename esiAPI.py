import urllib.request, json 

def getHistoricalMarketData(type_id):
    url = f"https://esi.evetech.net/latest/markets/10000002/history/?datasource=tranquility&type_id={type_id}"
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    
    parse_data = []
    if len(data) >= 30:
        parse_data = data[-30:]
    else:
        parse_data = data
    return parse_data


def getMarketPrices():
    urlSwagger = "https://esi.evetech.net/latest/markets/prices/?datasource=tranquility"
    with urllib.request.urlopen(urlSwagger) as url:
        data = json.loads(url.read().decode())
    marketPrices = {}
    for d in data:
        marketPrices[d['type_id']] = d
    return marketPrices

def getMarketOrderPrices(BPs):
    materials = getMaterials(BPs)
    prices = {}
    for type_id in materials:
        orders = getOrders(type_id)
        avgPrice = getFivePercentPrice(orders)
        print(f"Type_ID: {type_id}, Orders: {len(orders)}, Avg_Price: {avgPrice}")
        prices[type_id] = {'average_price': avgPrice}
    return prices

def getFivePercentPrice(orders):
    # Get total number of materials in sell orders
    q = 0
    for o in orders:
        q += o[1]
    
    q5 = 0.05*q
    q5q = 0
    qfCost = 0
    for o in orders:
        if q5q + o[1] >= q5:
            qfCost += o[0]*(q5 - q5q)
            q5q += (q5 - q5q)
            break
        else:
            qfCost += o[0]*o[1]
            q5q += o[1]
    avgPrice = qfCost/q5q
    return avgPrice

def getOrders(type_id, sort_dir="up"):
    orders = []
    urlSwagger = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=sell&page=1&type_id={type_id}"
    with urllib.request.urlopen(urlSwagger) as url:
        data = json.loads(url.read().decode())
        for d in data:
            orders.append( (d['price'], d['volume_remain']) )
        if sort_dir=="up":
            orders.sort(key=lambda tup: tup[0])
        else:
            orders.sort(key=lambda tup: tup[0], reverse=True)
    return orders

def getMaterials(BPs):
    materials = []
    for bp in BPs:
        for mat in bp.inputs:
            materials.append(mat[0])
    materials = set(materials)
    return materials

def getSellPrice(type_id):
    orders = getOrders(type_id, sort_dir="up")
    return orders[0][0]