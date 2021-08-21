from pymongo import MongoClient
import dbHelper as db
import requests
from bs4 import BeautifulSoup
import time
import toolHelper as tool

def get_phone_number(post_id):
    urlApi = 'https://rent.591.com.tw/rent-detail-{0}.html'.format(post_id)
    bs = BeautifulSoup(requests.get(urlApi).text, 'html.parser')
    tag = bs.find('span', {'class': 'dialPhoneNum'})
    if tag is None:
        return ''
    
    phone = tag.get('data-value')
    if phone == '':
        phone = bs.find('div', 'hidtel').text

    if phone != '':
        return phone.replace('-','')


def house_map_detail(house):
    house_dict = {}
    
    #發帖id
    house_dict['postid'] = house['id']
    
    #城市
    region_map = {1:'台北市', 3:'新北市'}
    house_dict['region'] = region_map.get(house['regionid'])
    
    #注意 太太, 媽媽, 阿姨, 小姐, 女士
    house_dict['renterName'] = house['linkman']
    
    #身分
    house_type_map = {1:'屋主', 2:'代理人', 3:'仲介'}
    house_dict['housetype'] = house_type_map.get(house['housetype'])
    
    #建築型態
    shape_map = {0:'無', 1:'公寓', 2:'電梯大樓', 3:'透天厝', 4:'別墅', 5:'華廈', 6:'住宅大樓', 7:'店面（店鋪）'}
    house_dict['shape'] = shape_map.get(house['shape'])
    
    #出租型態
    kind_map = {1:'整層住家', 2:'獨立套房', 3:'分租套房', 4:'雅房', 8:'車位', 24:'其他'}
    house_dict['kind'] = kind_map.get(house['kind'])
    
    #性別
    #有可能該屋主沒有設定此項條件, 此情況也屬於all_sex
    gender = '男女生皆可'
    if 'boy' in house['condition']:
        gender = '男生'
    if 'girl' in house['condition']:
        gender = '女生'
        
    house_dict['gender'] = gender
    
    #phoneNumber
    #電話根據postid去詳情頁取得, 組合完整後再存入detail_table
    
    return house_dict


if __name__ == '__main__':    

    house_list = db.loadAllHouse()#載入從api取得的所有房子
    for index, house in enumerate(house_list[14000:]):
        print(house['id'])
        #資料庫已有此筆資料就略過此房子
        if db.isRepeat(house['id']):
            timeString = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
            tool.logCrawlProgress("{0}  index:{1}  postid:{2} repeat\n".format(timeString, index, house['id']))
            continue
        
        house_dict = house_map_detail(house)#轉換成題目要求的schema
        house_dict['phoneNumber'] = get_phone_number(house['id'])#發送request取得phoneNumber

        """
            house_dict是完整的資料:
            {'postid': 10705634, 'region': '台北市', 'renterName': '李小姐', 'housetype': '屋主',
             'shape': '公寓', 'kind': '分租套房','gender': '男女生皆可' , 'phoneNumber': '0955860558'}
        """
        
        db.insetOneDetail(house_dict)
        
        timeString = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        tool.logCrawlProgress("{0}  index:{1}  postid:{2} success\n".format(timeString, index, house['id']))
