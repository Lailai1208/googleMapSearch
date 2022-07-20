from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import pyautogui  #模擬鍵盤、模擬滑鼠
from selenium.webdriver import ActionChains  #模擬滑鼠
from pynput.keyboard import Key, Controller #控制鍵判
import pandas as pd
# import requests
# from selenium.webdriver.common.by import By
from pathlib import Path
import urllib
import os

def make_dir():
    ccco1 = ['信義區']
    try:
        for skfd in range(len(ccco1)):
            dis_name = ccco1[skfd]+'餐廳_data'
            dis_name1 = ccco1[skfd]+'餐廳_images'
            os.mkdir(dis_name)
            os.mkdir(dis_name1)
    except:
        pass
#make_dir()

##抓取店名，網址，星級，留言數
ccco = ['信義區']
for jie in range(len(ccco)):
    District = ccco[jie]+'餐廳'
    def find_data():
        driver = webdriver.Chrome("chromedriver.exe")
        translation_a = urllib.parse.quote(District) #轉碼成url可搜尋的文字
        driver.get('https://www.google.com.tw/maps/search/' + translation_a + '/@24.1623009,120.6227675,14z/data=!3m1!4b1?hl=zh-TW')
        time.sleep(5)
        
        #建list
        href_link_list = []
        title_list = []
        star_list = []
        comm_list = []  
        
        element = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a')
        actionChains = ActionChains(driver)
        
        #抓取資料
            
        for i in range(15):             
            actionChains.context_click(element).send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(5)
            keyboard = Controller()#按esc建
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            time.sleep(3)
            for j in range(11):
                time.sleep(1)
                pyautogui.press('pgdn')            
            time.sleep(1)    
            #分析網頁                       
            #抓標題&網址
            
            soup = BeautifulSoup(driver.page_source)            
            href1 = soup.find_all('a', {'class': 'hfpxzc'})#標題                                   
            for i in href1:
                href_link = i.get('href')
                title = i.get('aria-label')
                href_link_list.append(href_link)#網址
                title_list.append(title)#標題
            # print(href_link_list) 
            # print(title_list)
            
            #抓星級跟評論數
            find_star = soup.find_all('span', {'class': 'ZkP5Je'})#星級
            
            for r in find_star:
                star_list.append(r.text.split('(')[0].replace(',', ''))
                
            #print(star_list)
            
            for kk in find_star:
                if kk !=None:
                    try:
                        comm_list.append(kk.text.split('(')[1].replace(')', ''))
                    except:
                        comm_list.append(kk.text.split('(')[0])   #評論數
            #print(comm_list)
            driver.find_element_by_id('eY4Fjd').click()
            time.sleep(2)
        df = pd.DataFrame()
        df['店名'] = title_list
        df['網址'] = href_link_list
        df['星級'] = star_list
        df['評論'] = comm_list
        df.to_csv(District + '_data/'+'商家網址連結.csv', index=False, encoding='utf-8-sig')
            
    find_data()



##資料清洗
df_res=pd.read_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/商家網址連結.csv',encoding='utf-8-sig')

#name=df_res[df_res['店名'].unique()]

df_res2=df_res.drop_duplicates(subset = "店名")    
df_res3=df_res2.reset_index()
del df_res3['index']
#df_res3

drop_list=['誠品信義店','微風信義','微風南山','寶麗廣場','信義威秀商圈','新光三越 台北信義新天地A4','Grand Hyatt Taipei','寒舍艾麗酒店','新光三越 台北信義新天地A11','台北W飯店','Bencotto','台北101','誠品生活松菸店','J.W. Teres, the Bulgarian Restaurant','茹絲葵美式牛排','粵亮廣式料理-台北六福萬怡酒店','統一時代百貨 台北店','吳興商圈']

for i in drop_list:    
    df_res3=df_res3.drop(df_res3[df_res3["店名"]==i].index)
    
df_res3.to_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/商家網址連結(已清洗).csv', index=False, encoding='utf-8-sig')





##備份資料
excel_dir = Path('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data')
excel_files = excel_dir.glob('商家網址連結(已清洗).csv')
df = pd.DataFrame()
for xls in excel_files:
    print(xls)
    data = pd.read_csv(xls, sep=',' )
    df = df.append(data)
df.to_csv("C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/商家網址連結(已清洗)備分.csv", encoding='utf-8-sig', index=False, sep=',')


##留下評分高於四星的店家   
def select_data():
    df = pd.read_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/商家網址連結(已清洗)備分.csv')
    df['評論'] = df['評論'].replace('沒有評論', '0')
    df['星級'] = df['星級'].replace('沒有評論', '0')
    df['評論'] = df['評論'].str.replace(',', '')
    df['星級'] = df[['星級']].astype(float)
    df['評論'] = df[['評論']].astype(int)
    df = df[(df["評論"] > 500) & (df["星級"] > 4.0)]
    df['回復'] = ''
    df['地址'] = ''
    df.to_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/信義區餐廳_篩選評論.csv', encoding='utf-8-sig', index=False)
select_data()
    
    
    
    


##抓取留言，地址
df = pd.read_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/信義區餐廳_篩選評論.csv')

addresslist=[]
Commentlist=[]

link = list(df['網址'])

for i in link:    
    driver = webdriver.Chrome("C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data\\chromedriver.exe")
    driver.get(i)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]').click()
    time.sleep(2)
    soup2 = BeautifulSoup(driver.page_source)
    address = soup2.find('div', {'class': 'Io6YTe fontBodyMedium'})
    if address!=None:
        address=address.text
    elif address==None:
        address='not searched'
    comment=str(address)
    addresslist.append(comment)
    for j in range(2):
        time.sleep(0.5)
        pyautogui.press('pgdn')
    time.sleep(3)
    soup1 = BeautifulSoup(driver.page_source)
    comm = soup1.find_all('div', {'class': 'tBizfc fontBodyMedium'})
    comm_list = []
    for ww in comm:
        comm_list.append(ww.text.replace(' 位評論者', '').replace('"', '').replace('   ', '').replace('  ', ''))
    Commentlist.append(comm_list)
df['回復']=Commentlist
df['地址']=addresslist
df.to_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/信義區餐廳抓取留言.csv', index=False,encoding='utf-8-sig')


    
    
    
# def get_address():
#     df = pd.read_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/信義區餐廳_篩選評論.csv')
#     link = list(df['網址'])
#     for i in range(len(link)):
#         driver = webdriver.Chrome("C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data\\chromedriver.exe")
#         driver.get(link[i])
#         time.sleep(3)
#         driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]').click()
#         time.sleep(2)
#         soup2 = BeautifulSoup(driver.page_source)
#         address = soup2.find('div', {'class': 'Io6YTe fontBodyMedium'})
#         if address!=None:
#             address=address.text
#         elif address==None:
#             address='not searched'
#         time.sleep(3)
#         for j in range(2):
#             time.sleep(0.5)
#             pyautogui.press('pgdn')
#         time.sleep(3)
#         soup1 = BeautifulSoup(driver.page_source)
#         comm = soup1.find_all('div', {'class': 'tBizfc fontBodyMedium'})
#         comm_list = []
#         for ww in comm:
#             comm_list.append(ww.text.replace(' 位評論者', '').replace('"', '').replace('   ', '').replace('  ', ''))
#         print(comm_list)
#         df.loc[i, '回復'] = str(comm_list)
#         df.loc[i, '地址'] = str(address)
#         df.to_csv('C:/Users/user/Downloads/BIG_DATA/web crawler/信義區餐廳_data/信義區餐廳抓取留言.csv', index=False)
#         time.sleep(2)
# get_address() 
    
    
    
    
    
    
    