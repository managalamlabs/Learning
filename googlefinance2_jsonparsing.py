
# coding: utf-8

# In[96]:

import urllib
import urllib2
import httplib
import sys
import re
from newspaper import Article
from bs4 import BeautifulSoup
import sys
import json
import threading

##uri='http://finance.google.com/finance/historical?q=NSE:GMRINFRA&startdate=Oct+24%2C+2015&enddate=Oct+23%2C+2017'

##uri_2='http://finance.google.com/finance/historical?q=NSE:GMRINFRA&startdate=Oct+24%2C+2015&enddate=jul+23%2C+2016&num=200'

###uri_3='http://finance.google.com/finance/historical?q=NSE:GMRINFRA&startdate=Oct+24%2C+2015&enddate=jul+23%2C+2016&num=200'

#print uri
def get_page_spoof(s):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = urllib2.Request(s, headers=hdr)
    expet = 0
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
        expet = 1
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
        expet = 1
    except httplib.HTTPException, e:
        print 'HTTPException'
        expet = 1
    except Exception:
        # import traceback
        print 'generic exception: '
        expet = 1
    if expet == 0:
        content = page.read()
        page.close()
        return content
    else:
        return 'no content for link ' + s


# In[69]:



def parsedata(data):
    soup = BeautifulSoup(data,'html.parser')
    #print 'test'
    tables=soup.find_all('table',class_='gf-table historical_price')
    if(len(tables) !=0):
        d=tables[0].text.encode('UTF-8').strip()
        datalines=d.splitlines()
        alllines = '|'.join(datalines).split('||')
        return alllines[1:]

def createuri(stock,start_date,end_date,numpage=200):
    #url='http://finance.google.com/finance/historical?q=NSE:GMRINFRA&startdate=Oct+24%2C+2015&enddate=jul+23%2C+2016&num=200'
    startdate=datetime.strptime(str(start_date), "%Y-%m-%d")
    enddate=datetime.strptime(str(end_date), "%Y-%m-%d")
    uri_head='http://finance.google.com/finance/historical?q='+stock
    uri_middle_1='&startdate='+datetime.strftime(startdate, "%b")+'+'+datetime.strftime(startdate, "%d")+'%2C+'+datetime.strftime(startdate, "%Y")
    uri_middle_2='&enddate='+datetime.strftime(enddate, "%b")+'+'+datetime.strftime(enddate, "%d")+'%2C+'+datetime.strftime(enddate, "%Y")
    uri_tail='&num='+str(numpage)
    return uri_head+uri_middle_1+uri_middle_2+uri_tail
    
        
    
    


# In[70]:

from datetime import datetime, timedelta
def geturlsforgoogle(stock_name,start_date,end_date):
    sd=datetime.strptime(str(start_date), "%Y/%m/%d")
    print str(sd).split(' ')[0]
    ed=datetime.strptime(str(end_date), "%Y/%m/%d")
    print str(ed).split(' ')[0]
    urilist=[]
    print (ed-sd).days
    if((ed-sd).days > 180):
        loads_r=(ed-sd).days%180
        loads=(ed-sd).days/180
        for i in range(0,loads):
            #print (sd+timedelta(days=179)).date
            uri_intr = createuri(stock_name,str(sd).split(' ')[0],str(sd+timedelta(days=179)).split(' ')[0],180)
            urilist.append(uri_intr)
            sd=sd+timedelta(days=180)
        urilist.append(createuri(stock_name,str(sd).split(' ')[0],str(sd+timedelta(days=loads_r)).split(' ')[0],180))
    else:
        urilist.append(createuri(stock_name,str(sd).split(' ')[0],str(ed).split(' ')[0],180))
    return urilist
        
            
def getstockdatafromgoogle(stocksymbol,startdate,enddate):
    print stocksymbol
    urllist=geturlsforgoogle(stocksymbol,startdate,enddate)
    stocklist=[]
    for url in urllist:
        data=get_page_spoof(url)
        scripslist=parsedata(data)
        if scripslist is None:
            lenstlist=0
        else:
            lenstlist=len(scripslist)
            stocklist=stocklist+scripslist
        print 'working on url'+url+" number of records :"+str(lenstlist)
    return stocklist
    
            
        
    
    


# In[71]:

##print len(getstockdatafromgoogle('NSE:8KMILES','2009/03/30','2017/10/23'))


# In[74]:

def writedataintofiles(scripinputpath,scripoutputpath=''):
    fr=open(scripinputpath,'r')
    lines=fr.readlines()
    for line in lines[1:]:
        scrip=line.split(',')[2]
        print scrip
        stocklist=getstockdatafromgoogle('NSE:'+scrip,'2004/03/30','2017/10/23')
        if stocklist is not None:
            updated_stocklist=['NSE:'+scrip+'|'+record for record in stocklist]
            writefiles(scripoutputpath+'\\'+scrip,updated_stocklist)
        
def writefiles(writepath,stocklist):
    fw=open(writepath,'w')
    fw.write("\n".join(stocklist))
    fw.close()
    print 'done writing file'+writepath
    
    



# In[77]:

##writedataintofiles('C:\Users\Dell\Desktop\managalamproject\\500scriplist.csv','C:\Users\Dell\Desktop\managalamproject\datalakestocksupdated')
print 'done'


# In[120]:

import mysql.connector
import os
def writeintomysql(stocklist,host_name='localhost',tablename='historicalstockprices',database_name='stockdata',user_name='root',password_v='toor'):
    cnx = mysql.connector.connect(user=user_name, password=password_v,host=host_name,database=database_name)
    print 'connection created'
    cursor = cnx.cursor()
    for stck in stocklist:
        print 'done'
        

def writefiles(stocklist,writepath='',db=False):
    if db==False:
        fw=open(writepath,'w')
        fw.write("\n".join(stocklist))
        fw.close()
        print 'done writing file'+writepath
    else:
        #writeintomysql(stocklist)
        print 'write to sql'

from dateutil.parser import parse

def changeformat(datev,requiredformat='%Y-%m-%d'):
    #dt = parse('Sep 20, 2005')
    dt = parse(datev)
    #return (dt.strftime('%d/%m/%Y'))
    # 15/02/2010
    return (dt.strftime(requiredformat))

#print get_page_spoof('https://www.motilaloswal.com/markets/stock-market-live/StockSplits.aspx')


def parsejson(path='C:\\Users\\Dell\\Desktop\\managalamproject\\repositories\\moneycontrolScrapping\\test.json',decode='UTF-8'):
    import json
    data=json.loads(open(path).read())
    return data

json = parsejson('C:\\Users\\Dell\\Desktop\\managalamproject\\repositories\\moneycontrolScrapping\\test.json')


origin_page=page=get_page_spoof('http://profit.ndtv.com/market/market-dashboard/research-reports')


print url


def parsedata(data):
    soup = BeautifulSoup(data,'html.parser')
    #print 'test'
    tables=soup.find_all('table',class_='gf-table historical_price')
    if(len(tables) !=0):
        d=tables[0].text.encode('UTF-8').strip()
        datalines=d.splitlines()
        alllines = '|'.join(datalines).split('||')
        return alllines[1:]
iterations=json['iteration']


def parsedata(data,properties):
    classname=properties[0]
    whichtable=properties[1]
    soup = BeautifulSoup(data,'html.parser')
    #print 'test'
    print data[0:20]
    tables=soup.find_all('table',class_=classname)
    #print tables
    if(len(tables) !=0):
        d=tables[whichtable].text.encode('UTF-8').strip()
        datalines=d.splitlines()
        alllines = '|'.join(datalines).split('||')
        return alllines[1:]

iterations=json['iteration']




for it in iterations:
    if it['table'] == 1:
        data_p=parsedata(origin_page,[it['classname'],it['numberstocrawl']])
        print data_p
        

soup = BeautifulSoup(origin_page,'html.parser')  
tables=soup.find_all('table')
print len(tables)




#page=get_page_spoof(url)


# In[107]:

dir(tables)


# In[116]:

#d=tables[3].text.encode('UTF-8').strip()
print 'test'
#print d
dir(tables[3])

for table in tables:
    print table.text



# In[ ]:



