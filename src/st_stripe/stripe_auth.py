import streamlit as st
import stripe
import urllib.parse

testing_mode = st.secrets.get("testing_mode", False)
stripe.api_key = st.secrets["stripe_api_key_test"] if testing_mode else st.secrets["stripe_api_key"]
stripe_link = st.secrets["stripe_link_test"] if testing_mode else st.secrets["stripe_link"]


def redirect_button(
    text: str,
    customer_email: str,
    color="#FD504D",
):
    encoded_email = urllib.parse.quote(customer_email)
    button_url = f"{stripe_link}?prefilled_email={encoded_email}"

    st.sidebar.markdown(
        f"""
    <a href="{button_url}" target="_blank">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )


def get_customer_emails():
    customers = stripe.Customer.list()
    emails = []
    for i in customers["data"]:
        emails.append(i["email"])
    return emails
