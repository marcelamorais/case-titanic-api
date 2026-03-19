import json
import os
import uuid
import pickle
import traceback
from decimal import Decimal

import boto3
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=str)
    }


def to_decimal(value):
    return Decimal(str(value))


def parse_body(event):
    body = event.get("body")

    if not body:
        return {}

    if isinstance(body, str):
        return json.loads(body)

    return body


def normalize_path(path):
    if not path:
        return ""

    if path.startswith("/dev/"):
        return path[4:]

    if path == "/dev":
        return "/"

    return path


def score_passageiros(data):
    resultados = []

    for passageiro in data:
        print("PASSAGEIRO RECEBIDO:", passageiro)

        features = np.array(passageiro, dtype=float).reshape(1, -1)
        print("FEATURES FORMATADAS:", features.tolist())

        prob = float(model.predict_proba(features)[0][1])
        print("PROBABILIDADE:", prob)

        passenger_id = str(uuid.uuid4())

        item = {
            "id": passenger_id,
            "features": [to_decimal(x) for x in passageiro],
            "probabilidade": to_decimal(prob)
        }

        print("ITEM DYNAMODB:", item)
        table.put_item(Item=item)

        resultados.append({
            "id": passenger_id,
            "probabilidade": prob
        })

    return resultados


def list_passageiros():
    result = table.scan()
    items = result.get("Items", [])

    return [
        {
            "id": item["id"],
            "probabilidade": float(item["probabilidade"])
        }
        for item in items
    ]


def get_passageiro(passenger_id):
    result = table.get_item(Key={"id": passenger_id})
    item = result.get("Item")

    if not item:
        return None

    return {
        "id": item["id"],
        "probabilidade": float(item["probabilidade"])
    }


def delete_passageiro(passenger_id):
    result = table.get_item(Key={"id": passenger_id})

    if "Item" not in result:
        return False

    table.delete_item(Key={"id": passenger_id})
    return True


def extract_id_from_path(path, path_params):
    if path_params and path_params.get("id"):
        return path_params["id"]

    parts = path.strip("/").split("/")
    if len(parts) == 2 and parts[0] == "sobreviventes":
        return parts[1]

    return None


def lambda_handler(event, context):
    try:
        print("EVENTO COMPLETO:", json.dumps(event))

        method = event.get("requestContext", {}).get("http", {}).get("method", "")
        raw_path = event.get("rawPath", "")
        path = normalize_path(raw_path)
        path_params = event.get("pathParameters") or {}

        print("METHOD:", method)
        print("RAW_PATH:", raw_path)
        print("NORMALIZED_PATH:", path)
        print("PATH PARAMS:", path_params)

        if method == "POST" and path == "/sobreviventes":
            body = parse_body(event)
            print("BODY PARSING:", body)

            data = body.get("data", [])
            print("DATA:", data)

            if not isinstance(data, list) or len(data) == 0:
                return build_response(400, {
                    "erro": "O campo 'data' deve ser uma lista não vazia."
                })

            resultados = score_passageiros(data)
            return build_response(200, resultados)

        if method == "GET" and path == "/sobreviventes":
            return build_response(200, list_passageiros())

        passenger_id = extract_id_from_path(path, path_params)

        if method == "GET" and passenger_id:
            item = get_passageiro(passenger_id)

            if not item:
                return build_response(404, {"erro": "Passageiro não encontrado"})

            return build_response(200, item)

        if method == "DELETE" and passenger_id:
            deleted = delete_passageiro(passenger_id)

            if not deleted:
                return build_response(404, {"erro": "Passageiro não encontrado"})

            return build_response(200, {"mensagem": "Passageiro deletado com sucesso"})

        return build_response(404, {
            "erro": "Rota não encontrada",
            "method": method,
            "raw_path": raw_path,
            "normalized_path": path
        })

    except Exception as e:
        print("ERRO DETALHADO:", str(e))
        print(traceback.format_exc())
        return build_response(500, {
            "erro": str(e),
            "trace": traceback.format_exc()
        })