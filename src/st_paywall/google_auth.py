import asyncio
from typing import Optional

import jwt
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2

testing_mode = st.secrets.get("testing_mode", False)


client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_url = st.secrets["redirect_url_test"] if testing_mode else st.secrets["redirect_url"]

client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)


@st.cache_resource(ttl=300)
def qparms_cache(key):
    return {}

def state_generator(size):
    import string
    import random
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def decode_user(token: str):
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(jwt=token, options={"verify_signature": False})

    return decoded_data


async def get_authorization_url(client: GoogleOAuth2, redirect_url: str):
    state = state_generator(15)
    if st.experimental_get_query_params():
        qpcache = qparms_cache(state)
        qpcache = st.experimmental_get_query_params()
    authorization_url = await client.get_authorization_url(
        redirect_url,
        state=state,
        scope=["email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url


def markdown_button(
    url: str, text: Optional[str] = None, color="#FD504D", sidebar: bool = True
):
    markdown = st.sidebar.markdown if sidebar else st.markdown

    markdown(
        f"""
    <a href="{url}" target="_blank">
        <div style="
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
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


async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str):
    token = await client.get_access_token(code, redirect_url)
    return token


def get_access_token_from_query_params(client: GoogleOAuth2, redirect_url: str) -> str:
    query_params = st.experimental_get_query_params()
    code = query_params["code"]
    if "state" in query_params:
        qpcache = qparms_cache(query_params["state"])

    token = asyncio.run(
        get_access_token(client=client, redirect_url=redirect_url, code=code)
    )
    # Clear query params
    st.experimental_set_query_params(**qpcache)
    return token


def show_login_button():
    authorization_url = asyncio.run(
        get_authorization_url(client=client, redirect_url=redirect_url)
    )
    markdown_button(authorization_url, "Login with Google")


def get_logged_in_user_email() -> Optional[str]:
    if "email" in st.session_state:
        return st.session_state.email

    try:
        token_from_params = get_access_token_from_query_params(client, redirect_url)
    except KeyError:
        return None

    user_info = decode_user(token=token_from_params["id_token"])

    st.session_state["email"] = user_info["email"]

    return user_info["email"]
