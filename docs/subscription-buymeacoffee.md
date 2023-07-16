# Subscription with Buy Me A Coffee

Not everywhere in the world is covered by Stripe! Buy Me A Coffee is a lighter, less business-y service that allows folks to support you online. To link to your buy me a coffee page instead of your Stripe payment link, go to their dev page and create an access token. You will also add a membership product offering as well. Once you have the membership link and the key, add the following to your secrets file.

```toml
payment_provider = "bmac"
bmac_api_key = "eyJ0...."
bmac_link = "https://www.buymeacoffee.com/..."
```

This will change your app to link out to buymeacoffee instead of Stripe, and will get your customer list from there as well!

Buy Me A Coffee does not have a testing mode (Stripe does!), so turning on or off testing mode in your secrets file will be ignored.

<p>&nbsp;</p>