import streamlit as st
from .stripe_auth import is_active_subscriber, redirect_button
from .buymeacoffee_auth import get_bmac_payers

payment_provider = st.secrets.get("payment_provider", "stripe")


def add_auth(required: bool = True, show_redirect_button: bool = True, subscription_button_text: str = 'Subscribe now!', button_color: str = "#FD504D", use_sidebar: bool = True):
    """Add authentication and payment verification to a Streamlit app."""
    if required:
        require_auth(show_redirect_button, subscription_button_text, button_color, use_sidebar)
    else:
        optional_auth(show_redirect_button, subscription_button_text, button_color, use_sidebar)


def require_auth(show_redirect_button: bool = True, subscription_button_text: str = 'Subscribe now!', button_color: str = "#FD504D", use_sidebar: bool = True):
    """Require authentication and payment verification to proceed."""
    if not st.experimental_user.is_logged_in:
        st.stop()

    user_email = st.experimental_user.email

    if payment_provider == "stripe":
        is_subscriber = is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not is_subscriber:
        if show_redirect_button:
            redirect_button(
                text=subscription_button_text,
                customer_email=user_email,
                color=button_color,
                payment_provider=payment_provider,
                use_sidebar=use_sidebar,
            )
        st.session_state.user_subscribed = False
        st.stop()
    else:
        st.session_state.user_subscribed = True


def optional_auth(show_redirect_button: bool=True, subscription_button_text: str = 'Subscribe now!', button_color: str = "#FD504D", use_sidebar: bool = True):
    """Add optional authentication and payment verification."""
    if st.experimental_user.is_logged_in:
        user_email = st.experimental_user.email

    if payment_provider == "stripe":
        is_subscriber = user_email and is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email and user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not user_email:
        st.session_state.user_subscribed = False
        if show_redirect_button:
            redirect_button(
                text=subscription_button_text,
                customer_email="",
                color=button_color,
                payment_provider=payment_provider,
                use_sidebar=use_sidebar,
            )
    elif not is_subscriber:
        st.session_state.user_subscribed = False
        if show_redirect_button:
            redirect_button(
                text=subscription_button_text,
                customer_email=user_email,
                color=button_color,
                payment_provider=payment_provider,
                use_sidebar=use_sidebar,
            )
    else:
        st.session_state.user_subscribed = True
