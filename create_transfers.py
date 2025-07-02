import base64
import json
import random
from datetime import datetime, timedelta

import websocket
from bank.datamodel.v1.dtos.createtransfer import CreateTransferDTO
from bank.datamodel.v1.dtos.getaccounttransfers import GetAccountTransfersDTO
from bank.protocol.message import Message


class Banker:
    def __init__(self):
        self.host = "localhost"
        self.port = "80"
        self.ws_host = "ws://localhost:80/v1/bank"
        self.num_accounts = 20000
        self.accounts = tuple(range(1, self.num_accounts + 1))
        self.username = "test_test"
        self.password = "password_password"
        self.username_password = self.username + ":" + self.password
        self.token = base64.b64encode(self.username_password.encode("utf-8"))
        self.headers = [f"Authorization: Basic {self.token}", "Content-Type: application/json",
                        "Accept: application/json"]
        self.ws = websocket.create_connection(self.ws_host, header=self.headers)

    def create_transfer(self):
        from_account = random.choice(self.accounts)
        to_account = random.choice(self.accounts)
        try:
            dto: CreateTransferDTO = CreateTransferDTO.model_validate(
                {"from_account_id": from_account, "to_account_id": to_account,
                 "amount": round(random.uniform(1.00, 5000.00), 2)})
            self.ws.send(dto.model_dump_json())
            response = self.ws.recv()
            json_data = json.loads(response)
            print(json.dumps(json_data, indent=4))
        except:
            pass

    def get_account_transfers(self):
        account_id = random.choice(self.accounts)
        from_time = datetime.now().isoformat()
        to_time = (datetime.now() + timedelta(hours=7)).isoformat()
        dto: GetAccountTransfersDTO = GetAccountTransfersDTO.model_validate(
            {"account_id": account_id, "from_time": from_time, "to_time": to_time})
        self.ws.send(dto.model_dump_json())
        response = self.ws.recv()
        while response != Message.END:
            print(response)
            response = self.ws.recv()


if __name__ == "__main__":
    banker = Banker()
    while True:
        banker.create_transfer()
        banker.get_account_transfers()
