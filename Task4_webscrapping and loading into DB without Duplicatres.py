
import requests
import re
import pymysql as db
import validators as valid
import datetime as dt


conn=db.connect("localhost","root","","test")
cursor=conn.cursor()
cursor.execute("select * from web_scrap;")
data=cursor.fetchall()
#print(len(data))
start_str='href="'
end_str='"'

def get_page(base_url):
    global response,r
    r = requests.head(base_url)
    source_response=requests.get(base_url).text.encode('utf8')
    response = ''
    for i in range(len(source_response)):
        response += chr(source_response[i])

def get_url():
    global list_url
    list_url=[]
    get_page(base_url)
    list_url_in_base_url = response.split(start_str)

    for i in list_url_in_base_url:
        list_url_final = i.split(end_str)
        if list_url_final[0].startswith('/') :
            list_url.append(base_url+list_url_final[0])
def get_url_info():
    get_url()
    unique_url=list(set(list_url))
    for i in unique_url:
        get_page(i) #'https://economictimes.indiatimes.com/indices/sensex_30_companies')
        if response.find('name="keyword" content="')>0:
            count=0
            for db_url in range (len(data)):

                if i==data[db_url][0]:
                    count+=1
                    print('already exists')

            if count==0:
                print("URL Inserted into web_scrap table, URL: "+i)
                keywords=response.split('name="keyword" content="')[1].split('"')[0].replace(',','-')
                last_modified_date=response.split('Last-Modified" content="')[1].split('"')[0]
                cur_date=dt.datetime.today()
                cursor.execute("INSERT INTO web_scrap values (%s,%s,%s,%s)", (i,last_modified_date,keywords,cur_date))
                cursor.execute("commit")


base_url = 'http://economictimes.indiatimes.com'
get_url_info()

conn.close()




