import sqlite3,ast,requests,os
from bs4 import BeautifulSoup

cur_path=os.path.dirname(__file__)
conn=sqlite3.connect(cur_path+'/'+'DataBasePM25.sqlite')
cursor=conn.cursor()


sqlstr='''
CREATE TABLE IF NOT EXISTS TablePM25 ("no" INTEGER PRIMARY KEY AUTOINCREMENT
NOT NULL UNIQUE ,"SiteName" TEXT NOT NULL ,"PM25" INTEGER)
'''
cursor.execute(sqlstr)

url="http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"

html=requests.get(url).text.encode('utf-8-sig')

print('資料已更新...')
sp=BeautifulSoup(html,'html.parser')

jsondata=ast.literal_eval(sp.text)

conn.execute("delete from TablePM25")
conn.commit()

n=1
for site in jsondata:
    SiteName=site["SiteName"]
    if site["PM2.5"]=="ND":
        continue
    PM25=0 if site["PM2.5"]=="" else int(site["PM2.5"])
    print("站名:{}  PM2.5={}".format(SiteName,PM25))

    sqlstr="insert into TablePM25 values({},'{}',{})".format(n,SiteName,PM25)
    cursor.execute(sqlstr)
    n+=1
    conn.commit()

conn.close()