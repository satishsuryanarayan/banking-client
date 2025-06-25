import json
import random
from datetime import datetime, timedelta

from locust import HttpUser, task, between
from requests.models import Response


class Banker(HttpUser):
    host = "http://localhost:80/v1"
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
        with self.client.post("/transfers", json=transfer, auth=(self.username, self.password)) as response:
            print(response.status_code)

    @task(1)
    def get_transfers(self):
        account_id = random.choice(self.accounts)
        from_time = datetime.now().isoformat()
        to_time = (datetime.now() + timedelta(hours=7)).isoformat()
        with self.client.get(f"/transfers/account/{account_id}?from_time={from_time}&to_time={to_time}", name = "/transfers/account", auth=(self.username, self.password), stream=True) as response:
            for line in response.iter_lines():
                try:
                    decoded_line = line.decode('utf-8')
                    json_data = json.loads(decoded_line)
                    print(json.dumps(json_data, indent=4))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e} - Line: {line}")
                except UnicodeDecodeError as e:
                    print(f"Error decoding bytes: {e} - Line: {line}")
