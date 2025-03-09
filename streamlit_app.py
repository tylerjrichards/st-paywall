import streamlit as st
from st_paywall import add_auth

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

add_auth(
    required=True,
    subscription_button_text="Login with Google",
    button_color="#FD504D",
    use_sidebar=True,
)

st.write("Congrats, you are subscribed!")
st.write("the email of the user is " + str(st.experimental_user.email))
