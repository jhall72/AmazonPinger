from random import randrange, randint
import sqlalchemy as sa
import requests
from bs4 import BeautifulSoup
import time
from datetime import date
print("STARTING")
engine = sa.create_engine('')
connection = engine.connect()
metadata = sa.MetaData()
PriceTag = sa.Table('PriceTag', metadata, autoload=True, autoload_with=engine)

s = sa.select([PriceTag])
result = connection.execute(s)
pingcount = 0
today = str(date.today())

NameList = []
PriceList = []
URLList = []
TimeList = []
ProductIDList = []
InStockList = []
ExcludeNameList = []

for prerow in result:
    print()
    print("CHECKING IF ", str(prerow[3]), " IS ", str(today))
    if (str(prerow[3]) == str(today)):
        print("IT IS, ADDING TO EXCLUDE LIST: ", str(prerow[4]))
        ExcludeNameList.append(prerow[4])
    else:
        print("IT IS NOT")

result = connection.execute(s)
print()
print("SEARCHING QUERY RESULTS")
for row in result:
    print()
    print("SEARCHING: ", row[4])
    if row[4] in ExcludeNameList:
        print("PRODUCT HAS ENTRY FOR TODAY, SKIPPING.")
        continue
    else:
        print("NOT IN EXLCUDED NAME LIST")
    if row[4] in NameList:
        index = NameList.index(row[4])
        print("INDEX: ", str(index),"INDEX NAME: ", NameList[index])
        print("Is ", row[3], " GRATHER THAN ", TimeList[index])
        if row[3] > TimeList[index]:
            print("YES")
            del NameList[index]
            del PriceList[index]
            del URLList[index]
            del TimeList[index]
            del ProductIDList[index]
            del InStockList[index]
            NameList.append(row[4])
            URLList.append((row[1]))
            PriceList.append((row[2]))
            TimeList.append(row[3])
            ProductIDList.append(row[5])
            InStockList.append(row[6])
        else:
            print("NO")
    else:
        NameList.append(row[4])
        URLList.append(row[1])
        PriceList.append(row[2])
        TimeList.append(row[3])
        ProductIDList.append(row[5])
        InStockList.append(row[6])
print()
print("WEBSCRAPING FINAL RESULTS")
v = 0
i = 0


def my_function(a, pingcount, i):
    if (pingcount < 10):
        try:
            pingcount = pingcount + 1
            print("NAME: ",NameList[i])
            print("URL: ",URLList[i])
            print("LAST LISTED PRICE: ",PriceList[i])
            delay = randint(5,30)
            print("DELAY: ",delay)
            time.sleep(delay)
            url = URLList[i]
            randNum = str(randrange(10000))
            headers = { "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate",     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1" }
            html = requests.get(url, headers=headers)
            soup1 = BeautifulSoup(html.text, 'html.parser')
            soup = BeautifulSoup(soup1.prettify(), 'html.parser')
            headerInfo = soup.find("div", {"id": "cerberus-data-metrics"})
            price = headerInfo['data-asin-price']

            if (str(price) != str(PriceList[i])):
                print("PRICE CHANGED, NEW PRICE: ",price)
                ins = PriceTag.insert().values(
                    URL=URLList[i],
                    Price=str(price),
                    CheckTime=date.today(),
                    ProductName=str(NameList[i]),
                    ProductID=str(ProductIDList[i]),
                    inStock=str(InStockList[i]))


                connection.execute(ins)
            else:
                print("PRICE UNCHANGED")
            print("")
        except:
            my_function(a, pingcount, i)
    else:
        print("Too many errors for: ",NameList[i])

for a in PriceList:
    my_function(a, pingcount, i)
    i = i + 1

print()
print("ENDING")
