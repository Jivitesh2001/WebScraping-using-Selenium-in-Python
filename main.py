from selenium import webdriver
chrome_driver_path = r"C:\Development\chromedriver_win32\chromedriver"
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service = service)

driver.get("https://moneysmart.gov.au/fake-regulators-and-exchanges")

curs = driver.find_elements(By.XPATH,"//div[@id='content']/div[@class='wrapper']/div[@class='content-global']/div[@class='main-column']/ul/li/a")

links=[]

for i in curs:
    x= i.get_attribute('href')
    k= i.get_attribute('innerHTML')
    links.append([x,k])
size = len(links)
for i in range(size):
    if '(' in str(links[i][1]):
        index1 = str(links[i][1]).index('(')
        index2 = str(links[i][1]).index(')')
        links[i].append(str(links[i][1])[index1:index2+1])
        links[i][1]=str(links[i][1]).replace(links[i][2],'')
    else:
        links[i].append(' ')

#print(links[0])
#driver.get(str(links[0][0]))
#curs2 = driver.find_element(By.XPATH,"//div[@class='row']/div[@class='cell']/p")
#print(curs2.get_attribute('innerHTML'))

for i in range(size):
    temp=''
    if links[i][0] != None:
        driver.get((links[i][0]))
        curs2 = driver.find_elements(By.XPATH,"//div[@class='row']/div[@class='cell']/p")
        no_of_elements = len(curs2)
       
        for c in range(no_of_elements):
            text=curs2[c].get_attribute('innerHTML')
            
            if '<br>' in text:
                text=text.replace('<br>',' ')
            if '<span class=""alias"">' in text:
                text=text.replace('<span class=""alias"">',' ')
            if '<span class=""account"">' in text:
                text=text.replace('<span class=""account"">',' ')
            if '</span>' in text:
                text=text.replace('</span>',' ')
            temp +=text
    if temp!='':
        links[i].append(temp)
    else:
        links[i].append(' ')
print(links)
print(len(links))

data=[]

for i in range(size):
    entityid = str(links[i][1]).replace(' ',"_")
    name=links[i][1]
    alias=links[i][2]
    notes = links[i][3]
    data.append([entityid,name,alias,notes])

df = pd.DataFrame(data,columns=['Entity_ID','Name','Alias','Notes'])

print(df)

df.to_csv('data.csv',sep=',',encoding='utf-8')


driver.quit()