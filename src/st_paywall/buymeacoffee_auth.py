from __future__ import annotations
import requests
import streamlit as st


def extract_payer_emails(json_response):
    payer_emails = []

    for item in json_response["data"]:
        payer_email = item["payer_email"]
        payer_emails.append(payer_email)

    return payer_emails


def get_bmac_payers(access_token: str | None = None, one_time: bool = False):
    if access_token is None:
        access_token = st.secrets["bmac_api_key"]

    if one_time is False:
        url = "https://developers.buymeacoffee.com/api/v1/subscriptions?status=active"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return extract_payer_emails(response.json())
        else:
            raise Exception(
                "Error fetching active subscriptions: "
                f"{response.status_code} - {response.text}"
            )
    else:
        url = "https://developers.buymeacoffee.com/api/v1/supporters"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return extract_payer_emails(response.json())
        else:
            raise Exception(
                "Error fetching active subscriptions: "
                f"{response.status_code} - {response.text}"
            )
