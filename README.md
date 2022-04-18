# Bem vindo à Fii_api

Esta API acessa o site [StatusInvest](https://statusinvest.com.br/fundos-imobiliarios/busca-avancada) e gera um JSON para fácil acesso das principais informações de cada FII.

Ao rodar o arquivo fii_api.py, é possível acessar os dados localmente, utilizando flags -l
-dy ou -all para saber informações sobre liquidez e Dividend yield e um sumário com todas as informações do FII, respectivamente.
fii_api.py salva um JSON localmente para tornar a análise mais rápida

# Por que?????

Para praticar minhas habilidades com manipulação JSON e para ver informações sobre FIIs

# Data Science

Uso o ds/datascience.py para visualizar dados dos FIIs. Para mais infos, vá para o [README](https://github.com/PedroMarquetti/fii_api/blob/main/ds/README.md)

# Linha de commando:

## linux:

`python3 fii_api.py < FII > -l -all -dy`

## windows:

`py fii_api.py < FII > -l -all -dy`

# Requirements:

instalar com pip3 install -r requirements.txt
