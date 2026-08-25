import os
import jwt
import requests

from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

app = Flask(__name__)

# Secret used by Flask to protect the session
app.secret_key = os.urandom(24)

# Auth0 configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")


# Configure OAuth
oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email read:ai-data",
        "audience": AUTH0_AUDIENCE,
        "code_challenge_method": "S256",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


@app.route("/")
def home():
    return """
    <h1>SecureNova AI Customer Service</h1>
    <p>Auth0 authentication is being configured.</p>
    <a href="/login">Login with Auth0</a>
    """


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)

    return oauth.auth0.authorize_redirect(
        redirect_uri,
        audience=AUTH0_AUDIENCE,
        scope="openid profile email offline_access read:ai-data",
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    

   


    access_token = token.get("access_token")
    

    try:
        access_payload = jwt.decode(
            access_token,
            options={"verify_signature": False}
        )
        
        print(access_payload)
    except Exception as e:
        print("ACCESS TOKEN DECODE ERROR:", str(e))
        if not access_token:
            return "Login succeeded, but no access token was returned.", 500

    # Safely inspect the access-token header.
    # This does NOT print the actual token.
    try:
        token_header = jwt.get_unverified_header(access_token)
        print("ACCESS TOKEN HEADER:", token_header)
    except Exception as e:
        print("ACCESS TOKEN HEADER ERROR:", str(e))

    print("TOKEN TYPE:", token.get("token_type"))
    print("TOKEN KEYS:", list(token.keys()))

    session["user"] = token.get("userinfo")
    session["access_token"] = access_token

    if token.get("refresh_token"):
        session["refresh_token"] = token.get("refresh_token")
    

    return redirect(url_for("profile"))


@app.route("/profile")
def profile():
    user = session.get("user")

    if not user:
        return redirect(url_for("login"))

    return f"""
    <h1>Welcome to SecureNova</h1>
    <p>You successfully authenticated with Auth0.</p>
    <p>Email: {user.get("email")}</p>
    <p>Name: {user.get("name")}</p>
    """
def verify_access_token(token):
    """
    Verify an Auth0 RS256 access token using Auth0 JWKS.
    """

    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

    jwks_client = jwt.PyJWKClient(jwks_url)

    signing_key = jwks_client.get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=AUTH0_AUDIENCE,
        issuer=f"https://{AUTH0_DOMAIN}/",
    )

    return payload
@app.route("/chat")
def chat():
    token = session.get("access_token")

    if not token:
        return "Unauthorized: Please login first.", 401

    try:
        payload = verify_access_token(token)

        scopes = payload.get("scope", "").split()

        if "read:ai-data" not in scopes:
            return "Forbidden: read:ai-data scope required.", 403

        return f"""
        <h1>SecureNova AI Chat API</h1>
        <p>Access granted.</p>
        <p>Required scope: read:ai-data</p>
        <p>Your scopes: {payload.get("scope")}</p>
        """

    except Exception as e:
        return f"Unauthorized: {str(e)}", 401
@app.route("/admin")
def admin():
    token = session.get("access_token")

    if not token:
        return "Unauthorized: Please login first.", 401

    try:
        payload = verify_access_token(token)

        scopes = payload.get("scope", "").split()

        if "write:admin" not in scopes:
            return "Forbidden: write:admin scope required.", 403

        return """
        <h1>SecureNova Admin API</h1>
        <p>Administrative access granted.</p>
        """

    except Exception as e:
        return f"Unauthorized: {str(e)}", 401

@app.route("/test-refresh-rotation")
def test_refresh_rotation():

    refresh_token = session.get("refresh_token")

    if not refresh_token:
        return """
        <h2>Refresh Token Rotation Test</h2>
        <p>ERROR: No refresh token in session.</p>
        <p>Please log in again.</p>
        """

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }

    print("=" * 70)
    print("SECURENOVA - AUTH0 REFRESH TOKEN ROTATION TEST")
    print("=" * 70)

    print("\n[STEP 1] Using original refresh token")

    first = requests.post(
        token_url,
        json=payload,
        timeout=15
    )

    print("HTTP STATUS:", first.status_code)

    if first.status_code != 200:
        print("ERROR: Initial refresh failed.")
        print("Response:", first.text)
        return "Initial refresh failed. Check terminal."

    first_data = first.json()

    print("Initial refresh successful.")
    print("New access token received:",
          bool(first_data.get("access_token")))
    print("New refresh token received:",
          bool(first_data.get("refresh_token")))

    print("\n[STEP 2] Replaying OLD refresh token")

    second = requests.post(
        token_url,
        json=payload,
        timeout=15
    )

    print("HTTP STATUS:", second.status_code)

    if second.status_code == 200:
        print("\nSECURITY TEST FAILED")
        print("OLD REFRESH TOKEN WAS ACCEPTED")

        return """
        <h2>SECURITY TEST FAILED</h2>
        <p>Old refresh token was accepted.</p>
        """

    print("\nOLD REFRESH TOKEN REJECTED")
    print("Rotation protection is working.")
    print("STATUS: REJECTED")

    return """
    <h2>Refresh Token Rotation Test</h2>
    <p>Old refresh token rejected.</p>
    <p>Rotation protection is working.</p>
    <p><b>STATUS: REJECTED</b></p>
    """

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)