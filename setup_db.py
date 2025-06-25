import json
import random
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry

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
        json_data = json.dumps({"user": {"username": f"{username}", "password": f"{password}", "email": "name@domain.com"}})
        print(json_data)
        response = session.post(f"http://{host}:{port}/v1/users", data=json_data)
        data = response.json()
        print(json.dumps(data))
        json_data = json.dumps({"customer": {"name": "test_customer"}})
        response = session.post(f"http://{host}:{port}/v1/customers", auth=basic, data=json_data)
        data = response.json()
        print(json.dumps(data, indent=4))
        customer_id = data["id"]
        response.close()
        for i in range(1, num_accounts + 1):
            data = {"account": {"customer_id": customer_id, "amount": round(random.uniform(50000.00, 9999999999.99), 2)}}
            json_data = json.dumps(data)
            response = session.post(f"http://{host}:{port}/v1/accounts", auth=basic, data=json_data)
            response.close()
   
    print("Created " + str(num_accounts) + " accounts")
if __name__ == "__main__":
    run()
