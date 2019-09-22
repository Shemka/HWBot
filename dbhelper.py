import sqlite3


class DBHelper:
    def __init__(self, dbname="db.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self, columns):
        stmt = "CREATE TABLE IF NOT EXISTS items ({})".format(', '.join(['\''+column+'\'' for column in columns]))
        self.conn.execute(stmt)
        self.conn.commit()

    def update_item(self, items, subject_column):
        stmt = "SELECT * FROM items WHERE " + subject_column + "=" +"\'"+items[0]+"\'"
        item_ = [list(x) for x in self.conn.execute(stmt)]
        if len(item_) < 1:
            return False
        item_ = item_[0]
        print(item_[1], items[1])
        item_[1] += ' ' + items[1]
        item_[2] += ' ' + items[2]
        
        stmt = "DELETE FROM items WHERE "+subject_column+" = "+"\'"+items[0]+"\'"
        self.conn.execute(stmt)

        stmt = "INSERT INTO items VALUES ({})".format(', '.join(['\''+item+'\'' for item in item_]))
        self.conn.execute(stmt)
        self.conn.commit()

    def change_item(self, items, subject_column):
        stmt = "DELETE FROM items WHERE "+subject_column+" = "+"\'"+items[0]+"\'"
        self.conn.execute(stmt)
        stmt = "INSERT INTO items VALUES ({})".format(', '.join(['\''+item+'\'' for item in items]))
        self.conn.execute(stmt)
        self.conn.commit()

    def get_items(self, subject, subject_column):
        stmt = "SELECT * FROM items WHERE "+subject_column+" = "+"\'"+subject+"\'"
        return [x for x in self.conn.execute(stmt)]