from collections import OrderedDict
import requests as req
import argparse
import json
from os.path import exists


def save_json():
    url = r'https://statusinvest.com.br/category/advancedsearchresult?search={"Segment":"","Gestao":"","my_range":"0;20","dy":{"Item1":null,"Item2":null},"p_vp":{"Item1":null,"Item2":null},"percentualcaixa":{"Item1":null,"Item2":null},"numerocotistas":{"Item1":null,"Item2":null},"dividend_cagr":{"Item1":null,"Item2":null},"cota_cagr":{"Item1":null,"Item2":null},"liquidezmediadiaria":{"Item1":null,"Item2":null},"patrimonio":{"Item1":null,"Item2":null},"valorpatrimonialcota":{"Item1":null,"Item2":null},"numerocotas":{"Item1":null,"Item2":null},"lastdividend":{"Item1":null,"Item2":null}}&CategoryType=2'

    get = req.request(
        "get", url, headers={
            "User-Agent": r"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Referer": r"https://statusinvest.com.br/fundos-imobiliarios/busca-avancada"
        }
    ).json()
    json_dict = OrderedDict()
    # dict.update({[items for items in get]})
    for items in get:
        json_dict.update({str(items["ticker"]): items})
        # print("{}:{}".format(items["ticker"], items))
    return json_dict


if __name__ == "__main__":
    if not exists("fiis.json"):
        print("baixando JSON de todos os FIIs")
        with open("fiis.json", "w") as file:
            json.dump(save_json(), file)
    fiis_str = open("fiis.json", "r")
    result = json.load(fiis_str)  # parsed JSON

    parser = argparse.ArgumentParser(
        description="Bem vindo ao menu de ajuda, aqui você encontra todos os possíveis comandos que podem ser executados",
        usage="py (ou python3) fii_api.py [-h] [-l](liquidez) [-dy](dividend yield) nome do FII"
    )  # Argument Parser object

    # adding necessary arg
    parser.add_argument(
        "-force", help="Força a atualização do arquivo", action="store_true")
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
        FII = result[parsed.nome]  # Nome do FII atual
        print(f"""
Nome: {parsed.nome}
Preço atual: R$ {FII["price"]}
Ultimo dividendo: R$ {FII["lastdividend"]}
            """.rstrip())
        if parsed.force:
            print("Atualizando JSON local")
            with open("fiis.json", "w") as file:
                json.dump(save_json(), file)
        elif parsed.l:
            print(f"""
liquidez: {FII["liquidezmediadiaria"]}
            """.rstrip())

        elif parsed.dy:
            print(f"""
Dividend Yield %: {FII["dy"]}
            """)
        elif parsed.all:
            print(f"""
Nome da adm.: {FII["companyName"]}
Dividend Yield : {FII["dy"]}%
Preço atual: R$ {FII["price"]}
Tipo de gestão: {FII["gestao"]}
P/VP: {FII["p_vp"]}
Valor patrimonial p/ cota: {FII["valorpatrimonialcota"]}
Liq. méd. diária: {FII["liquidezmediadiaria"]}
% em caixa: {FII["percentualcaixa"]}
Dividendo CAGR (3 anos): {FII["dividend_cagr"]}
Valor CAGR: {FII["cota_cagr"]}
Numero de cotistas: {FII["numerocotistas"]}
Numero de cotas: {FII["numerocotas"]}
Patrimonio: {FII["patrimonio"]}
Ulimo rendimento: {FII["lastdividend"]}
            """)

    except (KeyError, NameError) as e:
        print("key not found, try:\n")
        for k, v in result.items():
            print(f"names: {k}")
    fiis_str.close()
else:
    if not exists("fiis.json"):
        print("baixando JSON de todos os FIIs")
        with open("fiis.json", "w") as file:
            json.dump(save_json(), file)
    fiis_str = open("fiis.json", "r")
    result = json.load(fiis_str)  # parsed JSON
