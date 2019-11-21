import psycopg2
from configs.config import config
from db.dbparser import *


class DBConnector:

    def __init__(self):
        self.connection_params = config('configs/database.ini', 'postgresql')

        self.sql_select_from_users = 'SELECT * FROM USERS WHERE id = {0}'
        self.sql_select_from_users_by_username = 'SELECT * FROM USERS WHERE username=(%s)'
        self.sql_insert_into_users = 'INSERT INTO USERS(username, email, password, firstname) VALUES({0}) RETURNING id'

        self.sql_select_from_categories = 'SELECT * FROM CATEGORIES WHERE user_id IS NULL'
        self.sql_select_from_categories_by_user_id = 'SELECT * FROM CATEGORIES WHERE user_id = {0}'
        self.sql_select_from_categories_simple = 'SELECT * FROM CATEGORIES WHERE id = {0}'
        self.sql_select_from_categories_by_user_and_name = 'SELECT * FROM CATEGORIES WHERE user_id = {0} AND name = \'{1}\''
        self.sql_insert_into_categories = 'INSERT INTO CATEGORIES(user_id, name) VALUES({0}) RETURNING id'

        self.sql_select_from_fiszki = 'SELECT * FROM FISZKI WHERE category_id = {0} '
        self.sql_insert_into_fiszki = 'INSERT INTO FISZKI(category_id, src_lang, src_text, target_lang, target_text) VALUES {0} RETURNING id'

    def getUserById(self, id):
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

    def getUserByUsername(self, username):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_select_from_users_by_username, (username,))
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
            row = cur.fetchone()
            conn.commit()
            cur.close()
            return row[0]  # returns created user id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def getPublicCategories(self):
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

    def getPrivateCategories(self, id):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_select_from_categories_by_user_id.format(id))
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

    def getCategory(self, id, name):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self. sql_select_from_categories_by_user_and_name.format(id, name))
            row = cur.fetchone()
            cur.close()
            return parseCategory(row)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    def createCategory(self, category):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            cur.execute(self.sql_insert_into_categories.format(category.__str__()))
            row = cur.fetchone()
            conn.commit()
            cur.close()
            return row[0]  # returns created category id
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

    def createFiszki(self, fiszki):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            cur = conn.cursor()
            values = ""
            for fiszka in fiszki:
                values += fiszka.__str__() + ","
            values = values[:-1]
            cur.execute(self.sql_insert_into_fiszki.format(values))
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            return rows  # returns created ids
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
