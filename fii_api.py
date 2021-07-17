from collections import OrderedDict
import requests as req
from bs4 import BeautifulSoup as bs
import argparse


def main():
    """main function, scrapes the URL and returns a ordered dictionary"""
    agent = { #setting user-agent
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    URL = r"https://www.fundsexplorer.com.br/ranking" #target URL
    s = req.Session() 
    get = s.request("get",URL,headers=agent) # sending GET request with Session
    soup = bs(get.text,"lxml")
    tr = soup.find_all("tr")[1:] # BeautifulSoup finds all <tr> tags
    result = OrderedDict()
    for items in tr: 
        td = items.find_all("td") # finding <td> inside <tr>

        result.update({td[0].getText(): # creating Ordered Dict ({FII:{info...}})
            {
                "Setor":td[1].getText(),
                "Preço Atual":td[2].getText(),
                "Liquidez Diária":td[3].getText(),
                "Dividendo":td[4].getText(),
                "Dividend Yield":td[5].getText(),
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
    result = main() # dic obj 
    parser = argparse.ArgumentParser(
        description="Bem vindo ao menu de ajuda, aqui você encontra todos os possíveis comandos que podem ser executados",
        usage="Como utilizar: py (ou python3) fii_api.py [-h] [-l](liquidez) [-dy](dividend yield) nome do FII"
        ) # Argument Parser object
    parser.add_argument("nome",help="nome do fii (XXXX11)") # adding necessary arg
    parser.add_argument("-l",help="Mostra a liquidez do FII",action="store_true") #optional arg
    parser.add_argument("-dy",help="Mostra informações sobre o Dividend Yield do FII",action="store_true")
    parser.add_argument("-all",help="Mostra todas as informações do FII",action="store_true") #optional arg

    parsed = parser.parse_args()
    try:
        print(
        f"""
Nome: {parsed.nome}
Preço atual: {result[parsed.nome]["Preço Atual"]},
Último rendimento: {result[parsed.nome]["Dividendo"]},
        """)
        if parsed.l: # liquidez
            print(
        f"""
Liquidez Diária: {result[parsed.nome]["Liquidez Diária"]}""")
        elif parsed.dy:
            print(f"""
Dividend Yield: {result[parsed.nome]["Dividend Yield"]}
DY (3M) Acumulado: {result[parsed.nome]["DY (3M) Acumulado"]}
DY (6M) Acumulado: {result[parsed.nome]["DY (6M) Acumulado"]}
DY (12M) Acumulado: {result[parsed.nome]["DY (12M) Acumulado"]}
DY (3M) Média: {result[parsed.nome]["DY (3M) Média"]}
DY (6M) Média: {result[parsed.nome]["DY (6M) Média"]}
DY (12M) Média: {result[parsed.nome]["DY (12M) Média"]}
DY Ano: {result[parsed.nome]["DY Ano"]}
        """
            )
        elif parsed.all:
            print(f"""
Setor: {result[parsed.nome]["Setor"]}
Preço Atual: {result[parsed.nome]["Preço Atual"]}
Liquidez Diária: {result[parsed.nome]["Liquidez Diária"]}
Dividendo: {result[parsed.nome]["Dividendo"]}
Dividend Yield: {result[parsed.nome]["Dividend Yield"]}
DY (3M) Acumulado: {result[parsed.nome]["DY (3M) Acumulado"]}
DY (6M) Acumulado: {result[parsed.nome]["DY (6M) Acumulado"]}
DY (12M) Acumulado: {result[parsed.nome]["DY (12M) Acumulado"]}
DY (3M) Média: {result[parsed.nome]["DY (3M) Média"]}
DY (6M) Média: {result[parsed.nome]["DY (6M) Média"]}
DY (12M) Média: {result[parsed.nome]["DY (12M) Média"]}
DY Ano: {result[parsed.nome]["DY Ano"]}
Variação Preço: {result[parsed.nome]["Variação Preço"]}
Rentab Período: {result[parsed.nome]["Rentab Período"]}
Rentab Acumulada: {result[parsed.nome]["Rentab Acumulada"]}
Patrimônio Líq: {result[parsed.nome]["Patrimônio Líq"]}
VPA: {result[parsed.nome]["VPA"]}
P/VPA: {result[parsed.nome]["P/VPA"]}
DY Patrimonial: {result[parsed.nome]["DY Patrimonial"]}
Variação Patrimonial: {result[parsed.nome]["Variação Patrimonial"]}
Rentab. Patr. no Período: {result[parsed.nome]["Rentab. Patr. no Período"]}
Rentab. Patr. Acumulada: {result[parsed.nome]["Rentab. Patr. Acumulada"]}
Vacância Física: {result[parsed.nome]["Vacância Física"]}
Vacância financeira: {result[parsed.nome]["Vacância financeira"]}
Quantidade de ativos: {result[parsed.nome]["Quantidade de ativos"]}
"""
            )
            
    except KeyError or NameError as e:
        print("key not found, try:\n")
        for k,v in result.items():
            print(f"names: {k}")
    