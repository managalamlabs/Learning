
# coding: utf-8

# In[ ]:

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



def get_page_spoof(s):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = urllib2.Request(s, headers=hdr)
    expet = 0
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
        print 'the url for HTTPERROR is: '+s
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



def withSoupScrap_businessline(url, metadata):
    page = get_page_spoof(url)
    soup = BeautifulSoup(page, 'html.parser')
    # pull published date and publisher name
    publisher_name = 'no_name'
    published_Date = "no_date"
    title = soup.find("meta", property="article:author")
    if title is not None:
        publisher_name = title["content"].encode('UTF-8').strip()
    publishedDate = soup.find("meta", property="article:published_time")
    
    if publishedDate is not None:
        published_Date = publishedDate["content"].encode('UTF-8').strip()
    # url = soup.find("meta",  property="og:url")
    # Take out the <div> of name and get its value
    content_box = soup.findAll('p', attrs={'class': 'body'})
    # print name_box
    if(content_box is not None):
        try:
            unicoded_list = []  
             
            [unicoded_list.append(content.text.encode('UTF-8').strip()) for content in content_box]
            
            description = ' '.join(unicoded_list)
            
            return published_Date + "|" + publisher_name + "|" + description
        except UnicodeEncodeError, e:
            print "the unicode error is" + str(e.reason)
            return None
        
def get_all_links(url):
    url_list = []
    page = get_page_spoof(url)
    soup = BeautifulSoup(page, 'html.parser')
    all_hrefs = soup.find_all('a', href=True)
    [url_list.append(urltag['href'].encode('UTF-8').strip()) for urltag in all_hrefs]
    return url_list
        
    
    

def businessLine_urls(url, metadata):
    filt = metadata[0]
    links = get_all_links(url)
    data_list = []
    # print links
    for lin in links:
        # "todays-pick"
        if(lin.find(filt) >= 0):
            data_list.append(lin.encode('UTF-8').strip())
    data_list = list(set(data_list))
    return data_list

def businessMain(url, path):
    allurls = businessLine_urls("http://www.thehindubusinessline.com/markets/todays-pick/", ['todays-pick'])
    f = open(path, 'w')
    for url in allurls:
        f.write(withSoupScrap_businessline(url, ''))
        f.write('\n')
    f.close()
    print 'processDone'
        
def moneycontrol(url_intial, path, metadata):
    pagerange = metadata[0]
    f = open(path + "/" + str(pagerange[0]) + "-" + str(pagerange[1]) + "-moneycontrol.txt", 'w')
    url_list = generateHistoryLinksMoneycontrol('http://www.moneycontrol.com/news/business/stocks-business/page-', pagerange)
    for url in url_list:
        match_list = moneycontrol_urls(url, ['buy-', 'sell-', 'hold-'])
        for matchurl in match_list:
            d = extractdataMoneyControl(matchurl, [])
            print d
            f.write(d)
            f.write('\n')
    f.close()
    print 'prosess done'
            
    
def moneycontrol_urls(url, metadata):
    
    links = get_all_links(url)
    matched_links = []
    for link in links:
        # matching = [s for s in metadata if link.find(s)>0]
        if any(link.find(s) > 0 for s in metadata):
            # print link
            matched_links.append(link)
    matched_links = list(set(matched_links))
    return matched_links


    
    

def generateHistoryLinksMoneycontrol(urlpattern, pagerange):
    
    # pattern = 'http://www.moneycontrol.com/news/business/stocks-business/page-2'
    # pattern = 'http://www.moneycontrol.com/news/business/stocks-business/page-'
    historyUrls = []
    startpage = pagerange[0]
    endpage = pagerange[1]
    for i in range(startpage, endpage + 1):
        historyUrls.append(urlpattern + str(i))
    historyUrls = list(set(historyUrls))
    return historyUrls;

def extractdataMoneyControl(url, metadata):
    # print url
    page = get_page_spoof(url)
    soup = BeautifulSoup(page, 'html.parser')
    publisher_name = 'no_name'
    published_date = 'no_date'
    description = 'no_description'
    script_content = soup.findAll('script', type='application/ld+json')
    if script_content is not None:
        if(len(script_content) == 2):
            # print script_content[1].text
            contentJson_m = json.loads(script_content[1].text.encode('UTF-8').strip(), strict=False)
            contentJson=contentJson_m[0]
            published_date = contentJson['datePublished'].encode('UTF-8').strip()
            publisher_name = contentJson['author'].encode('UTF-8').strip()        
            description = contentJson['description'].encode('UTF-8').strip()
        
    return publisher_name.replace('\n', ' ').replace('\r', '') + "|" + published_date.replace('\n', ' ').replace('\r', '') + "|" + description.replace('\n', ' ').replace('\r', '')
        
def test():
    businessMain('', 'C:\\Users\\h139584\\Desktop\\my learnings\\stockAnalzer\\businessline_news_march_22st.txt')
    # moneycontrol('http://www.moneycontrol.com/news/business/stocks-business/page-355', '')
    # print generateHistoryLinksMoneycontrol('http://www.moneycontrol.com/news/business/stocks-business/page-',355)
    print extractdataMoneyControl('http://www.moneycontrol.com/news/business/stocks-business/sell-usdinr-around-6690-target6650-way2wealth-958932.html', [])    

# def parallelizeMoneycontrol(baseurl,basepath,metada):
    

def parallelMoneycontrol(url_intial, path, metadata, noOfBatches):
    thread_list = []
    diff = (metadata[1] - metadata[0]) / noOfBatches
    intial = metadata[0];
    last = metadata[1]
    print 'the difference is '+str(diff)
    for batch in range(0, noOfBatches):
        t = threading.Thread(target=moneycontrol, args=('', path, [[intial, intial + diff - 1]],))
        intial = intial + diff
        thread_list.append(t)
    t = threading.Thread(target=moneycontrol, args=('', path, [[intial, last]],))
    thread_list.append(t)
    
    for thread in thread_list:
        thread.start()
        
    for thread in thread_list:
        thread.join()
        
    print "Done"
    
      

if __name__ == "__main__":
    # script from_page to_page number_of_batches
	###how to run:note run in powershell######
	####python datascrapper_mc.py pathtostoreoutputfiles from_page to_page numberofbatches
	####python .\datascrapper_mc.py C:\Users\Dell\Desktop\managalamproject\datlakemoneycontrol 10 20 2
    print 'the inputs path from_page,to_page,number_of_batches is: ' + str(sys.argv[1]) + "," + str(sys.argv[2]) + "," + str(sys.argv[3]) + "," + str(sys.argv[4])
    # parallelMoneycontrol('', 'C:\\Users\\h139584\\Desktop\\my learnings\\stockAnalzer\\scrappedData\\moneycontrol\\', [int(sys.argv[1]), int(sys.argv[2])], int(sys.argv[3]))
    parallelMoneycontrol('', str(sys.argv[1]), [int(sys.argv[2]), int(sys.argv[3])], int(sys.argv[4]))

