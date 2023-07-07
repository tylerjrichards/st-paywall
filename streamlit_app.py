import streamlit as st
from st_stripe import require_auth

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

require_auth()

st.write("Congrats, you are subscribed!")
st.write(st.session_state.email)
st.write(st.session_state.user_subscribed)