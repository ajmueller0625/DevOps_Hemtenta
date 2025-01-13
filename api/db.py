import psycopg2
from psycopg2.extras import RealDictCursor

from exceptions import GameNotFoundError, DeveloperNotFoundError


def add_game_db(con, title: str, genre: str, platform: str, release_year: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    INSERT INTO games (title, genre, platform, release_year) 
                    VALUES (%s, %s, %s, %s) RETURNING id"
                """,
                (title, genre, platform, release_year)
            )
            result = cursor.fetchone()
            if result:
                return result


def get_games_db(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    SELECT * FROM games
                """
            )
            result = cursor.fetchall()
            return result


def get_game_db(con, game_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    SELECT * FROM games 
                    WHERE id = %s
                """,
                (game_id,)
            )
            result = cursor.fetchone()
            if result:
                return result
            raise GameNotFoundError()


def update_game_db(con, game_id: int, title: str, genre: str, platform: str, release_year: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    UPDATE games
                    SET title = %s,
                    genre = %s,
                    platform = %s,
                    release_year = %s
                    WHERE id = %s
                    RETURNING id
                """,
                (title, genre, platform, release_year, game_id)
            )
            result = cursor.fetchone()
            if result:
                return result
            raise GameNotFoundError()


def delete_game_db(con, game_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    DELETE FROM games
                    WHERE id = %s
                    RETURNING id;
                """,
                (game_id,)
            )
            result = cursor.fetchone()
            if result:
                return result
            raise GameNotFoundError()


def add_developer_db(con, name: str, founded_year: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    INSERT INTO developers (name, founded_year) 
                    VALUES (%s, %s) RETURNING id
                """,
                (name, founded_year)
            )
            result = cursor.fetchone()
            if result:
                return result


def get_developers_db(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    SELECT * FROM developers
                """
            )
            result = cursor.fetchall()
            return result


def add_publisher_db(con, name: str, country: str):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    INSERT INTO publishers (name, country) 
                    VALUES (%s, %s) RETURNING id"
                """,
                (name, country)
            )
            result = cursor.fetchone()
            if result:
                return result


def get_publishers_db(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    SELECT * FROM publishers
                """
            )
            result = cursor.fetchall()
            return result


def add_review_db(con, game_id: int, reviewer: str, rating: float, comment: str):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    INSERT INTO reviews (game_id, reviewer, rating, comment) 
                    VALUES (%s, %s, %s, %s) RETURNING id
                """,
                (game_id, reviewer, rating, comment)
            )
            result = cursor.fetchone()
            if result:
                return result


def get_reviews_for_game_db(con, game_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    SELECT * FROM reviews 
                    WHERE game_id = %s
                """,
                (game_id,)
            )
            result = cursor.fetchall()
            if result:
                return result
            raise GameNotFoundError()


def add_game_developer_db(con, game_id: int, developer_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    INSERT INTO game_developers (game_id, developer_id) 
                    VALUES (%s, %s)
                """,
                (game_id, developer_id)
            )
            result = cursor.fetchone()
            if result:
                return result


def get_developers_for_game_db(con, game_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    SELECT d.* 
                    FROM developers d 
                    INNER JOIN game_developers gd ON d.id = gd.developer_id 
                    WHERE gd.game_id = %s
                """,
                (game_id,)
            )
            result = cursor.fetchall()
            if result:
                return result
            raise GameNotFoundError()


def get_games_by_developer_db(con, developer_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                    SELECT g.* 
                    FROM games g 
                    INNER JOIN game_developers gd ON g.id = gd.game_id 
                    WHERE gd.developer_id = %s
                """,
                (developer_id,)
            )
            result = cursor.fetchall()
            if result:
                return result
            raise DeveloperNotFoundError()
