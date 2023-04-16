 # python-591-data(20210821)
這個專案根據 [API規格.txt](https://github.com/a0979470582/python-591-data/blob/main/API%E8%A6%8F%E6%A0%BC.txt) 內定義的題目要求，提供一個 Restful API 讓客戶端可以傳入不同條件搜尋房屋。
 
 例如想搜尋的標的為: 位於台北 且 女性屋主 且 姓氏為吳，則我們可以將下面的網址鍵入瀏覽器來進行搜尋(由於運行伺服器需要成本，因此當前伺服器未開啟):
 
 
      http://104.199.237.229:8888/search?region=台北市&homeOwnerIsWoman=1&homeOwnerLastName=吳

關於此專案的相關資訊: 
1. 使用 Python 語言來實現從 591租屋網 取得租屋資料。
2. 使用 SoupBeautiful 套件將原始房屋資料進行分析，分析後存入本地 MongoDB 資料庫。
3. 在 GCP 的 Compute Engine 架設 Flask 伺服器, 來實作並提供客戶端 Restful API。
4. 最後，使用者可以用 Restful API 來搜尋 MongoDB 中的租屋資料, 且 API 網址後方可以帶入不同條件進行自定義搜尋。
    
