import asyncio

import streamlit as st
import stripe
from httpx_oauth.clients.google import GoogleOAuth2

from google_auth import (
    decode_user,
    markdown_button,
    write_access_token,
    write_authorization_url,
)
from stripe_auth import get_customer_emails, redirect_button

st.set_page_config(layout="wide")
st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

my_customer_emails = get_customer_emails()

client_id = st.secrets['client_id']
client_secret = st.secrets['client_secret']
redirect_url = st.secrets['redirect_url']

client = GoogleOAuth2(client_id=client_id,
                      client_secret=client_secret)

authorization_url = asyncio.run(
    write_authorization_url(client=client,
                            redirect_url=redirect_url)
)
markdown_button(authorization_url, "Login with Google")


if 'user_token' in st.session_state:
    token = st.session_state.user_token
    pass
else:
    try:
        query_params = st.experimental_get_query_params()
        code = query_params['code']
        st.experimental_set_query_params()
        token = asyncio.run(
            write_access_token(client=client,
                            redirect_url=redirect_url,
                            code=code))
        st.session_state.user_token = token
    except Exception:
        st.stop()

decoded_user_info = decode_user(token=token['id_token'])
user_email = decoded_user_info['email']
if user_email:
    st.sidebar.write('')
    st.sidebar.write(f'You are logged in as {user_email}')

if user_email not in my_customer_emails:
    subscribe_link = "https://buy.stripe.com/test_bIYg0v53Pfo73pCfYY"
    st.sidebar.write('Looks like you are not yet subscribed to this app! Click the button below to sub')
    redirect_button(subscribe_link,"Subscribe now!")
    st.stop()


st.subheader('Welcome to Tylers Super Cool GPT App')
st.write('Toss your prompt in here to see the magic')
import openai

gpt3_api = st.secrets["gpt3_api"]
openai.api_key = gpt3_api

@st.cache_data
def get_gpt3_completion(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    return response

my_text_input = st.text_input('Your prompt', 'How big is the sun')
output = get_gpt3_completion(my_text_input)["choices"][0]["text"]

st.write(f"Your response is {output}")