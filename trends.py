from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from tkinter import *
import threading

def orderdatabasebylastscan():
    data = pd.read_csv('Database\dropshippername.csv')
    list1 = data.sort_values(by="Last Scan", na_position='first')
    list1.to_csv('Database\dropshippername.csv', index=False)
    ordereddata = pd.read_csv('Database\dropshippername.csv')
    return ordereddata

def convertstringdatetodate(stringdate):
    try:
        date=datetime.datetime.strptime(stringdate, '%Y-%m-%d %H:%M:%S.%f')
        return date
    except:
        return None

def savedropitems(new_data):
    df=pd.DataFrame([new_data])
    with open('Database\dropitems.csv', 'a') as temp:
        df.to_csv(temp,header=False, index=False)
        temp.close()
    data = pd.read_csv('Database\dropitems.csv')
    data.drop_duplicates(subset="Ebay Url", inplace=True)
    data.to_csv('Database\dropitems.csv' , index=False)

def savedropshippers(new_data):
    df=pd.DataFrame(new_data)
    with open('Database\dropshippername.csv', 'a') as temp:
        df.to_csv(temp,header=False, index=False)
        temp.close()

def readalldata():
    data = pd.read_csv('Database\dropshippername.csv')
    return data

def readdatadropshippers():
    data = pd.read_csv('Database\dropshippername.csv')
    return data['Names'].values


def ziklogin():
    try:
        packed_extension_path = 'ZIK-booster_v0.3.84.crx'
        options = Options()
        options.add_extension(packed_extension_path)
        chrome = webdriver.Chrome(executable_path='chromedriver.exe',options=options)
        chrome.get("https://zikanalytics.com/Search/Index")
        chrome.find_element_by_id("Username").send_keys("Ourielrybski3@gmail.com")
        chrome.find_element_by_id("Password").send_keys("Xpehoakthch1")
        chrome.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/form/div[3]/button").click()
        time.sleep(2)
        return chrome
    except Exception as err:
        print (err)
        temp=ziklogin()
        return temp

def randomamazon():
    try:
        listproduct=[]
        category=["https://www.amazon.com/Best-Sellers-Health-Personal-Care/zgbs/hpc",
                  "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden",
                  "https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products",
                  "https://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty",
                  "https://www.amazon.com/Best-Sellers-Garden-Outdoor/zgbs/lawn-garden",
                  "https://www.amazon.com/Best-Sellers-Luggage-Travel-Gear/zgbs/fashion/9479199011",
                  "https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products",
                  "https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies",
                  "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods",
                  "https://www.amazon.com/Best-Sellers-Home-Improvement/zgbs/hi",
                  "https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games"]
        randomcategory=category[random.randrange(0,len(category))]
        page=requests.get(randomcategory).content
        soup = BeautifulSoup(page, "html.parser")
        text = str(soup.find(id="zg-ordered-list"))
        soup = BeautifulSoup(text, "html.parser")
        itemtext = soup.findAll('div',{"class":"p13n-sc-truncate p13n-sc-line-clamp-2"})
        randomitem=itemtext[random.randrange(0,len(itemtext))].string
        randomitem=' '.join(randomitem.split(' ')[12:21]).replace(",","")
        return (randomitem)
    except Exception as err:
        print(err)
        temp=randomamazon()
        return temp

def searchzikwithamazonitem(chrome):
    try:
        minfeedback=0
        maxfeedback=10000

        chrome.get("https://zikanalytics.com/Search/Index")
        randomitem=randomamazon()
        try:
            element = WebDriverWait(chrome, 15).until(
                EC.presence_of_element_located((By.ID, 'srcKeyword'))
            )
        finally:
            chrome.find_element_by_id("srcKeyword").send_keys(randomitem)

        chrome.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div/div[2]/div/div[2]/div/input[2]").send_keys("{}".format(maxfeedback))
        chrome.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div/div[2]/div/div[2]/div/input[1]").send_keys("{}".format(minfeedback))
        chrome.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div[1]/button").click()
        try:
            element = WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="productTBody"]/tr[2]/td[3]/a[2]'))
            )
        finally:
            elementhover = chrome.find_element_by_xpath('//*[@id="productTBody"]/tr[2]/td[3]/a[2]')
            hover = ActionChains(chrome).move_to_element(elementhover)
            hover.perform()
        time.sleep(2)
        chrome.find_element_by_xpath('//*[@id="tableProducts"]/thead/tr/th[4]/label/span').click()
        chrome.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div/div[2]/div/div[5]/div/button").click()
        try:
            element = WebDriverWait(chrome, 40).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'zconm zika-80'))
            )
        except Exception as err:
            print(err)
            pass
        finally:
            response = chrome.page_source

        soup = BeautifulSoup(response, "html.parser")
        feedbacknum=[]
        allcountry = []
        allnames = []
        for country in soup.findAll('tr', {"class": "even"}):
            temp = country
            try:
                tempcountry=(str(temp).split('zconm')[1].split('>')[1].split("</")[0])
                tempname=(str(temp).split('ebay.com/usr/')[1].split('"')[0])
                tempfeedbacknum=(str(temp).split("b>")[1].split("</")[0])
                if len(str(tempname)) and len(str(tempcountry)) > 0:
                    allcountry.append(tempcountry)
                    allnames.append(tempname)
                    feedbacknum.append(tempfeedbacknum)
            except Exception as err:
                print('fail to load flag')
                pass
        for country in soup.findAll('tr', {"class": "odd"}):
            temp = country
            try:
                tempcountry = (str(temp).split('zconm')[1].split('>')[1].split("</")[0])
                tempname = (str(temp).split('ebay.com/usr/')[1].split('"')[0])
                tempfeedbacknum = (str(temp).split("b>")[1].split("</")[0])
                if len(str(tempname)) and len(str(tempcountry)) > 0:
                    allcountry.append(tempcountry)
                    allnames.append(tempname)
                    feedbacknum.append(tempfeedbacknum)
            except Exception as err:
                print('fail to load flag')
                pass
        dropshippers = readdatadropshippers()
        newdropshippers=[]
        nowtime=datetime.datetime.now()
        tempdrop=[]
        print(len(allcountry),len(allnames),len(feedbacknum))
        for x in range(0, len(allcountry)):
            if allcountry[x] == 'ISRAEL':
                if allnames[x] not in dropshippers: # and int(feedbacknum[x]) < 20000:
                    tempdrop.append(allnames[x])
            if allcountry[x] == 'GREECE':
                if allnames[x] not in dropshippers: # and int(feedbacknum[x]) < 20000:
                    tempdrop.append(allnames[x])
            if allcountry[x] == 'BULGARIA':
                if allnames[x] not in dropshippers: #and int(feedbacknum[x]) < 20000:
                    tempdrop.append(allnames[x])
            if allcountry[x] == 'UNITED STATES':
                if allnames[x] not in dropshippers: #and int(feedbacknum[x]) < 6000:
                    tempdrop.append(allnames[x])
        tempdrop = list(dict.fromkeys(tempdrop))
        for x in tempdrop:
            newdropshippers.append([x,nowtime])
        savedropshippers(newdropshippers)
        return chrome
    except Exception as err:
        print(err)
        temp=searchzikwithamazonitem(chrome)
        return temp


def searchdropshipperinzik(chrome):
    wantednumber=3
    data=orderdatabasebylastscan()
    ebaygooditems=[]
    for count in data.index:
        lastscan=convertstringdatetodate(data.at[count,'Last Scan'])
        if lastscan == None :
            chrome.get('https://zikanalytics.com/SearchCompetitor/Index')
            try:
                chrome.find_element_by_id('srcUsername').send_keys(data.at[count, 'Names'])
                chrome.find_element_by_xpath(
                    '/html/body/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/select/option[4]').click()
                chrome.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/button').click()
                time.sleep(3)
                if chrome.find_element_by_xpath(
                        '//*[@id="info"]').text != 'The seller had no sales for the selected period.' and chrome.find_element_by_xpath(
                        '//*[@id="info"]').text != 'This user is in waiting list. Please check back later for results.':
                    try:
                        element = WebDriverWait(chrome, 15).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="datatable-responsive"]/tbody/tr[1]/td[4]'))
                        )
                    finally:
                        time.sleep(2)
                        loopfor = chrome.find_element_by_xpath('//*[@id="intercomEbayCards"]/div[6]/div/div[3]').text
                        if int(loopfor) > 30:
                            loopfor = 30
                        for num in range(1, int(loopfor)):
                            numberofbuys = chrome.find_element_by_xpath(
                                '//*[@id="datatable-responsive"]/tbody/tr[{}]/td[4]'.format(num)).text

                            if int(numberofbuys) > wantednumber:
                                ebayitem = (chrome.find_element_by_xpath(
                                    '//*[@id="datatable-responsive"]/tbody/tr[{}]/td[2]/h4/b/a'.format(
                                        num)).get_attribute('href'))
                                print(ebayitem, data.at[count, 'Names'])
                                ebaygooditems = [data.at[count, 'Names'], ebayitem, datetime.datetime.now(), numberofbuys]
                                savedropitems(ebaygooditems)
                    data.at[count, 'Last Scan'] = datetime.datetime.now()
                    data.to_csv('Database\dropshippername.csv', index=False)
                else:
                    data.at[count, 'Last Scan'] = datetime.datetime.now()
                    data.to_csv('Database\dropshippername.csv', index=False)
            except Exception as err:
                print(err)
                pass
        else:
            if lastscan < (datetime.datetime.now() - datetime.timedelta(days=8)):
                chrome.get('https://zikanalytics.com/SearchCompetitor/Index')
                try:
                    chrome.find_element_by_id('srcUsername').send_keys(data.at[count, 'Names'])
                    chrome.find_element_by_xpath(
                        '/html/body/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/select/option[4]').click()
                    chrome.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/button').click()
                    time.sleep(3)
                    if chrome.find_element_by_xpath('//*[@id="info"]').text !='The seller had no sales for the selected period.':
                        try:
                            element = WebDriverWait(chrome, 15).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//*[@id="datatable-responsive"]/tbody/tr[1]/td[4]'))
                            )
                        finally:
                            time.sleep(2)
                            loopfor = chrome.find_element_by_xpath('//*[@id="header"]/div[8]/div/div[3]').text
                            if int(loopfor) > 30:
                                loopfor = 30
                            for num in range(1, int(loopfor)):
                                numberofbuys = chrome.find_element_by_xpath(
                                    '//*[@id="datatable-responsive"]/tbody/tr[{}]/td[4]'.format(num)).text

                                if int(numberofbuys) > wantednumber:
                                    ebayitem = (chrome.find_element_by_xpath(
                                        '//*[@id="datatable-responsive"]/tbody/tr[{}]/td[2]/h4/b/a'.format(
                                            num)).get_attribute('href'))
                                    print(ebayitem,data.at[count, 'Names'])
                                    ebaygooditems=[data.at[count, 'Names'],ebayitem,datetime.datetime.now(),numberofbuys]
                                    savedropitems(ebaygooditems)
                        data.at[count, 'Last Scan'] = datetime.datetime.now()
                        data.to_csv('Database\dropshippername.csv', index=False)
                    else:
                        data.at[count, 'Last Scan'] = datetime.datetime.now()
                        data.to_csv('Database\dropshippername.csv', index=False)
                except Exception as err:
                    print(err)
                    pass

def findgooddropshippers():
    chrome = ziklogin()
    for x in range(0, 5000):
        k = searchzikwithamazonitem(chrome)
    chrome.quit()

def findgooditems():
    chrome = ziklogin()
    searchdropshipperinzik(chrome)
    chrome.quit()

class tkguiwindow():
    def __init__(self,master):
        master.title("Monitor")
        master.geometry('300x300')
        self.dropshipperlbl = Label(master, text="Find DropShippers")
        self.dropshipperlbl.grid(column=0, row=0)

        self.dropshipperButton=Button(master,text="Start",command=self.dropbutton)
        self.dropshipperButton.grid(column=1, row=0)

        self.dropshipperitemlbl = Label(master, text="Scan dropShippers items")
        self.dropshipperitemlbl.grid(column=0, row=1)

        self.dropshipperitemButton = Button(master, text="Start", command=self.itembutton)
        self.dropshipperitemButton.grid(column=1, row=1)

    def dropbutton(self):
        self.dropshipperButton.configure(text="Loading")
        def callback():
            findgooddropshippers()
        t = threading.Thread(target=callback)
        t.start()


    def itembutton(self):
        self.dropshipperitemButton.configure(text="Loading")
        def callback1():
            findgooditems()
        t = threading.Thread(target=callback1)
        t.start()



root=Tk()
monitor=tkguiwindow(root)
root.mainloop()
