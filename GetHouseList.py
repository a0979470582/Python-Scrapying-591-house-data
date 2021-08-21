import requests
from bs4 import BeautifulSoup
import json
import csv
import dbHelper as db
import toolHelper as tool
import time


#進入主頁取得csrf-token, 保存在cookie中
def getCsrfToken(session, url_591 = 'https://rent.591.com.tw/'):
    bs = BeautifulSoup(session.get(url_591, cookies={'urlJumpIp':'1'}).text, 'html.parser')
    tag = bs.html.head.find('meta', {'name':'csrf-token'})
    token = tag.attrs['content']
    return token

#請求狀態等於200就回傳true
def checkStatusCode(status_code):
    return status_code == requests.codes.ok

#api範例:
#https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow=30&totalRows=9005
#https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow=60&totalRows=9010
#......
#https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow=9000&totalRows=9011
#根據地區碼和資料行數發送一次request, 回傳的純HTML包含三十筆房屋資料
def getHouseListHtml(session, csrf_Token, region_code, row_Number):
    url_getHouseListApi = 'https://rent.591.com.tw/home/search/rsList'
    my_params = {'is_new_list': 1,
                 'type': 1,
                 'kind': 0,
                 'searchtype': 1,
                 'firstRow': row_Number,
                 'totalRows':12233}  
    
    my_headers = {'X-CSRF-TOKEN': csrf_Token}

    response = session.get(url_getHouseListApi, headers = my_headers, params = my_params, cookies={'urlJumpIp':str(region_code)})

    if checkStatusCode(response.status_code) is False:
        return ""
        
    html_text = response.text
    return html_text
    
#傳入純HTML, 解析出其中的三十筆房屋資料的id
def getHouseList(html_text):
    house_dict = json.loads(html_text)#house_dict是完整的json檔
    house_list = house_dict['data']['data']#house_list是三十筆房屋資料形成的List
    return house_list

#傳入純HTML, 解析出該地區資料總筆數(總筆數會浮動)
def getTotalNumber(html_text):
    house_dict = json.loads(html_text)#house_dict是完整的json檔
    totalNumber = house_dict['records']
    return int(totalNumber.replace(',', '')) 
    

def mainGetHouseList(region_code):
    number = 0
    totalNumber = 0
    while number <= totalNumber:
        html_text = getHouseListHtml(session, csrf_Token, region_code, number)
        
        if html_text == "":
            tool.logCrawlProgress("failure, fuck\n")
            break
            
        house_list = getHouseList(html_text)
        db.insertManyHouse(house_list)
        
        number += 30
        totalNumber = getTotalNumber(html_text)
        
        timeString = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        tool.logCrawlProgress("{0}  {1}-{2}  {3}\n".format(timeString, number-30, number, totalNumber))

taipei_region_code = 1
newtaipei_region_code = 3   

session = requests.session()
csrf_Token = getCsrfToken(session)#only get once

if __name__ == '__main__':    
    mainGetHouseList(newtaipei_region_code)