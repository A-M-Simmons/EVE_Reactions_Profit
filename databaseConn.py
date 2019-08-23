import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def getBlueprintIO(conn, blueprintID):    
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    request = f"SELECT COUNT(*) FROM industryActivity WHERE typeID={blueprintID}"
    cur = conn.cursor()
    cur.execute(request)
    rows = cur.fetchall()
    if rows[0][0] > 0:
        return getIndustryMaterials(conn, blueprintID)
    else:
        return getReactionMaterials(conn, blueprintID)

def getIndustryMaterials(conn, blueprintID):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    request = f"SELECT materialTypeID, quantity FROM industryActivityMaterials WHERE typeID={blueprintID} AND (activityID=1 OR activityID=11)"
    cur = conn.cursor()
    cur.execute(request)
 
    rows = cur.fetchall()
    inputs = []
    for row in rows:
        inputs.append(row)

    request = f"SELECT * FROM industryActivityProducts WHERE typeID={blueprintID} AND (activityID=1 OR activityID=11)"
    cur.execute(request) 
    rows = cur.fetchall()
    output = (rows[0][2], rows[0][3])
    return inputs, output

def getReactionMaterials(conn, blueprintID):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    request = f"SELECT * FROM invTypeReactions WHERE reactionTypeID={blueprintID}"
    cur = conn.cursor()
    cur.execute(request)
 
    rows = cur.fetchall()
    inputs = []
    for row in rows:
        q = getReactionAmounts(conn, row[2])
        if row[1] == 0:
            output = (row[2], q)
        else:
            inputs.append((row[2], q))
    return inputs, output

def getReactionAmounts(conn, ID):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    request = f"SELECT valueInt FROM dgmTypeAttributes WHERE typeID={ID} AND attributeID=726"
    cur = conn.cursor()
    cur.execute(request) 
    rows = cur.fetchall()
    if len(rows) == 0:
        return 1
    else:
        return rows[0][0]

