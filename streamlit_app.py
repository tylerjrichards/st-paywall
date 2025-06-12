import streamlit as st
from st_paywall import add_auth

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

if not st.user.is_logged_in:
    if st.button("Log in using Streamlit's native authentication"):
        st.login()

else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.user.name}!")
    st.write('Now we can use this to check if the user is a subscriber!')
    add_auth(required=True, show_redirect_button=True, use_sidebar=False)

    st.write("Congrats, you are subscribed!")
    st.write("the email of the user is " + str(st.user.email))
