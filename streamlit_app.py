import streamlit as st
from st_paywall import add_auth

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

add_auth(
    required=True,
    login_button_text="Login with Google",
    login_button_color="#FD504D",
    login_sidebar=True,
)

st.write("Congrats, you are subscribed!")
st.write("the email of the user is " + str(st.session_state.email))
