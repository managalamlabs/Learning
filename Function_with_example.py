
# coding: utf-8

# In[3]:


import urllib
import urllib2
import time
import httplib
import mysql.connector
import os
import json
from bs4 import BeautifulSoup
import pandas
import datetime
url='http://www.stocklinedirect.com/stock-tips.html'
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
def get_required(strg,jason):
    # function that takes Page source and One of the jason object in for loop
    deff=str(strg)# converting it to string if in case if its different object
    soup=BeautifulSoup(deff,'html.parser')#page source is passed to generate beautiful soup object
    #json file parameters are stored in variables
    req=[]
    name=jason.get("object")
    vlue=jason.get("value")
    get=jason.get("get")
    
    if name!='' and len(vlue)==0 and get=='':#if name is passed and other objects are not passed through json
        strg=''#page source passed erlier is removed
        beautobj=soup.find_all(name)
        #below for loop used create get the requested page source as string or store it to variable that has been passed intially
        for beautobjs in beautobj:
            strg+=str(beautobjs)+'\n'+'|'+'\n'#\n is used to move he next loop object to next line with pipe delimiter 
    elif name!='' and len(vlue)>0 and get=='':#if name, vlue is passed through json and other objects are not passed
        strg=''#page source passed erlier is removed
        dics=dict()#dictonary object to to be passed to pass web object value
        dics[values[0]]=values[1]#cretating key value pair of dictionary 
        beautobj=soup.find_all(name,dics)
        for beautobjs in beautobj:
            strg+=str(beautobjs)+'\n'+'|'+'\n'#\n is used to move he next loop object to next line with pipe delimiter 
    elif name!='' and len(vlue)>0 and get!='':#if name, vlue is passed through json along with get paramter,should be used in last run of the looop
        strg=''#page source passed erlier is removed
        dics=dict()#dictonary object to to be passed to pass web object value
        dics[values[0]]=values[1]#cretating key value pair of dictionary 
        beautobj=soup.find_all(name,dics)#it fetching page source based on object and their value
        #below it fetches requested get item passed from json
        if len(beautobj)>0:
            for beaut in beautobj:
                se=beaut.get(get)
                sep=se.decode('utf-8')
                req.append(se)#list is created with required parameter passed from get object of json
        else:
            print 'there are no desired object based on parameters passed from json file'
    elif name!='' and len(vlue)==0 and get!='':#if name with get paramter,should be used in last run of the looop
        beautobj=soup.find_all(name)
        if len(beautobj)>0:
            for beaut in beautobj:
                se=beaut.get(get)
                sep=se.decode('utf-8')
                req.append(sep)#list is created with required parameter passed from get object of json
        else:
            print 'There are no results for you desired get value'
    else:
        print 'your json file is do not have proper data'
    
    if len(req)>0:#returns if there is no get parameter is passed from json 
        return req
    else:#returns list if there is get parameter is passed from json 
        #print 'Your file do not have proper get properties'
        return strg


def scrap_urls(url,file_name):
    #used to pass url and json file
    page_source=get_page_spoof(url)
    #json file is read and json in children are read and get_required function executed in for loop 
    data=json.loads(open(file_name).read())
    jdata=data["children"]
    for jdatas in jdata:
        page_source=get_required(page_source,jdatas)
    return page_source

objects=scrap_urls('http://www.stocklinedirect.com/stock-tips.html','D:\\test1.json')
print objects
 

