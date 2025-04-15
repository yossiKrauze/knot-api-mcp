import requests
import base64
import json

# Test the merchant list API
def test_merchant_list():
    url = "http://127.0.0.1:8002/merchant/list"
    
    payload = {
        "type": "card_switcher",
        "platform": "ios",
        "user_agent": "test-agent",
        "search": "",
        "external_user_id": "test-user-123",
        "status": "active"
    }
    
    # Create a Basic Auth header with a dummy value
    auth_string = "username:password"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }
    
    print(f"Sending request to {url}")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response

if __name__ == "__main__":
    test_merchant_list()
