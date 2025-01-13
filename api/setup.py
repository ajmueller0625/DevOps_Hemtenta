import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host=os.getenv("DB_HOST"),  # Use the DB_HOST variable
        port=os.getenv("DB_PORT"),  # Use the DB_PORT variable
    )


def create_tables():
    con = get_connection()
    create_games_table_query = """ 
    CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100) NOT NULL,
            platform VARCHAR(100) NOT NULL,
            release_year INT NOT NULL
        );
    """

    create_developers_table_query = """
    CREATE TABLE IF NOT EXISTS developers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            founded_year INT NOT NULL
        );
    """

    create_publishers_table_query = """
    CREATE TABLE IF NOT EXISTS publishers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            country VARCHAR(100) NOT NULL
        );
    """

    create_reviews_table_query = """
    CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            game_id INT NOT NULL REFERENCES games(id),
            reviewer VARCHAR(255) NOT NULL,
            rating FLOAT NOT NULL CHECK (rating >= 0 AND rating <= 10),
            comment TEXT
        );
    """

    create_game_developers_table_query = """
    CREATE TABLE IF NOT EXISTS game_developers (
            game_id INT NOT NULL REFERENCES games(id),
            developer_id INT NOT NULL REFERENCES developers(id),
            PRIMARY KEY (game_id, developer_id)
        );
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(create_games_table_query)
            cursor.execute(create_developers_table_query)
            cursor.execute(create_publishers_table_query)
            cursor.execute(create_reviews_table_query)
            cursor.execute(create_game_developers_table_query)


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
