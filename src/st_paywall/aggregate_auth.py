import streamlit as st
from .google_auth import get_logged_in_user_email, show_login_button
from .stripe_auth import get_customer_emails, redirect_button
from .buymeacoffee_auth import get_bmac_payers

payment_provider = st.secrets.get("payment_provider", "stripe")


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
    if payment_provider == "stripe":
        customer_emails = get_customer_emails()
    elif payment_provider == "bmac":
        customer_emails = get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if user_email not in customer_emails:
        redirect_button(
            text="Subscribe now!",
            customer_email=user_email,
            payment_provider=payment_provider,
        )
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
    if payment_provider == "stripe":
        customer_emails = get_customer_emails()
    elif payment_provider == "bmac":
        customer_emails = get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not user_email:
        show_login_button()
        st.session_state.email = ""
        st.sidebar.markdown("")

    if user_email and user_email not in customer_emails:
        redirect_button(
            text="Subscribe now!", customer_email="", payment_provider=payment_provider
        )
        st.sidebar.markdown("")
        st.session_state.user_subscribed = False

    elif user_email in customer_emails:
        st.session_state.user_subscribed = True

    if st.session_state.email != "":
        if st.sidebar.button("Logout", type="primary"):
            del st.session_state.email
            del st.session_state.user_subscribed
            st.experimental_rerun()
