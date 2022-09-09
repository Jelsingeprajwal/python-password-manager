from utils.dbconfig import dbconfig
from getpass import getpass
from rich import print as printc
from rich.console import Console
import hashlib
import random
import string
console = Console()
# print('config.py')


def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def config():
    # create the database and collections
    db = dbconfig()

    while 1:
        mp = getpass("Enter the Master password: ")
        if mp == getpass("Re-Type password: ") and mp != "":
            break
        printc("[yellow] Please try again[/yellow]")
    # hash the master password
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")
    # generate device secret
    ds = generateDeviceSecret()
    printc("[green][+][/green] Device Secret generated")
    # add them to db
    db[1].insert_one({
        "masterkey hash": hashed_mp,
        "device secret": ds
    })
    db[0].close()
    printc(" [green][+][/green] Added to the database ")
    printc(" [green][+] Configuration done ! [/green] ")


config()

# print('config.py end')
