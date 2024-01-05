import requests
from bs4 import BeautifulSoup
import pandas as pd


STOCKS = ["ACSEL"]
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
    year = []
    period = []
    url1 = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+nameOfStock
    req1 = requests.get(url1)
    soup = BeautifulSoup(req1.text, "html.parser")
    selectDate = soup.find("select", id="ddlMaliTabloFirst")
    selectValue = soup.find("select", id="ddlMaliTabloGroup")

    try:
        children = selectDate.findChildren("option")
        value = selectValue.find("option")["value"]

        for child in children:
            dates.append(child.string.rsplit("/"))
            store[each] = dates

        for i in store[each]:
            year.append(i[0])
            period.append(i[1])

        parameters = (
            ("companyCode", nameOfStock),
            ("exchange", "TRY"),
            ("financialGroup", value),
            ("year1", year[0]),
            ("period1", period[0]),
            ("year2", year[1]),
            ("period2", period[1]),
            ("year3", year[2]),
            ("period3", period[2]),
            ("year4", year[3]),
            ("period4", period[3]),
        )

        url2 = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
        req2 = requests.get(url2, params=parameters).json()["value"]
        data = pd.DataFrame.from_dict(req2)
        data.drop(columns=["itemCode", "itemDescEng"], inplace=True)
        print(data)
        
    except AttributeError:
        continue

