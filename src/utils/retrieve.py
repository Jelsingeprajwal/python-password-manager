from utils.dbconfig import dbconfig
from rich import print as printc
from rich.table import Table
from rich.console import Console
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import utils.aesutil
import pyperclip

console = Console()
# print('retrieve.py')


def computeMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def retrieveEntries(mp, ds, search, decryptPassword=False):
    # print('retrieve()')
    db = dbconfig()
    if len(search) == 0:
        results = db[2].find()
    else:
        results = db[2].find(search)
    results = list(results)
    if len(results) == 0:
        printc("[yellow][+][/yellow] No search results for the search")
        return

    if (decryptPassword and len(results) > 1) or (not decryptPassword):
        table = Table()
        table.add_column("Site Name")
        table.add_column("URL", )
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")
        for res in results:
            table.add_row(res['sitename'], res['siteurl'], res['email'],
                          res['username'], res['password'])
        console.print(table)

    if len(results) == 1 and decryptPassword:
        mk = str(computeMasterKey(mp, ds))
        decrepted = utils.aesutil.decrypt(
            key=mk, source=results[0]['password'], keyType="bytes")
        pyperclip.copy(str(decrepted)[2:-1])


# print('retrieve.py end')
