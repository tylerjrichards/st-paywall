import asyncio

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2

from google_auth import (
    decode_user,
    get_access_token_from_query_params,
    get_authorization_url,
    markdown_button,
)
from stripe_auth import get_customer_emails, redirect_button

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

my_customer_emails = get_customer_emails()

client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_url = st.secrets["redirect_url"]

client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)


def show_login_button():
    authorization_url = asyncio.run(
        get_authorization_url(client=client, redirect_url=redirect_url)
    )
    markdown_button(authorization_url, "Login with Google")


if "token" not in st.session_state:
    try:
        st.session_state.token = get_access_token_from_query_params(
            client, redirect_url
        )
    except KeyError:
        show_login_button()
        st.stop()

decoded_user_info = decode_user(token=st.session_state.token["id_token"])
user_email = decoded_user_info["email"]
if user_email:
    st.sidebar.write("")
    st.sidebar.write(f"You are logged in as {user_email}")

if user_email not in my_customer_emails:
    subscribe_link = st.secrets["stripe_link"]
    st.sidebar.write(
        "Looks like you are not yet subscribed to this app! Click the button below to sub"
    )
    redirect_button(subscribe_link, "Subscribe now!")
    st.stop()

st.write("Congrats, you are subscribed in!")
