import asyncio

import jwt
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2


def decode_user(token: str):
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(jwt=token, options={"verify_signature": False})

    return decoded_data


async def get_authorization_url(client: GoogleOAuth2, redirect_url: str):
    authorization_url = await client.get_authorization_url(
        redirect_url,
        scope=["email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url


def markdown_button(url: str, text: str | None = None, color="#FD504D"):
    st.sidebar.markdown(
        f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )


async def get_access_token(client, redirect_url, code):
    token = await client.get_access_token(code, redirect_url)
    return token


def get_access_token_from_query_params(client: GoogleOAuth2, redirect_url: str) -> str:
    query_params = st.experimental_get_query_params()
    code = query_params["code"]
    return asyncio.run(
        get_access_token(client=client, redirect_url=redirect_url, code=code)
    )
