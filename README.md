# Fii_api

Esta API acessa "https://www.fundsexplorer.com.br/ranking" e gera um JSON para fácil acesso das principais informações de cada FII.


Ao rodar o arquivo fii_api.py, é possível acessar os dados localmente, utilizando flags -l
-dy ou -all para saber informações sobre liquidez e Dividend yield e um sumário com todas as informações do FII, respectivamente.
Ou rodar o arquivo flaskapp.py para criar um servidor local com Flask.

# Linha de commando:
## linux: 
python3 fii_api.py < FII > -l -all -dy  
## windows:
py fii_api.py  < FII > -l -all -dy

# Requirements:

instalar com pip3 install -r requirements.txt