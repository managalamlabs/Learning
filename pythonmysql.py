
# coding: utf-8

# In[26]:

import mysql.connector
import os

#local host can be replaced with 127.0.0.1 loopback address
cnx = mysql.connector.connect(user='root', password='toor',
                              host='localhost',
                              database='webscrapping')
print 'connection created'
cursor = cnx.cursor()

test_q = ("INSERT INTO test "
               "(keywordname, url_string) "
               "VALUES (%s, %s)")
test_d = ('github123', 'www.github123.com')

cursor.execute(test_q, test_d)
cnx.commit()
cursor.close()
cnx.close()
print 'my windows command'
#os.execute('dir')
print 'connection closed'
str='mysql -uroot -ptoor webscrapping  -e /"INSERT INTO test (keywordname, url_string) VALUES (/"/"/"googlelly123/"/"/", /"/"/"www.googlelly12345.com/"/"/");/"'
print str
try:
    os.system(str)
except Error:
    print 'error'
#os.system("mysql -uroot -ptoor webscrapping  -e "INSERT INTO test (keywordname, url_string) VALUES ("""googlelly1234""", """www.googlelly1234.com""");"")


# In[ ]:



