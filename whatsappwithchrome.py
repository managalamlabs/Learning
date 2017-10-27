
# coding: utf-8

# In[ ]:

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
 
# Replace below path with the absolute path
# to chromedriver in your computer
driver = webdriver.Chrome('C:\Users\Dell\Downloads\chromedriver_win32\chromedriver.exe')
 
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)
 
# Replace 'Friend's Name' with the name of your friend 
# or the name of a group 
#target = '"Friend\'s Name"'

target = 'Mangalam gang'
 
# Replace the below string with your own message
stringmessage = "good night"
 
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located((
    By.XPATH, x_arg)))
group_title.click()
inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located((
    By.XPATH, inp_xpath)))

print 'messages sending'

for i in range(0,3):
    print 'start'
    input_box.send_keys(stringmessage + Keys.ENTER)
    print stringmessage
    time.sleep(1)


# In[ ]:

print 'omkar'


# In[ ]:

print 'omkar'


# In[ ]:



