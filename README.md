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

<strong>A python package for creating paid Streamlit apps with a paywall! </strong>

## Why st-paywall?

I made st-paywall so data scientists and LLM developers can create small businesses around their Streamlit apps. Every week I see dozens of new incredible apps built in Streamlit that are adored by users, but eventually shut down or moved off of Streamlit as authentication and payment integration are too hard. This is my attempt at a dead-simple API around each, abstracting the both away into a single function (`add_auth`). Enjoy!

## Documentation

Once you configure the authentication and subscription on `st.secrets`, you can use the the library methods to conditionally render the content of the page:

```python
from st_paywall import add_auth

add_auth()

#after authentication, the email and subscription status is stored
#in session state
st.write(st.session_state.email)
st.write(st.session_state.user_subscribed)
```


The full documentation for the usage of the library can be found at https://st-paywall.readthedocs.io/.


### Feedback:

If you have feedback about this package, please reach out to me on [twitter](https://twitter.com/tylerjrichards) or file an issue in [this repo](https://github.com/tylerjrichards/st-paywall/issues) and I will do my best to help you out.

### Local Development:

Local development setup with python >= 3.8 installed:

- Fork the repository to your own github account from the top of [this page](https://github.com/tylerjrichards/st-paywall)
- Clone your forked repository to your local system
- Initialize a virtual environment with python 3.8 installed
- Install the package locally with pip in editable mode
- Install streamlit
- Run the sample application
- Edit `src/st_paywall` as needed and re-run the sample application

Sample:

```sh
# clone fork
git clone git@github.com:$YOUR_USERNAME/st-paywall.git
# init virtual env
cd st-paywall
python -m venv venv
. ./venv/bin/activate
# Install dependencies
python -m pip install -e .
python -m pip install streamlit
# Run sample application!
python -m streamlit run streamlit_app.py
```
