from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import requests
import capitalcom

class CapitalcomData():
    def __init__(self, symbol):
        self.client = capitalcom.client.Client('hoangdev161201@gmail.com', 'Cuem1612@', 'nC9hhJDMkSqMDa7C')
        self.symbol = symbol

    def get_current_price(self):
        price = self.client.single_market(self.symbol)
        return price['snapshot']['bid']
    
    def search_market(self, symbol):
        return self.client.searching_market(symbol)
    
    def get_prices_history(self, resource, max ):
        return self.client.historical_price(self.symbol, resource, max)