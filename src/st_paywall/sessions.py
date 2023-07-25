import sqlite3
import secrets


def create_table():
    with sqlite3.connect("sessions.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT,
                email TEXT,
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

    return result


def get_new_session_id(email: str) -> str:
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

    return session_id
