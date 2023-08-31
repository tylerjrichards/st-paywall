import streamlit as st
import extra_streamlit_components as stx

from . import EMAIL_COOKIE, SUBSCRIBED_COOKIE
from .google_auth import get_logged_in_user_email, show_login_button
from .stripe_auth import is_active_subscriber, redirect_button
from .buymeacoffee_auth import get_bmac_payers

payment_provider = st.secrets.get("payment_provider", "stripe")
cookie_manager = stx.CookieManager()


def add_auth(required=True):
    if required:
        require_auth()
    else:
        optional_auth()


def require_auth():
    user_email = get_logged_in_user_email(cookie_manager)

    if not user_email:
        show_login_button()
        st.stop()
    if payment_provider == "stripe":
        is_subscriber = user_email and is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email and user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not is_subscriber:
        redirect_button(
            text="Subscribe now!",
            customer_email=user_email,
            payment_provider=payment_provider,
        )
        cookie_manager.set(SUBSCRIBED_COOKIE, False)
        st.stop()
    elif is_subscriber:
        cookie_manager.set(SUBSCRIBED_COOKIE, True)

    if st.sidebar.button("Logout", type="primary"):
        cookie_manager.delete(EMAIL_COOKIE)
        cookie_manager.delete(SUBSCRIBED_COOKIE)
        st.experimental_rerun()


def optional_auth():
    user_email = get_logged_in_user_email(cookie_manager)
    if payment_provider == "stripe":
        is_subscriber = user_email and is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email and user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not user_email:
        show_login_button()
        cookie_manager.set(EMAIL_COOKIE, "")
        st.sidebar.markdown("")

    if not is_subscriber:
        redirect_button(
            text="Subscribe now!", customer_email="", payment_provider=payment_provider
        )
        st.sidebar.markdown("")
        cookie_manager.set(SUBSCRIBED_COOKIE, False)

    elif is_subscriber:
        cookie_manager.set(SUBSCRIBED_COOKIE, True)

    email_cookie = cookie_manager.get(EMAIL_COOKIE)
    if email_cookie is not None and email_cookie != "":
        if st.sidebar.button("Logout", type="primary"):
            cookie_manager.delete(EMAIL_COOKIE)
            cookie_manager.delete(SUBSCRIBED_COOKIE)
            st.experimental_rerun()
