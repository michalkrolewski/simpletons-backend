import psycopg2
from configs.config import config
from db.dbparser import *


class DBConnector:

    def __init__(self):
        self.connection_params = config('configs/database.ini', 'postgresql')

        self.sql_select_from_users = 'SELECT * FROM USERS WHERE id = {0}'
        self.sql_insert_into_users = 'INSERT INTO USERS(username, email, password, firstname) VALUES({0}) RETURNING id'

        self.sql_select_from_categories = 'SELECT * FROM CATEGORIES WHERE user_id IS NULL'
        self.sql_select_from_categories_simple = 'SELECT * FROM CATEGORIES WHERE id = {0}'
        self.sql_insert_into_categories = ''

        self.sql_select_from_fiszki = 'SELECT * FROM FISZKI WHERE category_id = {0} '
        self.sql_insert_into_fiszki = ''

    def getUser(self, id):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_select_from_users.format(id))
            row = cur.fetchone()
            cur.close()
            return parseUser(row)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def createUser(self, user):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_insert_into_users.format(user.__str__()))
            rows = cur.fetchone()
            conn.commit()
            cur.close()
            return rows[0]  # returns created user id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def getCategories(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_select_from_categories)
            rows = cur.fetchall()
            cur.close()
            return parseCategories(rows)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def getCategory(self, id):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_select_from_categories_simple.format(id))
            row = cur.fetchone()
            cur.close()
            return parseCategory(row)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def getFiszkiByCategory(self, category_id):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_select_from_fiszki.format(category_id))
            rows = cur.fetchall()
            cur.close()
            return parseFiszki(rows)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
