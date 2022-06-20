from licensing.models import *
from licensing.methods import Key, Helpers
import requests
import subprocess    


#get HWID
def GetUUID():
   cmd = 'wmic csproduct get uuid'
   uuid = str(subprocess.check_output(cmd))
   pos1 = uuid.find("\\n")+2
   uuid = uuid[pos1:-15]
   return uuid

#auth check
def auth(my_key:str,have_license=True)-> bool:
    RSAPubKey = "<RSAKeyValue><Modulus>MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgHUJhhJVqKubqrDP867zYmx9MmOBa+gsDQ0HFNobNnJgFTaLZFiY8bL5ipAVsvptcyhAX9uVevxqhKLPc9Q9YAH/qBaXtpmjM0CGuezQjg6PqAKiri94SA6mcnSpP66XmdFguoKMUVr6Qzaz2U0u/PBpfsxRTCzeLGMVK/Q1CirLAgMBAAE=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    auth = "WyI1MzE5MzI1Iiwia3luWlQ4TjJUZDkxRmIrVzJVc0lxT0h1QkljMEdyWmJ4aExReGhjYSJd"
    result = Key.activate(token=auth,\
                       rsa_pub_key=RSAPubKey,\
                       product_id=14368, \
                       key=my_key,\
                       machine_code=GetUUID())
    if result[0] == None:
        return {'bool':False,'answer':format(result[1])}
    else:
        if have_license==False:
            with open('license.txt','w')as f:f.write(my_key)
        return True
    


#Redeem acts as auth no need for this
#def auth(hwid: str) -> bool:
#    """checks auth"""
#    with open('license.skm', 'r') as f:
#        license_key = LicenseKey.load_from_string(RSAPubKey, f.read())
#        if license_key == None or not Helpers.IsOnRightMachine(license_key):
#            return False
#        else:
#            return True

def version() -> dict:
    r = requests.get("https://api.auroratools.shop/data.json")
    return r.json()
