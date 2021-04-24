from collections import OrderedDict
import requests as req
from bs4 import BeautifulSoup as bs

def main():
    URL = r"https://www.fundsexplorer.com.br/ranking"
    s = req.Session()
    get = s.request("get",URL)
    soup = bs(get.text,"lxml")
    tr = soup.find_all("tr")[1:]
    result = OrderedDict()
    for items in tr: 
        td = items.find_all("td")

        result.update({td[0].getText():
            {
                "Setor":td[1].getText(),
                "Preço Atual":td[2].getText(),
                "Liquidez Diária":td[3].getText(),
                "Dividendo":td[4].getText(),
                "DividendYield":td[5].getText(),
                "DY (3M) Acumulado":td[6].getText(),
                "DY (6M) Acumulado":td[7].getText(),
                "DY (12M) Acumulado":td[8].getText(),
                "DY (3M) Média":td[9].getText(),
                "DY (6M) Média":td[10].getText(),
                "DY (12M) Média":td[11].getText(),
                "DY Ano":td[12].getText(),
                "Variação Preço":td[13].getText(),
                "Rentab Período":td[14].getText(),
                "Rentab Acumulada":td[15].getText(),
                "Patrimônio Líq":td[16].getText(),
                "VPA":td[17].getText(),
                "P/VPA":td[18].getText(),
                "DY Patrimonial":td[19].getText(),
                "Variação Patrimonial":td[20].getText(),
                "Rentab. Patr. no Período":td[21].getText(),
                "Rentab. Patr. Acumulada":td[22].getText(),
                "Vacância Física":td[23].getText(),
                "Vacância financeira":td[24].getText(),
                "Quantidade de ativos":td[25].getText(),
            }
            })


    return result
        
if __name__ == "__main__":
    result = main()
    # you can print locally as ["FII"]["#value"]
    