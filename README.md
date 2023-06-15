[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](DEPLOYED_APP_URL)

# 🥟 st-stripe

<strong>A template for how to create subscription Streamlit apps </strong>

## Overview

This repo shows you how to add both Google authentication and a Stripe subscription to your Streamlit apps. I hope you use this to create tons of value, and capture some of it with the magic of Streamlit!

- google_auth.py: this holds all of the Google Oauth parts of this code
- stripe_auth.py: this holds all the Stripe button creation and customer listing aspects of the code
- streamlit_app.py: this brings it all together, and has the code after users have subscribed

There is also one file you will have to create yourself:

- .streamlit/secrets.toml: this holds all of your secret credentials to access Google and Stripe. Note that you will need to create the .streamlit/ folder first, and then secrets.toml

### Stripe

In order to set up your Stripe (the best and easiest payment infrastructure in the world), go to [Stripe.com](https://stripe.com) and make an account. Once you make an account, you need to make a [payment subscription link](https://dashboard.stripe.com/test/payment-links/create) (which is in test mode by default) and add the link to your app (currently held in streamlit_app.py). If the user to your app logs in and has not already signed up and paid via Stripe, they will be asked to subscribe before they can see the rest of the app.

The subscription link should be added to secrets.toml like this. If you are using a test link, your link will include test (like the example below), otherwise it will not!

```toml
stripe_link = 'https://buy.stripe.com/test_...'`
```

You also need to create an [API key](https://dashboard.stripe.com/test/apikeys), which just like subscription links have test options as well. Store your API key in your secrets file as stripe_api_key and you're off to the races.

The subscription link should be added to secrets.toml like this

```toml
stripe_api_key = 'sk_test_...'`
```

By default we link out to creating test subscription links and test api keys, but when you launch your app and want folks to pay real money, switch over to a non-test link + api key on your [Stripe dashboard](https://dashboard.stripe.com).



### Google

In order to set up your Google Oauth, you need to register your web app with Google's OAuth system! Basically, you need to tell

So head over to [this url](https://console.cloud.google.com/apis/credentials/oauthclient) and create a web application (and a project, if this is your first go around with Google Cloud). Give a unique name, and add 'http://localhost:8501/' as an "Authorized redirect URI" (when you deploy your app, you'll also need to add the final url of your app to this list). Now press create, and store your client id, and client secret in the secrets.toml file as client_id and client_secret.

For example:

```toml
client_id = '1234.....googleusercontent.com'
client_secret = 'GOC...'
redirect_url = 'http://localhost.com:8501'
```

The last step for your Google Oauth provisioning is to head over to the [consent screen](https://console.cloud.google.com/apis/credentials/consent) and edit what users will see when logging in. Fill out all the info they ask for, and make sure to add the email scope (called '.../auth/userinfo.email' by Google with the user description 'See your primary Google Account email address'). That should be it!
