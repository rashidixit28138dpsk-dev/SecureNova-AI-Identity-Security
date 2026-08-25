import os
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")

REFRESH_TOKEN = os.getenv("TEST_REFRESH_TOKEN")


def refresh(refresh_token):
    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
            "audience": AUDIENCE,
        },
        timeout=15,
    )

    return response


print("=" * 75)
print("SECURENOVA - AUTH0 REFRESH TOKEN ROTATION TEST")
print("=" * 75)

if not REFRESH_TOKEN:
    print("\nERROR: TEST_REFRESH_TOKEN is not configured.")
    print("Add a refresh token to .env before running this test.")
    raise SystemExit(1)

print("\n[STEP 1] Using original refresh token")

first = refresh(REFRESH_TOKEN)

print("HTTP Status:", first.status_code)

if first.status_code != 200:
    print("ERROR: Initial refresh-token exchange failed.")
    print(first.text)
    raise SystemExit(1)

first_data = first.json()

print("Initial refresh successful.")
print("New access token received:", "access_token" in first_data)
print("New refresh token received:", "refresh_token" in first_data)

new_refresh_token = first_data.get("refresh_token")

if not new_refresh_token:
    print("\nERROR: Auth0 did not return a rotated refresh token.")
    raise SystemExit(1)

print("\n[STEP 2] Replaying the OLD refresh token")

second = refresh(REFRESH_TOKEN)

print("HTTP Status:", second.status_code)

if second.status_code == 200:
    print("\nSECURITY TEST FAILED")
    print("OLD REFRESH TOKEN WAS ACCEPTED")
else:
    print("\nOLD REFRESH TOKEN REJECTED")
    print("Rotation protection is working.")
    print("Auth0 response:")
    print(second.text)

print("\n" + "=" * 75)