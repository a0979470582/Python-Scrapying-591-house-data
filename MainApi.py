import flask
from flask import request
from flask import jsonify
import dbHelper as db
from pymongo import MongoClient
import json


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
