import json
import random
from datetime import datetime, timedelta

import base64
import websocket
from locust import User, task, between

from dtos.createtransferdto import CreateTransferDTO
from dtos.getaccounttransfersdto import GetAccountTransfersDTO


class Banker(User):
    ws_host = "ws://localhost:80/v1/bank"
    num_accounts = 20000
    accounts = tuple(range(1, num_accounts + 1))
    username = "test_test"
    password = "password_password"
    wait_time = between(30, 120)
    ws = None

    def on_start(self):
        username_password = self.username + ":" + self.password
        token = base64.b64encode(username_password.encode("utf-8"))
        headers = [f"Authorization: Basic {token}"]
        self.ws = websocket.create_connection(self.ws_host, header=headers)

    def on_stop(self):
        self.ws.close()

    @task(3)
    def transfer(self):
        from_account = random.choice(self.accounts)
        to_account = random.choice(self.accounts)
        dto: CreateTransferDTO = CreateTransferDTO.model_validate({"from_account_id": from_account, "to_account_id": to_account,
                                 "amount": round(random.uniform(1.00, 5000.00), 2)})
        self.ws.send(dto.model_dump_json())
        response = self.ws.recv()
        json_data = json.loads(response)
        print(json.dumps(json_data, indent=4))

    @task(1)
    def get_transfers(self):
        account_id = random.choice(self.accounts)
        from_time = datetime.now().isoformat()
        to_time = (datetime.now() + timedelta(hours=7)).isoformat()
        dto: GetAccountTransfersDTO = GetAccountTransfersDTO.model_validate({"account_id": account_id, from_time: from_time, to_time: to_time,})
        self.ws.send(dto.model_dump_json())
        response = self.ws.recv()
        json_data = json.loads(response)
        print(json.dumps(json_data, indent=4))
