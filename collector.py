import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import warnings
from itertools import zip_longest

warnings.filterwarnings("ignore")

# Getting the info from webpage
STOCKS = ["ACSEL","ADEL","AFYON","AGROT","AKCNS","ATEKS","AKSA","ALCAR","ALKIM","ALKA","ALMAD","AEFES","ASUZU","ANGEN","ARCLK","ARSAN","ASTOR","ATAKP","AVOD",
          "AYGAZ","BAGFS","BAKAB","BNTAS","BANVT","BARMA","BTCIM","BSOKE","BAYRK","BRKSN","BIENY","BLCYT","BMSTL","BMSCH","BOBET","BRSAN","BFREN","BOSSA",
          "BRISA","BURCE","BURVA","BUCIM","BVSAN","CCOLA","CVKMD","CELHA","CEMSA","CEMTS","CMBTN","CIMSA","CUSAN","DAGI","DARDL","DMSAS","DERIM","DESA","DEVA",
          "DNISI","DITAS","DMRGD","DOFER","DGNMO","DOGUB","DOKTA","DURDO","DYOBY","EGEEN","EGGUB","EGPRO","EGSER","EPLAS","EKOS","EKSUN","ELITE","EMKEL",
          "ENSRI","ERBOS","ERCB","EREGL","ERSU","TEZOL","EUREN","EUPWR","FADE","FMIZP","FROTO","FORMT","FRIGO","GEDZA","GENTS","GEREL","GIPTA","GOODY",
          "GOKNR","GOLTS","GUBRF","HATEK","HATSN","HEKTS","HKTM","ISKLP","IHEVA","IMASM","IPEKE","ISDMR","ISSEN","IZINV","IZMDC","IZFAS","JANTS","KLKIM",
          "KLSER","KAPLM","KRDMA","KRMDB","KRDMD","KARSN","KRTEK","KARTN","KATMR","KAYSE","KERVT","KRVGD","KMPUR","KLMSN","KCAER","KLSYN","KNFRT","KONYA",
          "KONKA","KORDS","KRPLS","KOZAL","KOZAA","KOPOL","KRSTL","KBORU","KUTPO","KTSKR","LUKSK","MAKIM","MAKTK","MRSHL","MEDTR","MEGMT","MEGAP","MEKAG",
          "MNDRS","MERCN","MERKO","MNDTR","NIBAS","NUHCM","OFSYM","ONCSM","ORCAY","OTKAR","OYAKC","OYLUM","OZRDN","OZSUB","PNLSN","PRKME","PARSN","PENGD",
          "PETKM","PETUN","PINSU","PNSUT","POLTK","PRZMA","QUAGR","RNPOL","RODRG","RTALB","RUBNS","SAFKR","SNICA","SANFM","SAMAT","SARKY","SASA","SAYAS",
          "SEKUR","SELGD","SELVA","SEYKM","SILVR","SOKE","SKTAS","SUNTK","TARKM","TATGD","TMPOL","TETMT","TOASO","TUCLK","TUKAS","MARBL","TRILC","TMSN",
          "TUPRS","PRKAB","TTRAK","ULUSE","ULUUN","USAK","ULKER","VANGD","VESBE","VESTL","VKING","YAPRK","YATAS","YYLGD","YKLSN","YUNSA"]                                                                                                                                                                   

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
    dates = []
    stockData = []
    title = 'Bilanço'

    url1 = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+each
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

        dates = [list(filter(None, group)) for group in grouper(dates, 4)]
        proper_list = [sublist for sublist in dates if len(sublist) >= 4]

        for a, b, c, d in proper_list:
            parameters = (
                ("companyCode", each),
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
            filteredData = data.filter(items=['itemDescTr', 'value1', 'value2', 'value3', 'value4'])
            filteredData = filteredData.rename(columns={'itemDescTr': title,'value1': d1, 'value2': d2, 'value3': d3, 'value4': d4})
            filteredData.drop_duplicates(subset=title, inplace=True)
            filteredData.set_index(title, inplace=True)
 
            stockData.append(filteredData)

        df = pd.concat(stockData, axis=1)
        df.fillna(0, inplace=True)
        # df = df.loc[:, ~df.columns.duplicated()]
        df = df.astype(int)
        
        df.to_excel("/home/gun/Documents/ReportCollector/FinancialReports/{}.xlsx".format(each), index=True)
    except AttributeError:
        continue
