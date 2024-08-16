
from collections import OrderedDict
import requests as req
import argparse
import json
from os.path import exists


def get_data(full=False) -> OrderedDict:
    url = r'https://statusinvest.com.br/category/advancedsearchresultpaginated?search=%7B%22Segment%22%3A%22%22%2C%22Gestao%22%3A%22%22%2C%22my_range%22%3A%220%3B20%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_vp%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22percentualcaixa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22numerocotistas%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividend_cagr%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22cota_cagr%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezmediadiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22patrimonio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorpatrimonialcota%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22numerocotas%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lastdividend%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&orderColumn=&isAsc=&page=0&take=566&CategoryType=2'

    get = req.request(
        "get", url, headers={
            "User-Agent": r"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Referer": r"https://statusinvest.com.br/fundos-imobiliarios/busca-avancada"
        }
    ).json()
    json_dict = OrderedDict()
    if not full:
        for item in get["list"]:
            json_dict.update({str(item["ticker"]): item})
    else:
        for item in get:
            json_dict.update({str(item): get[item]})
    return json_dict


if __name__ == "__main__":
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

    if not exists("fiis.json") or parsed.force:
        print("baixando JSON de todos os FIIs")
        with open("fiis.json", "w") as file:
            json.dump(get_data(), file)
    fiis_str = open("fiis.json", "r")
    result = json.load(fiis_str)  # parsed JSON

    try:
        FII = result[parsed.nome]  # Nome do FII atual
        # basic info
        print(f"""
            Nome: {parsed.nome}\nPreço atual: R$ {FII["price"]}\nÚltimo dividendo: R$ {FII["lastdividend"]}""".strip())

        # handling special flags
        if parsed.l:
            print(f"""Liquidez (R$): {FII["liquidezmediadiaria"]}""".strip())
        elif parsed.dy:
            print(f"""Dividend Yield %: {FII["dy"]}""")
        elif parsed.all:
            print(f"""Nome da adm.: {FII["companyname"]}\nDividend Yield : {FII["dy"]}%\nPreço atual: R$ {FII["price"]}\nTipo de gestão: {FII["gestao_f"]}\nP/VP: {FII["p_vp"]}\nValor patrimonial p/ cota: {FII["valorpatrimonialcota"]}\nLiq. méd. diária: {FII["liquidezmediadiaria"]}\n% em caixa: {FII["percentualcaixa"]}\nDividendo CAGR (3 anos): {FII["dividend_cagr"]}\nValor CAGR: {FII["cota_cagr"]}\nNumero de cotistas: {FII["numerocotistas"]}\nNumero de cotas: {FII["numerocotas"]}\nPatrimonio: {FII["patrimonio"]}\nUlimo rendimento: {FII["lastdividend"]}""")

    except (KeyError, NameError) as e:
        print(f"error ({e}) key not found, try:\n")
        for k, v in result.items():
            print(f"names: {k}")
    fiis_str.close()
else:
    get_data(True)
