import streamlit as st

from google_auth import (
    show_sidebar_login,
    get_access_token_from_query_params,
    get_client,
    get_logged_in_user_email
)
from stripe_auth import get_customer_emails, redirect_button

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

my_customer_emails = get_customer_emails()

user_email = get_logged_in_user_email()

if user_email:
    if st.sidebar.button("Logout", type="primary"):
        del st.session_state.email
        st.experimental_rerun()
else:
    show_sidebar_login()
    try:
        token_from_params = get_access_token_from_query_params(get_client(), redirect_url=str(st.secrets["redirect_uri_branch"]))
    except KeyError:
        st.stop()

if user_email:
    st.sidebar.write("")
    st.sidebar.write(f"You are logged in as {user_email}")

if user_email not in my_customer_emails:
    st.sidebar.write(
        """Looks like you are not yet subscribed to this app! Click the button below to
        subscribe"""
    )
    redirect_button(text="Subscribe now!", customer_email=user_email)
    st.stop()

st.write("Congrats, you are subscribed!")
