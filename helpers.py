import secrets
import sqlite3


def generate_code_str() -> str:
    code = f'{secrets.randbelow(16 ** 8):X}'
    while len(code) < 8:
        code = '0' + code

    return code


def check_code_exists_in_db(code: str, cur: sqlite3.Cursor) -> bool:
    cur.execute(f"SELECT * FROM codes WHERE code = '{code}'")
    return len(cur.fetchall()) > 0
