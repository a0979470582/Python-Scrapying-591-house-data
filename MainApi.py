import flask
from flask import request
from flask import jsonify
import dbHelper as db
from pymongo import MongoClient
import json



"""API規格

    http://104.199.237.229:8888/search?region=新北市
    
    可選參數:可選值(多個值請用逗號分隔, 例如search?region="新北市","台北市")
    region: 新北市; 台北市
    gender: 男生; 女生; 男女生皆可
    housetype: 屋主; 代理人; 仲介
    phoneNumber: 任意電話號碼, 例如0912345678
    homeOwnerIsWoman: 0:無限制 1:女屋主
    homeOwnerLastName: 任意屋主姓氏
    
    
    回傳的Json Schema
    {
      "totalNumber": 20, 
      "data": [
        {
          "postid": 10678298, 
          "region": "台北市", 
          "renterName": "王阿姨", 
          "housetype": "屋主", 
          "shape": "公寓", 
          "kind": "分租套房", 
          "gender": "女生", 
          "phoneNumber": "0931287385"
        }, ....
      ]
    }
    
    題目要求
    1.男生可承租 且 位於新北
      http://104.199.237.229:8888/search?region=新北市&gender=男生
    2.以聯絡電話搜尋
      http://104.199.237.229:8888/search?phoneNumber=0937938302
    3.非屋主自行刊登
      http://104.199.237.229:8888/search?housetype=仲介,代理人
    4.位於台北 且 女性屋主 且 姓氏為吳
      http://104.199.237.229:8888/search?region=台北市&homeOwnerIsWoman=1&homeOwnerLastName=吳
    
    
    註記:
    1. MongoDB可針對可搜索欄位加入索引, 可加快搜索速度, 但目前資料數少還不需要, 參考:
        https://www.runoob.com/mongodb/mongodb-indexing.html
    2. 在生產環境中應使用更為穩定的Web框架
"""

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False#可顯示UTF-8字元
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True#加入換行和縮排
app.config['JSON_SORT_KEYS'] = False#不重排序json欄位

#假如有收到該參數就加入搜尋條件
def makeSearchCondition(condition, key):
    value = request.args.get(key)#參數值或None
    if value is not None:
        condition[key] = {'$in': value.split(',')}
    return condition
    
def mainHandleCondition():
        
    condition = {}
    makeSearchCondition(condition, 'region')
    makeSearchCondition(condition, 'gender')
    makeSearchCondition(condition, 'housetype')
    makeSearchCondition(condition, 'phoneNumber')

    
    #進一步處理這兩個條件, 他們欄位名稱與資料庫的欄位名稱不同, 且他們不是只有比較是否相等
    #注意這兩個條件都會判斷renterName, 需要處理兩個條件同時使用的情況
    
    regexString = ''
    
    #比較姓名中的第一個字
    lastName = request.args.get('homeOwnerLastName')
    if lastName is not None:
        regexString = "^{0}".format(lastName)
        condition['renterName'] = {"$regex": regexString} 
    
    #判斷是否設定女屋主, 以下邏輯是1為女屋主, 而0和其他任何參數值為無限制
    #若為1則houseType設為屋主, 且renterName必須包含太太, 媽媽, 阿姨, 小姐, 女士
    #$regex是正規表達式用法
    isWoman = request.args.get('homeOwnerIsWoman')
    if isWoman == '1':
        regexString += "[太太|媽媽|阿姨|小姐|女士]"
        condition['housetype'] = '屋主'
        condition['renterName'] = {"$regex": regexString} 
    
    return condition
    
@app.route('/search', methods=['GET'])
def searchDetail():
    
    condition = mainHandleCondition()
    print(condition)
    table_detail = db.getTable('table_detail')
    result = table_detail.find(condition, {'_id':0})
    
    return_json = {
        'totalNumber':result.count(),
        'data':list(result)
    }
    
    
    #jsonify會讓HTTP的Response設為Content-Type: application/json
    #若使用json.dumps只是單純轉成json, 還需要手動設定Response的Content-Type
    return jsonify(return_json)
   
    
#若開啟debug模式, 除了API的port之外, flask還會另開一個port: 5000用來除錯
app.run(debug=False, host="0.0.0.0", port=8888)
