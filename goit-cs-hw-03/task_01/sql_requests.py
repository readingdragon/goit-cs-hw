import psycopg2

# з'єднання з базою даних
def connection_db():
    connection = psycopg2.connect(
        dbname='postgres',
        user='dev',
        password='pass4db',
        host='localhost',
        port='5432'
    )
    return connection

# виконуємо SQL-запити з файлу по черзі
def execute_query(file_path: str):
    try:
        with open(file_path, 'r') as req:
            sql_commands = req.read().split(";")
        
        with connection_db() as connection:
            with connection.cursor() as cursor:
                for command in sql_commands:
                    command = command.strip()
                    if command:
                        print(f"Executing query:\n{command}\n")
                        cursor.execute(command)
                        
                        if cursor.description:
                            results = cursor.fetchall()
                            for row in results:
                                print(row)
                        else:
                            print("Query executed successfully, no results to fetch.")
                        print("-" * 50)
                        
                connection.commit()  
    except Exception as e:
        print(f"Error: {e}")

execute_query('postgres_db/SQL_requests.sql')



