import streamlit as st
from .google_auth import get_logged_in_user_email, show_login_button
from .stripe_auth import get_customer_emails, redirect_button

def add_auth(required=True):
    if required:
        require_auth()
    else:
        optional_auth()

def require_auth():
    user_email = get_logged_in_user_email()

    if not user_email:
        show_login_button()
        st.stop()

    customer_emails = get_customer_emails()

    if user_email not in customer_emails:
        redirect_button(text="Subscribe now!", customer_email=user_email)
        st.session_state.user_subscribed = False
        st.stop()
    elif user_email in customer_emails:
        st.session_state.user_subscribed = True

    if st.sidebar.button("Logout", type="primary"):
        del st.session_state.email
        del st.session_state.user_subscribed
        st.experimental_rerun()

def optional_auth():
    user_email = get_logged_in_user_email()
    customer_emails = get_customer_emails()

    if not user_email:
        show_login_button()
        st.session_state.email = ""
        st.sidebar.markdown("")

    if user_email and user_email not in customer_emails:
        redirect_button(text="Subscribe now!", customer_email="")
        st.sidebar.markdown("")
        st.session_state.user_subscribed = False

    elif user_email in customer_emails:
        st.session_state.user_subscribed = True

    if st.session_state.email != "":
        if st.sidebar.button("Logout", type="primary"):
            del st.session_state.email
            del st.session_state.user_subscribed
            st.experimental_rerun()