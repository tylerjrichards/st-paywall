import sqlite3
import streamlit as st
import secrets
from streamlit_js_eval import get_cookie, set_cookie  # noqa


SESSION_COOKIE_NAME = "st_paywall_session_id"


def delete_cookie(key: str):
    set_cookie(key, "", -1, component_key=f"DELETE_COOKIE_{key}")


def create_table():
    with sqlite3.connect("sessions.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT,
                email TEXT
            )
            """
        )
        conn.commit()
        c.close()


def get_email_from_session_id(session_id: str) -> str | None:
    """Check the database for the email associated with the session_id"""
    create_table()
    with sqlite3.connect("sessions.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT email FROM sessions WHERE session_id = ?
            """,
            (session_id,),
        )

        result = c.fetchone()
        c.close()

    try:
        return result[0]
    except TypeError:
        return None


def set_new_session_id(email: str) -> str:
    """Create a new session_id and store it in the database"""
    create_table()
    session_id = secrets.token_hex(32)
    with sqlite3.connect("sessions.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO sessions (session_id, email) VALUES (?, ?)
            """,
            (session_id, email),
        )
        conn.commit()
        c.close()

    set_cookie(SESSION_COOKIE_NAME, session_id, duration_days=1)

    return session_id


def get_email_from_session() -> str | None:
    try:
        return st.session_state["email"]
    except KeyError:
        pass

    session_id = get_cookie(SESSION_COOKIE_NAME)
    if not session_id:
        return None

    email = get_email_from_session_id(session_id)
    if email:
        st.session_state["email"] = email

    return email


def clear_session():
    delete_cookie(SESSION_COOKIE_NAME)
