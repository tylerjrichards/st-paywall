import streamlit as st
import stripe

stripe.api_key = st.secrets["stripe_api_key"]


def redirect_button(url: str, text: str = None, color="#FD504D"):
    st.sidebar.markdown(
        f"""
    <a href="{url}" target="_blank">
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
