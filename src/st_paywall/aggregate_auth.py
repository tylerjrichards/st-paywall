import streamlit as st
from .stripe_auth import is_active_subscriber, redirect_button
from .buymeacoffee_auth import get_bmac_payers

payment_provider = st.secrets.get("payment_provider", "stripe")


def add_auth(required: bool = True):
    """Add authentication and payment verification to a Streamlit app."""
    if required:
        require_auth()
    else:
        optional_auth()


def require_auth():
    """Require authentication and payment verification to proceed."""
    if not st.experimental_user.email:
        st.stop()

    user_email = st.experimental_user.email

    if payment_provider == "stripe":
        is_subscriber = is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not is_subscriber:
        redirect_button(
            text="Subscribe now!",
            customer_email=user_email,
            payment_provider=payment_provider,
        )
        st.session_state.user_subscribed = False
        st.stop()
    else:
        st.session_state.user_subscribed = True


def optional_auth():
    """Add optional authentication and payment verification."""
    user_email = st.experimental_user.email

    if payment_provider == "stripe":
        is_subscriber = user_email and is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email and user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not user_email:
        st.session_state.user_subscribed = False
        redirect_button(
            text="Subscribe now!",
            customer_email="",
            payment_provider=payment_provider
        )
    elif not is_subscriber:
        st.session_state.user_subscribed = False
        redirect_button(
            text="Subscribe now!",
            customer_email=user_email,
            payment_provider=payment_provider,
        )
    else:
        st.session_state.user_subscribed = True
