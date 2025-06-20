import random
from datetime import datetime, timedelta

from locust import HttpUser, task, between


class Banker(HttpUser):
    host = "http://localhost:8000/v1"
    num_accounts = 20000
    accounts = tuple(range(1, num_accounts + 1))
    username = "test_test"
    password = "password_password"
    wait_time = between(30, 120)

    @task(3)
    def transfer(self):
        from_account = random.choice(self.accounts)
        to_account = random.choice(self.accounts)
        transfer = {"transfer": {"from_account_id": from_account, "to_account_id": to_account,
                                 "amount": round(random.uniform(1.00, 5000.00), 2)}}
        self.client.post("/transfers", json=transfer, auth=(self.username, self.password))

    @task(1)
    def get_transfers(self):
        account_id = random.choice(self.accounts)
        from_time = (datetime.now() - timedelta(hours=1)).isoformat()
        to_time = datetime.now().isoformat()
        self.client.get(f"/transfers/account/{account_id}?from_time={from_time}&to_time={to_time}", name = "/transfers/account", auth=(self.username, self.password), stream=True)