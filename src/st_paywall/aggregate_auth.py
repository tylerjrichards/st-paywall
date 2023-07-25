import streamlit as st
from .google_auth import (
    get_logged_in_user_email as get_logged_in_user_email_google,
    show_login_button,
)
from .stripe_auth import get_customer_emails, redirect_button
from .buymeacoffee_auth import get_bmac_payers
from .sessions import get_email_from_session, clear_session, set_new_session_id

payment_provider = st.secrets.get("payment_provider", "stripe")


def logout():
    del st.session_state.email
    del st.session_state.user_subscribed
    clear_session()


def add_auth(required: bool = True):
    top_button, bottom_button = st.sidebar.empty(), st.sidebar.empty()

    user_email = get_logged_in_user_email(use_google=True)

    if not user_email:
        with top_button.container():
            show_login_button()
        if required:
            st.stop()
        else:
            return
    else:
        with bottom_button.container():
            if st.button("Logout", type="primary"):
                logout()

    if payment_provider == "stripe":
        customer_emails = get_customer_emails()
    elif payment_provider == "bmac":
        customer_emails = get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if user_email not in customer_emails:
        with top_button.container():
            redirect_button(
                text="Subscribe now!",
                customer_email=user_email,
                payment_provider=payment_provider,
            )
        st.session_state.user_subscribed = False
        if required:
            st.stop()
        else:
            return
    elif user_email in customer_emails:
        st.session_state.user_subscribed = True


def get_logged_in_user_email(use_google: bool = True) -> str | None:
    email = get_email_from_session()
    if email:
        return email

    if use_google:
        email = get_logged_in_user_email_google()

    if email:
        st.session_state["email"] = email
        set_new_session_id(email)

    return email
