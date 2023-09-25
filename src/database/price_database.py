from sqlite3 import Connection


class PricesDatabase:
    def __init__(self, con: Connection):
        self.conn = con
        self.cur = self.conn.cursor()
        self.create_table()

    def __del__(self):
        self.cur.close()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS prices (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ot INTEGER,
                                do INTEGER
                            )''')
        self.conn.commit()

    def add_price_range(self, id, ot, do):
        if not self.check_prices_exists(id):
            #print(f"Строка с id {id} уже существует в таблице.")
            self.cur.execute("UPDATE prices SET ot=?, do=? WHERE id=?", (ot, do, id,))
            return False
        self.cur.execute("INSERT INTO prices (id, ot, do) VALUES (?, ?, ?)", (id, ot, do,))
        self.conn.commit()
        return True

    def get_price_range_by_id(self, price_id):
        if not self.check_prices_exists(id):
            #print(f"Строка с id {id} уже существует в таблице.")
            return None
        self.cur.execute("SELECT ot, do FROM prices WHERE id=?", (price_id,))
        return self.cur.fetchone()

    def delete_price_range_by_id(self, price_id):
        self.cur.execute("DELETE FROM prices WHERE id=?", (price_id,))
        self.conn.commit()
        return True

    def get_price_ranges_by_price(self, price):
        self.cur.execute("SELECT * FROM prices WHERE ? BETWEEN ot AND do", (price,))
        return self.cur.fetchall()
    
    def check_prices_exists(self, id):
        try:
            self.cur.execute("SELECT * FROM prices WHERE id = ?", (id,))
        except Exception as e:
            #print(e)
            return False
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False