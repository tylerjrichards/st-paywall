import streamlit as st

from google_auth import (
    show_sidebar_login,
)
from stripe_auth import get_customer_emails, redirect_button

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()


from google_auth_oauthlib.flow import Flow
from streamlit_elements import Elements


show_sidebar_login()
if st.session_state.my_token_received:
    st.write(st.session_state.my_token_input)

my_customer_emails = get_customer_emails()

user_email = get_logged_in_user_email()

if user_email:
    if st.sidebar.button("Logout", type="primary"):
        del st.session_state.email
        st.experimental_rerun()
else:
    show_login_button()
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
