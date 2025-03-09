import streamlit as st
from st_paywall import add_auth

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

if not st.experimental_user.is_logged_in:
    if st.button("Log in"):
        st.login()

else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.experimental_user.name}!")


add_auth(required=True, show_redirect_button=True, use_sidebar=True)

st.write("Congrats, you are subscribed!")
st.write("the email of the user is " + str(st.experimental_user.email))
