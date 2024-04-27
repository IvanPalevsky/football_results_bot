import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def get_results_info(self):
        sql = 'SELECT * FROM results' 

        return self.__select_data(sql=sql)[0]

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def get_result_date(self, date):
        sql='SELECT * FROM results WHERE date = ?'
        return self.__select_data(sql, [date,])
            
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)