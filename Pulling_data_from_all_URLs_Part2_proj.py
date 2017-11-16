from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import numpy as np

url=['http://profit.ndtv.com/stock/glenmark-pharmaceuticals-ltd_glenmark/research/report3664'
,'https://trendlyne.com/research-reports/stock/1261/SOBHA/sobha-limited/',
'https://trendlyne.com/research-reports/buy/',
'http://www.stocklinedirect.com/stock-tips-TATAMOTORS.html',
'http://www.religareonline.com/research/intraday-trading-tips/equities/1#',
'http://profit.ndtv.com/stock/glenmark-pharmaceuticals-ltd_glenmark/research/report3664'] #
"""  """
# Stockline Direct & NDTV should be given input as href url's  (Href URL's Get from Main Pagae Source code
#


def beauty_func(url):
    data = soup(requests.get(url).text,'html.parser')
    source=url.split('//')[1].split('/')[0]
    return data

def get_data(url):
    global x
    global recommandation
    recommandation = []
    rec_data = []
    x = 0


    for tr in beauty_func(url).find_all(['tr']):    # 'tr'   and 'td' to be call from property file

        if len(tr.find_all('td')) > 0:
            rec_data.append([])
            i=0
            for td in tr.find_all('td'):
                i+=1
                # For trendylyne  some of the field's are getting blank, because of that index are misplacing
                # to handle that am replacing with NV and am not inserting if it comes very first.
                td.text.replace('', 'NV')
                #print(td.text)
                if ((td.text.replace('','NV') != 'NV') or i>1 ):   #

                    rec_data[x].append(td.text.replace('\n', '').strip(' ').replace('N/A',''))

            if len(rec_data[x]) > 2:
                rec_data[x].append(url)
                recommandation.append(rec_data[x])


            x += 1

    return recommandation


def trendlyne(recommandation):

    insert_data = ''
    print('stockname,buy/Hold/sell,type_of_call,cmp,tgtprice,recommdate,tgtdate,recom by,recommsite')
    for record in recommandation:
        insert_data+=str((record[1],record[7],'Delivery',record[3],record[4],record[0],'1970-01-01',record[2].replace('\xa0','').replace('  ',''),'Trendlyne'))+',\n'
    print(insert_data.rstrip(',\n'))

def religare(recommandation):
    insert_data = ''
    print('script_code,script_name,buy/Hold/sell,type_of_call,cmp,tgtprice,recommdate,tgtdate,recom by,recommsite')
    for record in recommandation:
        insert_data += str((record[0][:record[0].find('.')+1],'To be fetch',record[0][record[0].find('-')+2:], record[2],
                            record[3][:record[3].find('.')+3], record[0][record[0].find('.')+2:record[0].find('|')-1],
                            '1970-01-01','Religare', 'Religare')) + ',\n'
    print(insert_data.rstrip(',\n'))

def ndtv(recommandation):

    #for tr in beauty_func(url).find_all('label',attrs={'id':'nseCode'}):
        #script_code=tr.text

    insert_data = ''
    print('script_code,script_name,buy/Hold/sell,type_of_call,cmp,tgtprice,recommdate,tgtdate,recom by,recommsite')
    for record in recommandation:
        script_name=url[url.find('stock/')+6:url.find('_')].replace('-',' ').upper()
        script_code=url[url.find('_')+1:url.find('/research')].upper()
        insert_data+=str((script_code,script_name,record[2],record[6][:record[6].find(' ')],record[3],record[4],
                          record[1],record[6][-10:],record[0],'Ndtv'))+',\n'
    print(insert_data.rstrip(',\n'))

def stocklinedirect(recommandation):

    for tr in beauty_func(url).find_all('h2'):  # 'tr'   and 'td' to be call from property file
        if tr.text.find('Stock Tips for ') >= 0:
            script_name=tr.text.replace('Stock Tips for ', '').strip('. ')

    for tr in beauty_func(url).find_all('tr'):
        for b in tr.find_all('b'): # 'tr'   and 'td' to be call from property file
            if b.text.find('trend')>=0:
                trend=b.text

    insert_data = ''
    df = pd.DataFrame(recommandation)
    # reassigning DataFrame only the first/second element contains 'Buy Above/Sell Below' and fetching first 6 Col's
    df = df[(df[0] == 'Buy Above') | (df[0] == 'Sell Below')].iloc[:, 0:6]
    #   Converting Df data in to array by mentioning all the Col names ( it converts Pandas DataFrame to list
    recommandation=df[[0,1,2,3,4,5]].as_matrix()
    print('stock_code,stockname,buy/Hold/sell,type_of_call,cmp,tgtprice,recommdate,tgtdate,recom by,recommsite')
    for record in recommandation:
        # Script Name Picking from the URL which we are passing by finding the position B/w stock-tips & html
        script_code=record[-1][record[-1].find('/stock-tips-') + 12:record[-1].find('.html')]

        insert_data+=str((script_code,script_name,record[0],trend,record[1],record[3]+'/'+record[4],
                          'To be Fetch','Stockline-Direct','Stockline-Direct'))+',\n'
    print(insert_data.rstrip(',\n'))


for url in url:
    # Calling Func "get_data" to bring all the recommandation without cleansing data
    get_data(url)

    if url.find('trendlyne')>0:
        print('trendlyne')
        trendlyne(recommandation)

    elif url.find('religareonline') > 0:
        print('religare')
        religare(recommandation)

    elif url.find('profit.ndtv.com')>0:
        print('ndtv')
        ndtv(recommandation)

    elif url.find('stocklinedirect')>0:
        print('stocklinedirect')
        stocklinedirect(recommandation)

    else:
        print('URL has no Such Definitions to Crawl, pls write New Function to fetch ')



# Religare: findout type of call buy/hold,type of call, ;in Ndtv type of call exception handling

#stocksymbol,stockname,buy/Hold/sell,cmp,tgtprice,recommdate,tgtdate,,recom by,recommsite,