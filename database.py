import sqlite3

from datetime import datetime


DATABASE_NAME = "chat_history.db"


def get_connection():

    return sqlite3.connect(
        DATABASE_NAME
    )


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            conversation_id INTEGER,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (conversation_id)

            REFERENCES conversations(id)

        )
        """
    )

    connection.commit()

    connection.close()


def create_conversation(
    title="New Chat"
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    clean_title = title.strip()

    if not clean_title:

        clean_title = "New Chat"

    clean_title = clean_title[:60]

    cursor.execute(
        """
        INSERT INTO conversations
        (
            title,
            created_at
        )

        VALUES (?, ?)
        """,

        (
            clean_title,
            created_at
        )
    )

    conversation_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return conversation_id


def save_message(
    conversation_id,
    role,
    content
):

    if conversation_id is None:

        return

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO messages
        (
            conversation_id,

            role,

            content,

            created_at
        )

        VALUES (?, ?, ?, ?)
        """,

        (
            conversation_id,

            role,

            content,

            created_at
        )
    )

    connection.commit()

    connection.close()


def get_conversations():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, created_at

        FROM conversations

        ORDER BY id DESC
        """
    )

    conversations = cursor.fetchall()

    connection.close()

    return conversations


def get_messages(
    conversation_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content

        FROM messages

        WHERE conversation_id = ?

        ORDER BY id ASC
        """,

        (
            conversation_id,
        )
    )

    messages = cursor.fetchall()

    connection.close()

    return messages


def delete_conversation(
    conversation_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM messages

        WHERE conversation_id = ?
        """,

        (
            conversation_id,
        )
    )

    cursor.execute(
        """
        DELETE FROM conversations

        WHERE id = ?
        """,

        (
            conversation_id,
        )
    )

    connection.commit()

    connection.close()


def delete_all_conversations():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("DELETE FROM messages")
    cursor.execute("DELETE FROM conversations")

    connection.commit()

    connection.close()


def update_conversation_title(conversation_id, title):
    import sqlite3

    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE conversations SET title = ? WHERE id = ?",
        (title, conversation_id)
    )

    conn.commit()
    conn.close()