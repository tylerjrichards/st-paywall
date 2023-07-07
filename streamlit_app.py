import streamlit as st
from aggregate_auth import require_auth

from google_auth import (
    get_logged_in_user_email,
    show_login_button,
)
from stripe_auth import get_customer_emails, redirect_button

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

require_auth()

st.write("Congrats, you are subscribed!")
