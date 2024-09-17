import os
import sqlite3
import json

directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FileHarDir = directory + r"/BaseHar/"
dbDir = directory + r"/database/sqllite.db"


def getFileList():
    ListFile = []
    for f in os.listdir(FileHarDir):
        if os.path.isdir(FileHarDir + "/" + f) == False:
            item = {}
            item["path"] = FileHarDir + f
            item["name"] = f
            item["format"] = str(f).split('.')[-1]
            if item["format"] == "har":
                ListFile.append(item)
    return ListFile


def createDB():
    path = dbDir
    if os.path.exists(path):
        conn = sqlite3.connect(path)
        sql_ = """drop table sc_request"""
        c = conn.cursor()
        c.execute(sql_)
        conn.commit()
        conn.close()
    else:
        f = open(path, 'w')
        f.close()

    conn = sqlite3.connect(path)
    sql_ = f"""CREATE TABLE sc_request
                (
                    name_scenario text not null,
                    priority int NOT NULL,
                    type_request TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    body blob
                )"""
    c = conn.cursor()
    c.execute(sql_)
    conn.commit()
    conn.close()


def analystSingleHar(har):
    print(har["path"])
    priority = har["name"].split("!")[0]
    f = open(har["path"], 'r', encoding='UTF-8')
    templates = json.loads(f.read())

    for i in templates["log"]["entries"]:
        if "request" in i.keys() and "method" in i["request"].keys() \
                and i["request"]["method"] in ["GET", "POST", "PUT"] \
                and "/api" in str(i["request"]["url"]) \
                and "wss:" not in str(i["request"]["url"]) \
                and "icon.svg" not in str(i["request"]["url"]):
            item = {}
            item["priority"] = priority
            item["name_scenario"] = har["name"]
            item["type_request"] = i["request"]["method"]
            tmp_path = i["request"]["url"].replace("https://", "").replace("http://", "").split("/")[1:]
            item["resource"] = "/" + "/".join(tmp_path)
            if "postData" in i["request"].keys() and len(i["request"]["postData"]) != 0:
                body = str(i["request"]["postData"]["text"]).replace("'", '"')
                body = body.replace("null", "None")
                body = body.replace("true", "True").replace("false", "False")
                item["body"] = body
            else:
                item["body"] = 'null'
            writeDB(item)
    return


def writeDB(item):
    path = dbDir
    conn = sqlite3.connect(path)
    c = conn.cursor()
    sql_ = f"""insert into sc_request
                (name_scenario,priority,type_request,resource,body)
                values
                ({null_or_notNull(item["name_scenario"])},{item["priority"]},{null_or_notNull(item["type_request"])},
                {null_or_notNull(item["resource"])},{null_or_notNull(item["body"])})"""
    c.execute(sql_)
    conn.commit()
    conn.close()


def null_or_notNull(tmp):
    if tmp == "null":
        return tmp
    else:
        return "'" + str(tmp) + "'"


def main():
    createDB()
    FileList = getFileList()
    for i in FileList:
        analystSingleHar(i)
