# Home

I made st-paywall so data scientists and LLM developers can create small businesses around their Streamlit apps. Every week I see dozens of new incredible apps built in Streamlit that are adored by users, but eventually shut down or moved off of Streamlit as authentication and payment integration are too hard. This is my attempt at a dead-simple API around each, abstracting the both away into a single function (`add_auth`). Enjoy!

## Overview

This package gives you one basic function (`add_auth`) that adds subscription functionality to your Streamlit apps. `add_auth` will add both a Google login button if they are not logged in, and a Stripe (or Buy Me A Coffee) subscription button to your sidebar if they are not subscribed. If they are subscribed, `st.session_state.user_subscribed` will be true, and if they are logged in, `st.session_state.email` will have their email. `st.session_state.subscriptions` will have the info about their subscription(s).
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

## Navigation

Use the top navigation bar to access the other pages within the documentation.