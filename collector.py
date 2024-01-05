import requests
from bs4 import BeautifulSoup
import pandas as pd


STOCKS = {"ACSEL", "AKBNK"}
url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=ACSEL"
request = requests.get(url)
supply = BeautifulSoup(request.text, "html.parser")
stockSupplier = supply.find("select", id="ddlAddCompare")
rawStocks = stockSupplier.findChild("optgroup").findAll("option")

# for stock in rawStocks:
#     STOCKS.append(stock.string)

for each in STOCKS:
    nameOfStock = each
    dates = []
    store = {}
    url1 = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+nameOfStock
    req1 = requests.get(url1)
    soup = BeautifulSoup(req1.text, "html.parser")
    selectDate = soup.find("select", id="ddlMaliTabloFirst")
    selectValue = soup.find("select", id="ddlMaliTabloGroup")

    children = selectDate.findChildren("option")
    value = selectValue.find("option")["value"]

    for child in children:
        dates.append(child.string.rsplit("/"))
        store[each] = dates
    print(store)
