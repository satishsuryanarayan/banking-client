import base64
import json
import random

import requests
import websocket
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry

from dtos.createaccountdto import CreateAccountDTO
from dtos.createcustomerdto import CreateCustomerDTO

num_accounts = 20000

retry_strategy = Retry(
    total=10,
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
username = "test_test"
password = "password_password"
host = "localhost"
port = "80"


def run():
    with requests.session() as session:
        basic = HTTPBasicAuth(f"{username}", f"{password}")
        session.mount("http://", adapter)
        session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        json_data = json.dumps(
            {"user": {"username": f"{username}", "password": f"{password}", "email": "name@domain.com"}})
        print(json_data)
        response = session.post(f"http://{host}:{port}/v1/users", data=json_data)
        data = response.json()
        print(json.dumps(data))

        ws_host = "ws://localhost:80/v1/bank"
        up_bytes = (username + ":" + password).encode("utf-8")
        token = base64.b64encode(up_bytes)
        headers = {"Authorization": f"Basic {token}"}
        with websocket.create_connection(ws_host, headers=headers) as ws:
            dto: CreateCustomerDTO = CreateCustomerDTO.model_validate({"name": "test_customer"})
            ws.send(json.dumps(dto))
            response = ws.recv()
            json_data = json.loads(response)
            print(json.dumps(json_data, indent=4))
            customer_id = json_data["id"]
            for i in range(1, num_accounts + 1):
                dto: CreateAccountDTO = CreateAccountDTO.model_validate(
                    {"customer_id": customer_id, "amount": round(random.uniform(50000.00, 9999999999.99), 2)})
                ws.send(json.dumps(dto))
                response = ws.recv()
                json_data = json.loads(response)
                print(json.dumps(json_data, indent=4))

    print("Created " + str(num_accounts) + " accounts")


if __name__ == "__main__":
    run()
