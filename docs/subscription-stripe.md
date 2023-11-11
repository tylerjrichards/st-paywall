# Subscription with Stripe

In order to set up your Stripe (the best and easiest payment infrastructure in the world), go to [Stripe.com](https://stripe.com) and make an account. Once you make an account, you need to make a [payment subscription link](https://dashboard.stripe.com/test/payment-links/create) (which is in test mode by default) and add the link to your app (currently held in streamlit_app.py). If the user to your app logs in and has not already signed up and paid via Stripe, they will be asked to subscribe before they can see the rest of the app. The package will also add information about the user's subscriptions that it gets from the Stripe API back to you via session state, in a param called 'subscriptions'. If you want to have multiple subscriptions, or filter only for a specific subscription, you can use this information to do so!

The subscription link should be added to secrets.toml like this.

```toml
stripe_link = 'https://buy.stripe.com/test_...'`
```

You also need to create an [Standard API key](https://dashboard.stripe.com/test/apikeys), which just like subscription links have test options as well. Store your API key in your secrets file as stripe_api_key and you're off to the races. If you make a restricted API key instead of a Standard key, make sure to add read permission on Customers and Subscriptions.


![Stripe API rest](images/stripe_api_rest.png)

The API key should be added to `secrets.toml` like this


```toml
stripe_api_key = 'sk_...'`
```

By default this repo links to creating test subscription links and test api keys (you probably already noticed the 'test' in the Stripe dashboard, the subscription link, and in our example api key). When you launch your app and want folks to pay real money, you will need to create production links and api keys from your [Stripe dashboard](https://dashboard.stripe.com) and use those instead. While you are testing out the Stripe part of your code, you can use [Stripe's test cards](https://stripe.com/docs/testing) instead of inputting your own credit card info! To run st-paywall in test mode, add the following to your secrets file.

```toml
testing_mode = true
```

Then, the package will look for the following secrets. Otherwise, it will look for the production api and link secrets. I highly encourage you to start out in test mode!

```toml
stripe_api_key_test = 'sk_test_...'`
stripe_link_test = 'https://buy.stripe.com/test_...'`
```

Once you decide to leave test mode and publish your subscription app, it is a good idea to have Stripe send the user back to your app once they've subscribed. To do this, go to the [payment links](https://dashboard.stripe.com/payment-links) page, edit your payment link, click 'After payment' and fill out your app's url.


![Payment Link After](images/payment_link_after.png)

<p>&nbsp;</p>