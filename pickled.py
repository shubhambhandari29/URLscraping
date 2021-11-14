#!/usr/bin/env python
# coding: utf-8

# importing libraries 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pickle
import pdfkit



#path = r'C:\Users\1709216\Downloads\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

s=Service('C:/Program Files/webdriver/chromedriver')
browser = webdriver.Chrome(service=s,options=options)
url= 'https://www.smilefoundationindia.org/'
browser.get(url)


# ## getting the link


content = browser.page_source
soup = BeautifulSoup(content,"html.parser")

menu = soup.find('ul', {'class': 'nav navbar-nav'})
menu = menu.findChildren(recursive=False)

print(len(menu))


menuLinks = []
for menuID in range(len(menu)):
    
    links = {
        'id' : menuID,
        'cat': menu[menuID].find('a').get_text().strip(),
        'url' :  menu[menuID].find('a', href = True)['href'],  
    }
    menuLinks.append(links)
    


# ### scraping the submenus and getting their URLs 

llist = []
urlList = []

browser.get("https://www.smilefoundationindia.org/#")
content = browser.page_source
soup = BeautifulSoup(content,"html.parser")
li = soup.find('ul', {'class': 'nav navbar-nav'})
children = li.find_all('a')
for childID in range(len(children)):
            links = {
                 'id' : childID,
                 'cat': children[childID].get_text().strip(),
                 'url' :children[childID]['href'],  
            }
            if(links["url"]!="#"):
                urlList.append(links["url"])
                llist.append(links)

# ###  converting python objects into a character stream using pickle


pickle.dump(llist, open('links.pkl', 'wb'))





