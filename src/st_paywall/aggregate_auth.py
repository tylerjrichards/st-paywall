import streamlit as st
from .stripe_auth import is_active_subscriber as is_stripe_subscriber, redirect_button
from .buymeacoffee_auth import get_bmac_payers

payment_provider = st.secrets.get("payment_provider", "stripe")


def add_auth(required: bool = True, 
             show_redirect_button: bool = True, 
             subscription_button_text: str = 'Subscribe now!',
             button_color: str = "#FD504D", 
             use_sidebar: bool = True):
    """Add authentication and payment verification to a Streamlit app."""
    if required:
        require_auth(show_redirect_button, subscription_button_text, button_color, use_sidebar)
    else:
        optional_auth(show_redirect_button, subscription_button_text, button_color, use_sidebar)


def is_bmac_subscriber(email: str) -> bool:
    """Check if a user is a Buy Me A Coffee subscriber."""
    return email in get_bmac_payers()


def is_subscriber(email: str) -> bool:
    """Check if a user is a subscriber based on the global payment provider."""
    if payment_provider == "stripe":
        return is_stripe_subscriber(email)
    elif payment_provider == "bmac":
        return is_bmac_subscriber(email)
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")


def require_auth(show_redirect_button: bool = True, subscription_button_text: str = 'Subscribe now!', button_color: str = "#FD504D", use_sidebar: bool = True):
    """Require authentication and payment verification to proceed."""
    if not st.experimental_user.is_logged_in:
        st.stop()

    user_email = st.experimental_user.email
    is_subscribed = is_subscriber(user_email)

    if not is_subscribed:
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
    user_email = None
    if st.experimental_user.is_logged_in:
        user_email = st.experimental_user.email
    
    is_subscribed = user_email and is_subscriber(user_email)

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
    elif not is_subscribed:
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
