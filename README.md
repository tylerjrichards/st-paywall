[![Releases](https://img.shields.io/pypi/v/st-paywall)](https://pypi.org/project/st-paywall/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://subscription.streamlit.app)

Author: [@tylerjrichards](https://twitter.com/tylerjrichards)

Kind consultant: [@blackary](https://github.com/blackary)

# st-paywall 🎈

A Python package for creating paywalled Streamlit apps! 

I made st-paywall so data scientists and LLM developers can create small businesses around their Streamlit apps. Every week I see dozens of new incredible apps built in Streamlit that are adored by users, but eventually shut down or moved off of Streamlit as payment integration is too hard. This is my attempt at a dead-simple API around payments, abstracting it away into a single function (`add_auth`). Enjoy!

## Installation

```bash
pip install st-paywall
```

## Quick Start

1. Set up Streamlit's native authentication in your app's secrets.toml file
2. Add your payment provider configuration (Stripe or Buy Me A Coffee)
3. Import and use `add_auth()` in your app

```python
import streamlit as st
from st_paywall import add_auth

st.title("My Subscription App")

# Handle Streamlit's native authentication
if not st.user.is_logged_in:
    if st.button("Log in using Streamlit's native authentication"):
        st.login()
else:
    # Add subscription check for logged-in users
    add_auth()
    
    # Your app code here - only runs for subscribed users
    st.write("Welcome, subscriber!")
    st.write(f"Your email is: {st.user.email}")
```

## Configuration

Create a `.streamlit/secrets.toml` file with your payment provider settings:

### For Stripe:
```toml
payment_provider = "stripe"
testing_mode = true  # Set to false for production
stripe_api_key_test = "sk_test_..."
stripe_api_key = "sk_live_..."
stripe_link = "https://buy.stripe.com/..."
stripe_link_test = "https://buy.stripe.com/test_..."
```

### For Buy Me A Coffee:
```toml
payment_provider = "bmac"
bmac_api_key = "ey..."
bmac_link = "https://www.buymeacoffee.com/..."
```

## Customization

The `add_auth()` function accepts several parameters to customize its behavior:

```python
add_auth(
    required=True,  # Stop the app if user is not subscribed
    show_redirect_button=True,  # Show the subscription button
    subscription_button_text="Subscribe Now!",  # Custom button text
    button_color="#FF4B4B",  # Button color (CSS color value)
    use_sidebar=True  # Show button in sidebar vs main section
)
```

## Example App

```python
import streamlit as st
from st_paywall import add_auth

st.title("My Subscription App")

if not st.user.is_logged_in:
    st.write("Please log in to access this app")
    if st.button("Log in"):
        st.login()
else:
    add_auth(required=True)
    st.write("Welcome to the premium content!")
```

## Documentation

For full documentation, visit [st-paywall.readthedocs.io](https://st-paywall.readthedocs.io/)

## License

MIT

### Feedback:

If you have feedback about this package, please reach out to me on [twitter](https://twitter.com/tylerjrichards) or file an issue in [this repo](https://github.com/tylerjrichards/st-paywall/issues) and I will do my best to help you out.
