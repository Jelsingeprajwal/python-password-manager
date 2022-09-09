import pymongo
from pymongo import MongoClient
from rich import print as printc
from rich.console import Console
console = Console()
# print("dbconfig accessed")


def dbconfig():
    # print("dbconfig() accessed")
    try:
        db = pymongo.MongoClient("mongodb://localhost:27017")
    except Exception as e:
        console.print_exception(e)
    database_list = db.list_database_names()
    if 'pw' not in database_list:
        printc("[green][+][/green] Creating a new database")
        mydb = db["pw"]
    mydb = db.pw
    collections_list = mydb.list_collection_names()
    if "secrets" not in collections_list:
        mydb.create_collection("secrets")
        printc("[green][+][/green] Creating 'secrets' Collection ")
    if "entries" not in collections_list:
        mydb.create_collection("entries")
        printc("[green][+][/green] Creating 'entries' Collection ")
    printc()
    secrets_collection = mydb.secrets
    entries_collection = mydb.entries
    return [db, secrets_collection, entries_collection]


# print("dbconfig accessed end")
