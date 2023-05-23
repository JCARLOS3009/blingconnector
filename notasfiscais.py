from datetime import datetime

import requests
from flask import Flask, jsonify

app = Flask(__name__)

API_KEY = "apikey"

DATA_INICIAL = "10/01/2023"
DATA_FINAL = datetime.now().strftime("%d/%m/%Y")


@app.route("/")
def produtos():
    endOfLoop = False
    result = []
    page = 1

    while endOfLoop == False:
        try:
            url = f"https://bling.com.br/Api/v2/notasfiscais/page={page}/json/?apikey={API_KEY}&filters=dataEmissao[{DATA_INICIAL} TO {DATA_FINAL}]"
            response = requests.get(url)
            data = response.json()["retorno"]["notasfiscais"]
        except:
            print("Erro na requisição")
            endOfLoop = True
            response = None

        if response != None and response.status_code == 200:
            for item in data:
                result.append(
                    {
                        "nomeCliente": item.get("notafiscal")
                        .get("cliente")
                        .get("nome"),
                        "dataEmissao": item.get("notafiscal").get("dataEmissao"),
                        "loja": item.get("notafiscal").get("loja"),
                        "valorNota": item.get("notafiscal").get("valorNota"),
                    }
                )
        page = page + 1
    return jsonify(result)


app.run()

print("------- ACABOU OS PEDIDOS -------")
