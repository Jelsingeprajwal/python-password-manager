from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import utils.aesutil
from utils.dbconfig import dbconfig
from rich import print as printc
# print("add.py accessed")


def computeMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def addEntry(mp, ds, sitename, siteurl, email, username):
    # get the password
    password = getpass("Password: ")
    mk = str(computeMasterKey(mp, ds))
    print(mk)
    print(type(mk))
    encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType="bytes")
    db = dbconfig()
    db[2].insert_one({
        "sitename": sitename,
        "siteurl": siteurl,
        "email": email,
        "username": username,
        "password": encrypted
    })
    printc("[green][+][/green] Added Entry")


# print('add.py end')
