[![Releases](https://img.shields.io/pypi/v/st-paywall)](https://pypi.org/project/st-paywall/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://subscription.streamlit.app)

Author: [@tylerjrichards](https://twitter.com/tylerjrichards)

Kind consultant: [@blackary](https://github.com/blackary)

## Installation

```sh
pip install st-paywall
```

## See it in action

Basic example: https://subscription.streamlit.app

<p>&nbsp;</p>

# 🥟 st-paywall

<strong>A python package for creating paywalled Streamlit apps! </strong>

## Why st-paywall?

I made st-paywall so data scientists and LLM developers can create small businesses around their Streamlit apps. Every week I see dozens of new incredible apps built in Streamlit that are adored by users, but eventually shut down or moved off of Streamlit as authentication and payment integration are too hard. This is my attempt at a dead-simple API around each, abstracting the both away into a single function (`add_auth`). Enjoy!

## Documentation

Once you configure the authentication and subscription on `st.secrets`, you can use the the library methods to conditionally render the content of the page:

```python
from st_paywall import add_auth

add_auth(required=True)

#after authentication, the email and subscription status is stored in session state
st.write(st.session_state.email)
st.write(st.session_state.user_subscribed)
```

If the `required` parameter is `True`, the app will stop with `st.stop()` if the user is not logged in and subscribed. Otherwise, you the developer will have control over exactly how you want to paywall the apps!

I hope you use this to create tons of value, and capture some of it with the magic of Streamlit.

This package expects that you have a `.streamlit/secrets.toml` file which you will have to create. Inside it, you will need to add your Stripe (or Buy Me A Coffee) and Google API information that runs the authentication and subscription parts of the package. If you already have all of your information for your payment and authentication providers, here is how the package expects your secrets file to look.

```toml
testing_mode = true
payment_provider = "stripe" #bmac if using Buy Me A Coffee
stripe_api_key_test = "sk_test_..." #only needed if using Stripe
stripe_api_key = "sk_live_..." #only needed if using Stripe
stripe_link = "https://buy.stripe.com/..." #only needed if using Stripe
stripe_link_test = "https://buy.stripe.com/test_..." #only needed if using Stripe
client_id = "590..."
client_secret = "GO..."
redirect_url_test = 'http://localhost:8501/'
redirect_url = "https://your_app_url..."
bmac_api_key = "ey..." #only needed if using buy me a coffee
bmac_link = "https://www.buymeacoffee.com/..." #only needed if using buy me a coffee
```

The full documentation for the usage of the library can be found at https://st-paywall.readthedocs.io/.


### Feedback:

If you have feedback about this package, please reach out to me on [twitter](https://twitter.com/tylerjrichards) or file an issue in [this repo](https://github.com/tylerjrichards/st-paywall/issues) and I will do my best to help you out.
