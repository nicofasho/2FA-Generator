import os.path
import sqlite3
import logging
from helpers import check_code_exists_in_db, generate_code_str
from setup import create_db


def generate_code() -> str:

    logging.basicConfig(level=logging.INFO)

    if not os.path.exists('wordlist.db'):
        logging.info("Wordlist DB does not exist, let's create it")
        con = sqlite3.connect('wordlist.db')
        cur = con.cursor()
        create_db(con, cur)
        con.close()
        logging.info('DB Created')

    logging.info("DB exists, leggo")

    code = generate_code_str()

    logging.info(f"Code generated: {code}")

    con = sqlite3.connect('wordlist.db')
    cur = con.cursor()

    while check_code_exists_in_db(code, cur):
        code = generate_code_str()
        logging.info(f'Previously generated code found, new code: {code}')

    cur.execute(f"INSERT INTO codes VALUES(?)", [code])
    con.commit()

    cur.execute("SELECT * FROM codes")
    if len(cur.fetchall()) == 16**8:
        cur.execute("DROP TABLE codes")
        create_db(con, cur)

    con.close()

    return code


if __name__ == "__main__":
    generate_code()
