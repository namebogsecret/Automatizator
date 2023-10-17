
import time

class Database_Simple_Table:
    def __init__(self, sql, table_name: str):
        self.connection = sql
        self.table_name = table_name
    
    def _get_cursor(self):
        return self.connection.cursor()
    
    def check_if_exists(self, user_id):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM {} WHERE id=%s".format(self.table_name), (user_id,))
        row = cursor.fetchone()
        return row is not None
    
    def add_to_table(self, user_id):
        cursor = self._get_cursor()
        current_time = time.time()
        cursor.execute("INSERT INTO {} (id, timestamp) VALUES (%s, %s)".format(self.table_name), (user_id, current_time))
        self.connection.commit()
    
    def delete_from_table(self, user_id):
        cursor = self._get_cursor()
        cursor.execute("DELETE FROM {} WHERE id=%s".format(self.table_name), (user_id,))
        self.connection.commit()
    
    def delete_all_from_table(self):
        cursor = self._get_cursor()
        cursor.execute("DELETE FROM {}".format(self.table_name))
        self.connection.commit()
