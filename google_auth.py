import asyncio

import jwt
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from google_auth_oauthlib.flow import Flow

clientSecret = str(st.secrets["client_secret"])
clientId = str(st.secrets["client_id"])
redirectUri = str(st.secrets["redirect_url_test"])

def markdown_button(
    url: str, text: str | None = None, color="#FD504D", sidebar: bool = True
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

def show_sidebar_login():
    st.markdown("")
    url = ("https://accounts.google.com/o/oauth2/auth?response_type=code&client_id="
        + str(clientId)
        + "&redirect_uri="
        + str(redirectUri)
        + "&scope=email&access_type=offline&prompt=consent")
    markdown_button(url, "Sign-in with Google", sidebar=True)

    credentials = {
        "installed": {
            "client_id": clientId,
            "client_secret": clientSecret,
            "redirect_uris": [],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
        }
    }

    flow = Flow.from_client_config(
        credentials,
        scopes=["email"],
        redirect_uri=redirectUri,
    )

    auth_url, _ = flow.authorization_url(prompt="consent")


def decode_user(token: str):
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(jwt=token, options={"verify_signature": False})

    return decoded_data

def get_client():
    client = GoogleOAuth2(client_id=clientId, client_secret=clientSecret)
    return(client)


def get_access_token_from_query_params(client: GoogleOAuth2, redirect_url: str) -> str:
    code = st.experimental_get_query_params()["code"]
    token = asyncio.run(
        get_access_token(client=client, redirect_url=redirect_url, code=code)
    )
    # Clear query params
    st.experimental_set_query_params()
    return token



async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str):
    token = await client.get_access_token(code, redirect_url)
    return token



def get_logged_in_user_email() -> str | None:
    if "email" in st.session_state:
        return st.session_state.email
    try:
        token_from_params = get_access_token_from_query_params(get_client(), redirect_url=str(st.secrets["redirect_uri_branch"]))
    except KeyError:
        return None

    user_info = decode_user(token=token_from_params["id_token"])

    st.session_state["email"] = user_info["email"]

    return user_info["email"]
