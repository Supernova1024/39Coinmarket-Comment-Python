import argparse
import requests
from requests.structures import CaseInsensitiveDict
import mysql.connector
from datetime import datetime
import random
from random import randrange
from random import randint
import time
import concurrent.futures
from lxml import html
import json

proxies = { 'https': 'http://lum-customer-hl_9cfd00a8-zone-data_center:bkq47uq0w1mp@zproxy.lum-superproxy.io:22225',  'http': 'http://lum-customer-hl_9cfd00a8-zone-data_center:bkq47uq0w1mp@zproxy.lum-superproxy.io:22225' }


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


for pageNumber in range(1,95):
    if pageNumber == 1:
        start = 1
    else:
        start = (pageNumber - 1) * 100
        
    page = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start='+str(start)+'&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap'
    resp = requests.get(page)
    json_data = json.loads(resp.text)

    for x in range(100):
        tokenId = json_data['data']['cryptoCurrencyList'][x]['id']
        tokenName = json_data['data']['cryptoCurrencyList'][x]['name']
        tokenName1 = tokenName.replace(".", "-")
        tokenUrl = 'https://coinmarketcap.com/currencies/'+str(tokenName1.replace(" ", "-")).lower() 

        with open('tokens.txt', 'a', encoding="utf-8") as file:
            file.write(str(tokenId)+'|'+tokenUrl+'|'+tokenName+'\n') 

'''

# Request the page
  
  
for url in URLS:
    page = requests.get(url)

    # Parsing the page
    tree = html.fromstring(page.content)
    print(tree)
    # Get element using XPath
    shares = tree.xpath("//*[contains(@class,'coin-logo')]/@src")
    #print(share)
    with open('cmc.txt', 'a') as file:
        file.write(str(shares))    

for share in shares:
    print(share)



def getData(url):
   res = requests.get(url)
   try:
       return res.json()
   except:
       return res.text
with futures.ThreadPoolExecutor(max_workers=5) as executor:
    res = executor.map(getData,URLS)
    responses = list(res) ## your list will already be pre-formated
    with open('cmc.txt', 'a') as file:
        file.write(str(responses))    
'''