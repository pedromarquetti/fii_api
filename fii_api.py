from collections import OrderedDict
import requests as req
from bs4 import BeautifulSoup as bs
import argparse
import re

def main():
    """main function, scrapes the URL and returns a ordered dictionary"""
    agent = {  # setting user-agent
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    URL = r"https://www.fundsexplorer.com.br/ranking"  # target URL
    s = req.Session()
    # sending GET request with Session
    get = s.request("get", URL, headers=agent)
    soup = bs(get.text, "lxml")
    tr = soup.find_all("tr")[1:]  # BeautifulSoup finds all <tr> tags
    result = OrderedDict()
    for items in tr:
        td = items.find_all("td")  # finding <td> inside <tr>

        result.update({td[0].getText():  # creating Ordered Dict ({FII:{info...}})
            {"Setor": td[1].getText(),
            "Preço Atual R$": re.sub("[^0-9|\.|\-]","",td[2].getText().replace(".","").replace(",",".")),
            "Liquidez Diária": re.sub("[^0-9|\.|\-]","",td[3].getText()),
            "Dividendo R$": re.sub("[^0-9|\.|\-]","",td[4].getText().replace(".","").replace(",",".")),
            "Dividend Yield %": re.sub("[^0-9|\.|\-]","",td[5].getText().replace(".","").replace(",",".")),
            "DY (3M) Acumulado %": re.sub("[^0-9|\.|\-]","",td[6].getText().replace(".","").replace(",",".")),
            "DY (6M) Acumulado  %": re.sub("[^0-9|\.|\-]","",td[7].getText().replace(".","").replace(",",".")),
            "DY (12M) Acumulado %": re.sub("[^0-9|\.|\-]","",td[8].getText().replace(".","").replace(",",".")),
            "DY (3M) Média %": re.sub("[^0-9|\.|\-]","",td[9].getText().replace(".","").replace(",",".")),
            "DY (6M) Média %": re.sub("[^0-9|\.|\-]","",td[10].getText().replace(".","").replace(",",".")),
            "DY (12M) Média %": re.sub("[^0-9|\.|\-]","",td[11].getText().replace(".","").replace(",",".")),
            "DY Ano %": re.sub("[^0-9|\.|\-]","",td[12].getText().replace(".","").replace(",",".")),
            "Variação Preço %": re.sub("[^0-9|\.|\-]","",td[13].getText().replace(".","").replace(",",".")),
            "Rentab Período %": re.sub("[^0-9|\.|\-]","",td[14].getText().replace(".","").replace(",",".")),
            "Rentab Acumulada %": re.sub("[^0-9|\.|\-]","",td[15].getText().replace(".","").replace(",",".")),
            "Patrimônio Líq R$": re.sub("[^0-9|\.|\-]","",td[16].getText().replace(".","").replace(",",".")),
            "VPA R$": re.sub("[^0-9|\.|\-]","",td[17].getText().replace(".","").replace(",",".")),
            "P/VPA": re.sub("[^0-9|\.|\-]","",td[18].getText().replace(".","").replace(",",".")),
            "DY Patrimonial %": re.sub("[^0-9|\.|\-]","",td[19].getText().replace(".","").replace(",",".")),
            "Variação Patrimonial %": re.sub("[^0-9|\.|\-]","",td[20].getText().replace(".","").replace(",",".")),
            "Rentab. Patr. no Período %": re.sub("[^0-9|\.|\-]","",td[21].getText().replace(".","").replace(",",".")),
            "Rentab. Patr. Acumulada %": re.sub("[^0-9|\.|\-]","",td[22].getText().replace(".","").replace(",",".")),
            "Vacância Física %": re.sub("[^0-9|\.|\-]","",td[23].getText().replace(".","").replace(",",".")),
            "Vacância financeira %": re.sub("[^0-9|\.|\-]","",td[24].getText().replace(".","").replace(",",".")),
            "Quantidade de ativos": re.sub("[^0-9|\.|\-]","",td[25].getText().replace(".","").replace(",",".")),
                }
            }
        )
    return result


if __name__ == "__main__":
    result = main()  # dic obj
    parser = argparse.ArgumentParser(
        description="Bem vindo ao menu de ajuda, aqui você encontra todos os possíveis comandos que podem ser executados",
        usage="py (ou python3) fii_api.py [-h] [-l](liquidez) [-dy](dividend yield) nome do FII"
    )  # Argument Parser object
    # adding necessary arg
    parser.add_argument("nome", help="nome do fii (XXXX11)")
    parser.add_argument("-l", help="Mostra a liquidez do FII",
                        action="store_true")  # optional arg
    parser.add_argument("-dy", 
                        help="Mostra informações sobre o Dividend Yield do FII",
                        action="store_true")
    parser.add_argument("-all", help="Mostra todas as informações do FII",
                        action="store_true")  # optional arg

    parsed = parser.parse_args()
    try:
        FII = result[parsed.nome]
        print(f"""
Nome: {parsed.nome}
Preço atual: R$ {FII["Preço Atual R$"]}
Ultimo dividendo: R$ {FII["Dividendo R$"]}
            """.rstrip())
        if parsed.l:
            print(f"""
liquidez: {FII["Liquidez Diária"]}
            """.rstrip())
        elif parsed.dy:
            print(f"""
Dividend Yield %: {FII["Dividend Yield %"]}
DY (3M) Acumulado %: {FII["DY (3M) Acumulado %"]}
DY (6M) Acumulado  %: {FII["DY (6M) Acumulado  %"]}
DY (12M) Acumulado %: {FII["DY (12M) Acumulado %"]}
DY (3M) Média %: {FII["DY (3M) Média %"]}
DY (6M) Média %: {FII["DY (6M) Média %"]}
DY (12M) Média %: {FII["DY (12M) Média %"]}
DY Ano %: {FII["DY Ano %"]}
DY Patrimonial %: {FII["DY Patrimonial %"]}
            """)
        elif parsed.all:
            print(f"""
Dividend Yield : {FII["Dividend Yield %"]}%
DY (3M) Acumulado : {FII["DY (3M) Acumulado %"]}%
DY (6M) Acumulado  : {FII["DY (6M) Acumulado  %"]}%
DY (12M) Acumulado : {FII["DY (12M) Acumulado %"]}%
DY (3M) Média : {FII["DY (3M) Média %"]}%
DY (6M) Média : {FII["DY (6M) Média %"]}%
DY (12M) Média: {FII["DY (12M) Média %"]}%
DY Ano : {FII["DY Ano %"]}%
Variação Preço : {FII["Variação Preço %"]}%
Rentab Período : {FII["Rentab Período %"]}%
Rentab Acumulada : {FII["Rentab Acumulada %"]}%
Patrimônio Líq: R$ {FII["Patrimônio Líq R$"]}
VPA: R$ {FII["VPA R$"]}
P/VPA: {FII["P/VPA"]}
DY Patrimonial : {FII["DY Patrimonial %"]}%
Variação Patrimonial : {FII["Variação Patrimonial %"]}%
Rentab. Patr. no Período : {FII["Rentab. Patr. no Período %"]}%
Rentab. Patr. Acumulada : {FII["Rentab. Patr. Acumulada %"]}%
Vacância Física : {FII["Vacância Física %"]}%
Vacância financeira : {FII["Vacância financeira %"]}%
Quantidade de ativos: {FII["Quantidade de ativos"]}
            """)
    except KeyError or NameError as e:
        print("key not found, try:\n")
        for k, v in result.items():
            print(f"names: {k}")
