import sqlite3
import os

directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
dbDir = directory + r"/database/sqllite.db"


def get_scenario_name():
    path = dbDir
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql_ = f"""Select distinct name_scenario, priority from sc_request"""
    result = c.execute(sql_)
    ReqData = []
    for i in result:
        ReqItem = {}
        ReqItem["name_scenario"] = i[0]
        ReqItem["priority"] = i[1]
        ReqData.append(ReqItem)
    conn.close()
    return ReqData


def get_scenario_detail(name):
    path = dbDir
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql_ = f"""Select * from sc_request where name_scenario = '{name}'"""
    result = c.execute(sql_)
    ReqData = []
    for i in result:
        ReqItem = {}
        ReqItem["name_scenario"] = i[0]
        ReqItem["priority"] = i[1]
        ReqItem["type_request"] = i[2]
        ReqItem["resource"] = i[3]
        ReqItem["body"] = i[4]
        ReqData.append(ReqItem)
    conn.close()
    return ReqData
