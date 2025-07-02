import base64
import json
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import websocket
import requests

from dtos.createaccountdto import CreateAccountDTO
from dtos.createcustomerdto import CreateCustomerDTO
from dtos.registeruserdto import RegisterUserDTO


class Banker:
    def __init__(self):
        self.host = "localhost"
        self.port = "80"
        self.ws_host = "ws://localhost:80/v1/bank"
        self.num_accounts = 500
        self.accounts = tuple(range(1, self.num_accounts + 1))
        self.username = "test_test"
        self.password = "password_password"
        self.username_password = self.username + ":" + self.password
        self.token = base64.b64encode(self.username_password.encode("utf-8"))
        self.headers = [f"Authorization: Basic {self.token}", "Content-Type: application/json",
                        "Accept: application/json"]
        self.register_user()
        self.ws = websocket.create_connection(self.ws_host, header=self.headers)

    def register_user(self):
        retry_strategy = Retry(
            total=10,
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        with requests.session() as session:
            session.mount("http://", adapter)
            session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
            dto: RegisterUserDTO = RegisterUserDTO(username=self.username, password=self.password, email="name@domain.com")
            json_data = json.dumps(
                {"param": dto.model_dump()})
            print(json_data)
            response = session.post(f"http://{self.host}:{self.port}/v1/users", data=json_data)
            data = response.json()
            print(json.dumps(data))

    def _create_customer(self) -> int:
        dto: CreateCustomerDTO = CreateCustomerDTO.model_validate({"name": "test_customer"})
        self.ws.send(dto.model_dump_json())
        response = self.ws.recv()
        print(response)
        json_data = json.loads(response)
        print(json.dumps(json_data, indent=4))
        return json_data["id"]

    def create_accounts(self):
        customer_id: int = self._create_customer()
        for i in range(1, self.num_accounts + 1):
            dto: CreateAccountDTO = CreateAccountDTO.model_validate(
                {"customer_id": customer_id, "amount": round(random.uniform(50000.00, 9999999999.99), 2)})
            self.ws.send(dto.model_dump_json())
            response = self.ws.recv()
            json_data = json.loads(response)
            print(json.dumps(json_data, indent=4))


if __name__ == "__main__":
    banker = Banker()
    banker.create_accounts()
