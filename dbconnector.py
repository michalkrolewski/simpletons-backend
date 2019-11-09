import psycopg2
from config import config


class DBConnector:

    def __init__(self):
        self.connection_params = config('configs/database.ini', 'postgresql')

        self.sql_select_from_users = 'SELECT * FROM USERS WHERE id = {0}'
        self.sql_insert_into_users = ''

        self.sql_select_from_categories = ''
        self.sql_insert_into_categories = ''

        self.sql_select_from_fiszki = ''
        self.sql_insert_into_fiszki = ''

    def selectFromUsers(self, ids):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_select_from_users.format(ids))
            rows = cur.fetchall()
            cur.close()
            return rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
