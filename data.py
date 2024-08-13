import re

foreignCurrencies = [
'AUD/CAD',
'AUD/CHF',
'AUD/JPY',
'AUD/NZD',
'AUD/USD',
'EUR/AUD',
'GBP/AUD',
'CAD/CHF',
'CAD/JPY',
'EUR/CAD',
'GBP/CAD',
'NZD/CAD',
'USD/CAD',
'CHF/JPY',
'EUR/CHF',
'GBP/CHF',
'NZD/CHF',
'USD/CHF',
'EUR/GBP',
'EUR/JPY',
'EUR/NZD',
'EUR/USD',
'GBP/JPY',
'GBP/NZD',
'GBP/USD',
'NZD/JPY',
'XAU/USD'
] 

api_id = '24104392'
api_hash = '3b479abb8cd0b6970cc33a54335dc4e0'


def tradewithpatfreeMsg(msg):
    if 'Trade Safely' in msg.message:
        result = f'{msg.date}@{'sell' if 'Sell' in msg.message else 'buy'}@'
        # use regex to find number by .
        values = re.findall(r'\d+\.\d+', msg.message)
        result = f'{result}{'@'.join(values)}'
        return result
    return None


return_msg_dict = {
    '@tradewithpatfree': tradewithpatfreeMsg
    '@GoldTradesignals11': d,
    '@forexstarteam': s,
    '@goldsignalsvip_S'

}
