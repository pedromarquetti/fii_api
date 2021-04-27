from collections import OrderedDict
import requests as req
from bs4 import BeautifulSoup as bs
import argparse


def main():
    agent = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    URL = r"https://www.fundsexplorer.com.br/ranking"
    s = req.Session()
    get = s.request("get",URL,headers=agent)
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
    parser = argparse.ArgumentParser(description="Bem vindo ao menu de ajuda, aqui você encontra todos os possíveis comandos que podem ser executados")
    parser.add_argument("nome",help="nome do fii (XXXX11)")
    parser.add_argument("-l",help="Mostra a liquidez do FII",action="store_true")
    parsed = parser.parse_args()
    try:
        print(
f"""
Nome: {parsed.nome}
Preço atual: {result[parsed.nome]["Preço Atual"]},
Último rendimento: {result[parsed.nome]["Dividendo"]},
""")
        if parsed.l:
            print(f"""Liquidez Diária: {result[parsed.nome]["Liquidez Diária"]}""")
    except KeyError or NameError as e:
        print("key not found, try:\n")
        for k,v in result.items():
            print(f"names: {k}")
    