import sqlite3


DATABASE_NAME = "personal_ai.db"


def init_memory_database():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            memory TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()


def save_memory(memory):

    if not memory or not memory.strip():

        return

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories (memory)

        VALUES (?)
        """,

        (
            memory.strip(),
        )
    )

    connection.commit()

    connection.close()


def get_memories():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, memory, created_at

        FROM memories

        ORDER BY id DESC
        """
    )

    memories = cursor.fetchall()

    connection.close()

    return memories


def delete_memory(memory_id):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM memories

        WHERE id = ?
        """,

        (
            memory_id,
        )
    )

    connection.commit()

    connection.close()


def clear_all_memories():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM memories
        """
    )

    connection.commit()

    connection.close()


def search_memories(query):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, memory, created_at

        FROM memories

        WHERE memory LIKE ?

        ORDER BY id DESC
        """,

        (
            f"%{query}%",
        )
    )

    memories = cursor.fetchall()

    connection.close()

    return memories