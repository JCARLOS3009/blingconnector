from datetime import datetime

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def getOrders():
    API_KEY = request.args["apikey"]

    INITIAL_DATE = request.args["initialDate"]
    FINAL_DATE = datetime.now().strftime("%d/%m/%Y")

    endOfLoop = False
    result = []
    page = 1

    while endOfLoop == False:
        try:
            url = f"https://bling.com.br/Api/v2/pedidos/page={page}/json/"
            response = requests.get(
                url,
                params={
                    "apikey": API_KEY,
                    "filters": f"dataEmissao[{INITIAL_DATE} TO {FINAL_DATE}]",
                },
            )
            data = response.json()["retorno"]["pedidos"]
        except:
            print("------- ACABOU OS PEDIDOS -------")
            endOfLoop = True
            response = None

        if response != None and response.status_code == 200:
            for item in data:
                result.append(
                    {
                        "numeroPedidoLoja": item.get("pedido").get("numeroPedidoLoja"),
                        "desconto": item.get("pedido").get("desconto"),
                        "valorFrete": item.get("pedido").get("valorfrete"),
                        "nota": item.get("pedido").get("nota"),
                    }
                )
        page = page + 1
    return jsonify(result)


app.run(port=5000, host="localhost", debug=True)
