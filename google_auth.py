import jwt
import streamlit as st


def decode_user(token: str):
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(jwt=token,
                              options={"verify_signature": False})

    return decoded_data

async def write_authorization_url(client,
                                  redirect_url
                                  ):
    authorization_url = await client.get_authorization_url(
        redirect_url,
        scope=["email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url

def markdown_button(url: str, text: str= None, color="#FD504D"):
    st.sidebar.markdown(
    f"""
    <a href="{url}" target="_self">
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
    unsafe_allow_html=True
    )


async def write_access_token(client,
                             redirect_url,
                             code):
    token = await client.get_access_token(code, redirect_url)
    return token