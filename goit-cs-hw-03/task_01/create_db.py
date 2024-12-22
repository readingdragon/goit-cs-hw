import psycopg2
from psycopg2 import sql


def create_db():
    try:
    # читаємо файл зі скриптом для створення БД
        with open('postgres_db/tms.sql', 'r') as f:
            sql = f.read()

        connection_params = {
            'dbname': 'postgres',
            'user': 'dev',
            'password': 'pass4db',
            'host': 'localhost',
            'port': 5432
        }
    # створюємо з'єднання з БД
        with psycopg2.connect(**connection_params) as con:
            with con.cursor() as cur:
    # виконуємо скрипт із файлу, який створить таблиці в БД
             cur.execute(sql)
             con.commit()
             print('Tables created successfully.')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    create_db()
