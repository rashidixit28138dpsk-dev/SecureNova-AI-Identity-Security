import os

from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.secret_key = os.urandom(24)


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ADMIN_CLIENT_ID = os.getenv("ADMIN_CLIENT_ID")
ADMIN_CLIENT_SECRET = os.getenv("ADMIN_CLIENT_SECRET")


oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=ADMIN_CLIENT_ID,
    client_secret=ADMIN_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


@app.route("/")
def home():
    user = session.get("user")

    if user:
        return f"""
        <h1>SecureNova Admin Portal</h1>
        <p>SSO authentication successful.</p>
        <p>Email: {user.get("email")}</p>
        <p>Name: {user.get("name")}</p>
        """

    return """
    <h1>SecureNova Admin Portal</h1>
    <p>You are not logged in.</p>
    <a href="/login">Login with Auth0</a>
    """


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)

    return oauth.auth0.authorize_redirect(
        redirect_uri
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()

    session["user"] = token.get("userinfo")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="localhost", port=4000, debug=True)