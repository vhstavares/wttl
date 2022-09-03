# Desafio Wttl
## Ativar Virtualenv 
virtualenv venv <br>
venv/Scripts/Activate
## Requirements
pip install -r requirements.txt
## Exemplo Filtro Passando Valores no GET:
init_date = 2020-11-11 <br>
finish_date = 2020-11-13 <br>
http://127.0.0.1:8000/struct_data/?init_date=2020-11-11&finish_date=2020-11-13 <br>
## Exemplo Filtro Passando Sem Valores no GET:
http://127.0.0.1:8000/struct_data/
