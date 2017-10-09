
# coding: utf-8

# In[1]:


import urllib
import urllib2
import time
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
def getting_links(g,s):
    pear=get_page_spoof(s)
    #getting page content to pear string
    f=g.split(',')
    j=pear.split('href')
    #dilimited by href entire content taken into list
    print len(j)
    #print j[1]
    #if str(j[1]).find('canonical')>0:
        #print str(j[1])[0:8]
        #print j[1][2:j[1][2:].find('"')+2]
    for i in j:
    #ittirating list
        #print i
        for m in f:
            print m
            if str(i).find(str(m))>0:
        #verifying if string exist in link and extracting link out of it
                return i[2:i[2:].find('"')+2]

            #else:
                #print j
while True:
    text_file = open("D:\\Output\\Output.txt", "a")
    text_file.write(getting_links('Honeypreet,China','http://economictimes.indiatimes.com/')+'\n')
    text_file.close()
    print 'check the data'
    time.sleep(60)
#print get_page_spoof('http://economictimes.indiatimes.com/')

