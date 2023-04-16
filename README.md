 # python-591-data(20210821)
 本 Repo 根據 [API規格.txt](https://github.com/a0979470582/python-591-data/blob/main/API%E8%A6%8F%E6%A0%BC.txt) 內定義的題目要求，提供一個 Restful API 讓客戶端可以傳入不同條件搜尋房屋。
 
 例如想搜尋的標的為: 位於台北 且 女性屋主 且 姓氏為吳。
 
 則我們可以將下面的網址鍵入瀏覽器來進行搜尋(由於運行伺服器需要成本，因此當前伺服器未開啟):
 
 
      http://104.199.237.229:8888/search?region=台北市&homeOwnerIsWoman=1&homeOwnerLastName=吳

1. 使用 Python 抓取 591租屋網 的租屋資料
2. 使用 SoupBeautiful 套件 分析後存入 MongoDB
3. 在 GCP 的 Compute Engine 架一個簡易的 Flask 伺服器, 來實作 Restful API
4. 使用者可用 API 搜尋 MongoDB 中的租屋資料, 且在 API 網址 後夾帶不同參數, 可自訂條件搜尋
    
