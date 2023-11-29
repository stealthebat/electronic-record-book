import pymysql
from data.auth_data import *


def add_text_to_label(new_text, text_label):
    current_text = text_label.cget("text")
    if current_text != '':
        new_text = current_text + "\n" + new_text
        text_label.configure(text=new_text)
    else:
        text_label.configure(text=new_text)


class Database:
    @staticmethod
    def get_connection() -> pymysql.Connection:
        try:
            connect = pymysql.connect(
                host=host,
                port=port,
                user=user,
                database=database,
                password=password,
                cursorclass=pymysql.cursors.DictCursor
            )
            return connect
        except Exception as ex:
            print(ex)

    def get_table(self, table: str) -> list[dict]:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                query = f"SELECT * FROM `{table}`"
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except Exception as ex:
            print(ex)
        finally:
            con.close()

    def get_row(self, table, id_title: str, id_value: int) -> list[dict]:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                query = f"SELECT * FROM `{table}` WHERE {table}.{id_title} = {id_value}"
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows
        except Exception as ex:
            print(ex)
        finally:
            con.close()

    def insert_data(self, table: str, data: str, keys: str) -> str:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                sql = f"INSERT INTO {table} {keys} VALUES {data}"
                cursor.execute(sql)
            con.commit()
            return "Successful insertion!"
        except Exception as ex:
            return f"Something went wrong! {ex}"
        finally:
            con.close()

    def delete_data(self, table: str, key: str, value: int) -> str:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                sql = f"DELETE FROM {table} WHERE {key}={value}"
                cursor.execute(sql)
            con.commit()
            return "Successful delete!"
        except Exception as ex:
            return f"Something went wrong! {ex}"
        finally:
            con.close()

    def update_the_data_in_the_table(self, keys: list, values: list, title: str) -> str:
        set_values = ", ".join([f"{keys[i]} = '{values[i]}'" for i in range(1, len(keys))])
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                query = f"UPDATE {title} SET {set_values} WHERE {keys[0]} = {values[0]};"
                cursor.execute(query)
            con.commit()
            return "Successful update!"
        except Exception as ex:
            return f"Something went wrong! {ex}"
        finally:
            con.close()

    def call_proc_get_exams_count_per_classroom(self) -> list or str:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                cursor.execute(
                    'CALL get_exams_count_per_classroom()'
                )
                res = cursor.fetchall()
                return res
        except Exception as ex:
            print(ex)
            return f"Something went wrong! {ex}"
        finally:
            con.close()

    def call_proc_get_youngest_students(self) -> list or str:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                cursor.execute(
                    "CALL get_youngest_students()"
                )
                res = cursor.fetchall()
                return res
        except Exception as ex:
            print(ex)
            return f"Something went wrong! {ex}"
        finally:
            con.close()

    def call_func_get_department_by_subject(self, subject_name_param) -> list or str:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                cursor.execute(
                    f"SELECT get_department_by_subject('{subject_name_param}')"
                )
                res = cursor.fetchall()
                return res
        except Exception as ex:
            print(ex)
            return f"Something went wrong! {ex}"
        finally:
            con.close()

    def call_func_get_student_average_grade(self, student_name: str) -> list or str:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                cursor.execute(
                    f'SELECT get_student_average_grade("{student_name}")'
                )
                res = cursor.fetchall()
                return res
        except Exception as ex:
            print(ex)
            return f"Something went wrong! {ex}"
        finally:
            con.close()

    def check_student(self, student_name: str) -> bool:
        try:
            con = self.get_connection()
            with con.cursor() as cursor:
                query = f"SELECT COUNT(1) FROM students WHERE name = '{student_name}';"
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows[0]['COUNT(1)'] != 0
        except Exception as ex:
            print(ex)
        finally:
            con.close()
