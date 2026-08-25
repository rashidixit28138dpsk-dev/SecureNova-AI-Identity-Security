import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
M2M_CLIENT_ID = os.getenv("M2M_CLIENT_ID")
M2M_CLIENT_SECRET = os.getenv("M2M_CLIENT_SECRET")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

CHAT_URL = "http://localhost:3000/chat"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


print(f"[{timestamp()}] Starting M2M credential rotation test")

# 1. Request M2M token
token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

token_response = requests.post(
    token_url,
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    },
    data={
        "grant_type": "client_credentials",
        "client_id": M2M_CLIENT_ID,
        "client_secret": M2M_CLIENT_SECRET,
        "audience": AUTH0_AUDIENCE,
    },
)

print(f"[{timestamp()}] Token endpoint status: {token_response.status_code}")

if token_response.status_code != 200:
    print(f"[{timestamp()}] Token request failed")
    print(token_response.text)
    raise SystemExit(1)

token_data = token_response.json()

access_token = token_data["access_token"]
expires_in = token_data.get("expires_in")

print(f"[{timestamp()}] M2M token obtained successfully")
print(f"[{timestamp()}] Token TTL reported by Auth0: {expires_in} seconds")


# 2. Use fresh token
print(f"[{timestamp()}] Calling /chat with fresh token...")

response = requests.get(
    CHAT_URL,
    headers={
        "Authorization": f"Bearer {access_token}"
    },
)

print(f"[{timestamp()}] /chat response: {response.status_code}")

if response.status_code == 200:
    print(f"[{timestamp()}] Fresh-token API call: SUCCESS")
else:
    print(f"[{timestamp()}] Fresh-token API call failed")
    print(response.text)


# 3. Wait until token expires
print(f"[{timestamp()}] Waiting 65 seconds for token expiration...")

time.sleep(65)


# 4. Replay the same token
print(f"[{timestamp()}] Replaying the expired M2M token...")

expired_response = requests.get(
    CHAT_URL,
    headers={
        "Authorization": f"Bearer {access_token}"
    },
)

print(
    f"[{timestamp()}] Expired-token /chat response: "
    f"{expired_response.status_code}"
)

if expired_response.status_code == 401:
    print(f"[{timestamp()}] EXPIRED TOKEN REJECTED: PASS")
else:
    print(f"[{timestamp()}] EXPIRED TOKEN REJECTION: UNEXPECTED")
    print(expired_response.text)