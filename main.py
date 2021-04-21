from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import xlrd
import time
import os

path="chromedriver.exe"
site="https://www.formula1.com/en/results.html/2021/drivers.html"
head=[]

def buttonClick(path):
    button = WebDriverWait(driver,30).until(expected_conditions.presence_of_element_located((By.XPATH,path)))
    button.click()

def findElement(path):
    element = WebDriverWait(driver,30).until(expected_conditions.presence_of_element_located((By.XPATH,path)))
    return element

def findChildren(ref, tag):
    element = WebDriverWait(ref,30).until(expected_conditions.presence_of_element_located((By.TAG_NAME,tag)))
    return element

def findChildrens(ref, tag):
    elements = WebDriverWait(ref,30).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME,tag)))
    return elements

def findChildrensXpath(ref, path):
    elements = WebDriverWait(ref,30).until(expected_conditions.presence_of_all_elements_located((By.XPATH,path)))
    return elements

driverOptions = webdriver.ChromeOptions()
driverOptions.add_argument('headless')
driver = webdriver.Chrome(options=driverOptions)
driver.get(site)

#accept cookies
buttonClick('/html/body/div[5]/div/div/div[2]/div[3]/div[2]/button[2]')
print("Cookies Accepted")

#search for the right table
table = findElement('/html/body/div[2]/main/article/div/div[2]/div[2]/div[2]/div/table')
print("Find Table")

#get all header information about columns
tableHeader = findChildren(table,'thead')
lines = findChildrens(findChildren(tableHeader,'tr'),'th')

for th in lines:
    if(th.text!=''):
        head.append(th.text)

print(head)

#get the data of table body
tableBody = findChildren(table, 'tbody')
lines = findChildrens(tableBody,'tr')
drivers=[]

for tr in lines:
    line=[]
    columns = findChildrens(tr, 'td')
    for col in columns:
        if(col.text!=''):
            if(col.get_attribute('class')==""):
                colElements = findChildrensXpath(col,'.//*')
                auxString = ''
                driverLastName = ''
                motor = False
                for ce in colElements:
                    if(ce.tag_name == 'a'):
                        auxString = ce.get_attribute('textContent')
                        motor=True
                    if(ce.get_attribute('class')=='hide-for-tablet'):
                        auxString = ce.get_attribute('textContent')
                        motor = False
                    if(ce.get_attribute('class')=='hide-for-mobile'):
                        driverLastName = ce.get_attribute('textContent')
                        motor = False
                if(motor):
                    name = auxString
                else:
                    name = (auxString+" "+driverLastName)
                line.append(name)
            else:
                line.append(col.text)
    drivers.append(line)

print(drivers)
driver.quit()