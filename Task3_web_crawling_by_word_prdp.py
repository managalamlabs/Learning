
import requests
import re

base_url='http://economictimes.indiatimes.com/'
source_response=requests.get(base_url).text.encode('utf8')
response=''
for i in range(len(source_response)):
    response+=chr(source_response[i])

#print(response)
start_str='href="'
end_str='"'

list_url_in_base_url=response.split(start_str)    #list_url_in_base_url=re.search(r'href="(.*)"', response).group(1).split(start_str)

list_url=[]                         #open('economictimes_href_url.txt','w')
for i in list_url_in_base_url:
    list_url_final=i.split(end_str)
    list_url.append(list_url_final[0])                          # list_url.write(list_url_final[0]+'\n')

search_list_word=open('word_to_find_in_economic_times.txt','r')
search_word=search_list_word.read()
search_list_word.close()

found_url=open('found_urls.txt','w')
for i in list_url:
    for j in search_word.split(','):
        if i.lower().find(j.lower())>0:
            found_url.write(i+'\n')

found_url.close()
#list_url.close()



