
from collections import OrderedDict
import requests as req
import argparse
import json
import traceback
import sys
from os.path import exists


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_data(full=False) -> OrderedDict:
    url = r'https://statusinvest.com.br/category/advancedsearchresultpaginated?search=%7B%22Segment%22%3A%22%22%2C%22Gestao%22%3A%22%22%2C%22my_range%22%3A%220%3B20%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_vp%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22percentualcaixa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22numerocotistas%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividend_cagr%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22cota_cagr%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezmediadiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22patrimonio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorpatrimonialcota%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22numerocotas%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lastdividend%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&orderColumn=&isAsc=&page=0&take=566&CategoryType=2'
    try:
        get = req.request(
            "get", url, headers={
                "User-Agent": r"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
                "Accept": r"text/html, application/xhtml+xml, application/xml q = 0.9, image/avif, image/webp, mage/png, image/svg+xml, */* q = 0.8",
                "Referer": r"https://statusinvest.com.br/fundos-imobiliarios/busca-avancada",
                "Host": r"statusinvest.com.br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "TE": "trailers",
                "Priority": "u = 4",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            }
        )
        json = get.json()
        json_dict = OrderedDict()
        if not full:
            for item in json["list"]:
                json_dict.update({str(item["ticker"]): item})
        else:
            for item in json:
                json_dict.update({str(item): json[item]})
        return json_dict
    except Exception as e:
        print_err(f"error in get_data {e}")
        traceback.print_exc()
        sys.exit(4)


if __name__ == "__main__":
    # user is running this script directly
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
        # if user hasn't downloaded the file OR has asked to force download, save the file
        try:
            with open("fiis.json", "w") as file:
                data = get_data()
                print("baixando JSON de todos os FIIs")
                json.dump(data, file)
        except (Exception, json.JSONDecodeError) as e:
            print_err(
                f"error ({e}) occurred while trying to open fiis.json / running get_data()")
            sys.exit(1)

    try:
        fiis_str = open("fiis.json", "r")
        result = json.load(fiis_str)  # parsed JSON

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
        print(f"error {e}", sys.stderr)
        print("try:\n")
        for k, v in result.items():
            print(f"names: {k}")
        sys.exit(2)
    except (Exception)as e:
        print_err(f"error {e}")
        sys.exit(3)

    fiis_str.close()
else:
    # user is running from somewhere else, exposing get_data
    get_data(True)
