import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import warnings

from itertools import chain
from itertools import zip_longest

warnings.filterwarnings("ignore")

# Getting the info from webpage
STOCKS = ["ACSEL"]
url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=ACSEL"
request = requests.get(url)
supply = BeautifulSoup(request.text, "html.parser")
stockSupplier = supply.find("select", id="ddlAddCompare")
rawStocks = stockSupplier.findChild("optgroup").findAll("option")

# Getting the names of stocks from webpage
# for stock in rawStocks:
#     STOCKS.append(stock.string)

# Get each stocks date and period
for each in STOCKS:
    stockName = each
    dates = []

    url1 = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+stockName
    req1 = requests.get(url1)
    soup = BeautifulSoup(req1.text, "html.parser")
    selectDate = soup.find("select", id="ddlMaliTabloFirst")
    selectValue = soup.find("select", id="ddlMaliTabloGroup")

    try:
        children = selectDate.findChildren("option")
        value = selectValue.find("option")["value"]

        for child in children:
            dates.append(child.string.rsplit("/"))

        def grouper(iterable, n, fillvalue=None):
            args = [iter(iterable)] * n
            return zip_longest(*args, fillvalue=fillvalue)

        dates = [list(filter(None, group)) for group in grouper(dates, 4, fillvalue=['2023', '9'])]

        for a, b, c, d in dates:
            parameters = (
                ("companyCode", stockName),
                ("exchange", "TRY"),
                ("financialGroup", value),
                ("year1", a[0]),
                ("period1", a[1]),
                ("year2", b[0]),
                ("period2", b[1]),
                ("year3", c[0]),
                ("period3", c[1]),
                ("year4", d[0]),
                ("period4", d[1]),
            )
            d1 = a[0] + '/' + a[1]
            d2 = b[0] + '/' + b[1]
            d3 = c[0] + '/' + c[1]
            d4 = d[0] + '/' + d[1]

            url2 = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
            req2 = requests.get(url2, params=parameters).json()["value"]
            data = pd.DataFrame.from_dict(req2)
            data = data.drop(['itemCode', 'itemDescEng'], axis=1)
            filteredData = data.rename(columns={'value1': d1, 'value2': d2, 'value3': d3, 'value4': d4})
            
            print(filteredData[filteredData['itemDescTr'] == 'BRÜT KAR (ZARAR)'])

    except AttributeError:
        continue
