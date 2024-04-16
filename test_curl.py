import requests


def send_data_to_server(data):
    url = 'http://backend-server-url.com'  # Replace with your backend server URL
    headers = {'Content-Type': 'application/json'}  # Adjust headers as needed

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP errors (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error sending data to server:", e)
        return None

def test_backend_server():
    # Example data to send to the server
    data = {
        'key1': 'value1',
        'key2': 'value2'
    }

    # Sending data to the server
    print("Sending data to the server...")
    response_data = send_data_to_server(data)

    if response_data:
        # Assuming the server responds with JSON data
        print("Response from server:", response_data)
        # Test the response data here
        # For example, check if a specific key exists in the response
        if 'key_in_response' in response_data:
            print("Test passed: Key found in the response.")
        else:
            print("Test failed: Key not found in the response.")
    else:
        print("Failed to receive response from the server.")


def main():
    """
    curl https://smoq.bieda.it/change_item --data '{"item_id": 1, "what_to_change": {"amount": 2, "value": 10.5}, "key": "asdf"}' -H "Content-type: application/json" 
    curl https://smoq.bieda.it/change_item --data '{"item_id": 1, "what_to_change": ["amount", "value"], "key": "asdf"}' -H "Content-type: application/json"
    curl https://smoq.bieda.it/add_item --data '{"produkt_name": "ddassanazwaasd_asddsaadasprod", "produkty_id": "266434", "value": 14.12, "amount": "0", "typ": "fig"}' -H "Content-type: application/json"
    curl https://smoq.bieda.it/adduser --data '{"name":"", "email": "sas", "username": "sas", "password": "p"}' -H "Content-type: application/json"
    curl https://smoq.bieda.it/login --data '{"email": "s", "username": "s", "password": "p"}' -H "Content-type: application/json"
    curl https://smoq.bieda.it/find_item --data '{"item_id": 1}' -H "Content-type: application/json"
    """

if __name__ == "__main__":
    main()

