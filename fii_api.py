from collections import OrderedDict
import requests as req
from bs4 import BeautifulSoup as bs

URL = r"https://www.fundsexplorer.com.br/ranking"
FILE = "index.html"
data = {
    "Código":1,
    "Setor":"",
    "Preço Atual":"",
    "Liquidez Diária":"",
    "Dividendo":"",
    "Dividend":"",
    "Yield":"",
    "DY (3M)":"",
    "Acumulado":"",
    "DY (6M)":"",
    "Acumulado":"",
    "DY (12M)":"",
    "Acumulado":"",
    "DY (3M)":"",
    "Média":"",
    "DY (6M)":"",
    "Média":"",
    "DY (12M)":"",
    "Média":"",
    "DY Ano":"",
    "Variação Preço":"",
    "Rentab":"",
    "Período":"",
    "Rentab":"",
    "Acumulada":"",
    "Patrimônio":"",
    "Líq":"",
    "VPA":"",
    "P/VPA":"",
    "DY":"",
    "Patrimonial":"",
    "Variação":"",
    "Patrimonial":"",
    "Rentab. Patr.":"",
    "no Período":"",
    "Rentab. Patr.":"",
    "Acumulada":"",
    "Vacância":"",
    "Física":"",
    "Vacância":"",
    "Financeira":"",
    "Quantidade":"",
    "Ativos":"",
}
# with req.Session() as s:
#     get = s.request("get",URL)

#     f = open("index.html","w")
#     f.write(get.text)    
f = open(FILE,"r")
soup = bs(f,"lxml")
tr = soup.find_all("tr")[1:]

print(data["Código"])
def createdic():
    result = OrderedDict()
    for items in tr: 
        try:
            td = items.find_all("td")
            # print(td[data["Código"]].getText()) # fii names
            # print(td[1].getText())
            result.update()


        except Exception as err:
            print(err)
        
createdic()



