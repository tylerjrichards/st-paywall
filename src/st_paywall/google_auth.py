import asyncio
import uuid
import jwt
import streamlit as st
from typing import Optional
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

# Mock database for storing session information
user_sessions_db = {}

# Configuration for Google OAuth client
testing_mode = st.secrets.get("testing_mode", False)
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_url = (
    st.secrets["redirect_url_test"] if testing_mode else st.secrets["redirect_url"]
)
client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)

# Decode JWT token
def decode_user(token: str):
    decoded_data = jwt.decode(jwt=token, options={"verify_signature": False})
    return decoded_data

# Get authorization URL
async def get_authorization_url(client: GoogleOAuth2, redirect_url: str) -> str:
    authorization_url = await client.get_authorization_url(
        redirect_url,
        scope=["email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url

# Markdown button for login
def markdown_button(url: str, text: Optional[str] = None, color="#FD504D", sidebar: bool = True):
    markdown = st.sidebar.markdown if sidebar else st.markdown
    markdown(
        f"""
        <a href="{url}" target="_blank">
            <div style="
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-weight: 400;
                padding: 0.25rem 0.75rem;
                border-radius: 0.25rem;
                margin: 0px;
                line-height: 1.6;
                width: auto;
                user-select: none;
                background-color: {color};
                color: rgb(255, 255, 255);
                border: 1px solid rgb(255, 75, 75);
                text-decoration: none;
                ">
                {text}
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

# Get access token
async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str) -> OAuth2Token:
    token = await client.get_access_token(code, redirect_url)
    return token

# Get access token from query parameters
def get_access_token_from_query_params(client: GoogleOAuth2, redirect_url: str) -> OAuth2Token:
    query_params = st.experimental_get_query_params()
    code = query_params["code"][0]
    token = asyncio.run(
        get_access_token(client=client, redirect_url=redirect_url, code=code)
    )
    st.experimental_set_query_params()
    return token

# Show login button
def show_login_button(text: Optional[str] = "Login with Google", color="#FD504D", sidebar: bool = True):
    authorization_url = asyncio.run(
        get_authorization_url(client=client, redirect_url=redirect_url)
    )
    markdown_button(authorization_url, text, color, sidebar)

# Generate a unique session hash
def generate_user_session_hash():
    return uuid.uuid4().hex

# Store session information in the mock database
def store_user_session(email, session_hash):
    user_sessions_db[session_hash] = email

# Validate the user session
def validate_user_session(session_hash):
    return user_sessions_db.get(session_hash)

# JavaScript code to set a cookie
def set_cookie_js(hash):
    js = f"""
    <script>
    document.cookie = "session={hash}; path=/; expires=Fri, 31 Dec 9999 23:59:59 GMT";
    </script>
    """
    st.components.v1.html(js, height=0, width=0)

# JavaScript code to get a cookie
def get_cookie_js():
    js = """
    <script>
    var cookie_value = "";
    var name = "session=";
    var decoded_cookie = decodeURIComponent(document.cookie);
    var ca = decoded_cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            cookie_value = c.substring(name.length, c.length);
            break;
        }
    }
    window.location.href = window.location.href.split("?")[0] + "?session=" + cookie_value;
    </script>
    """
    st.components.v1.html(js, height=0, width=0)

# Get the cookie from the query params
def get_cookie_from_query_params():
    query_params = st.experimental_get_query_params()
    return query_params.get("session", [None])[0]

# Get logged in user email
def get_logged_in_user_email() -> Optional[str]:
    session_hash = get_cookie_from_query_params()

    if session_hash:
        user_email = validate_user_session(session_hash)
        if user_email:
            return user_email

    try:
        token_from_params = get_access_token_from_query_params(client, redirect_url)
    except KeyError:
        show_login_button()
        return None

    user_info = decode_user(token=token_from_params["id_token"])
    new_session_hash = generate_user_session_hash()
    store_user_session(user_info["email"], new_session_hash)
    set_cookie_js(new_session_hash)

    return user_info["email"]

# Main execution
user_email = get_logged_in_user_email()
if user_email:
    st.write(f"Logged in as {user_email}")
else:
    show_login_button()
