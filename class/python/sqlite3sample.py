import sqlite3

class sqlite3sample:
    def __init__(self):
        con = sqlite3.connect('mydata.sqlite') 
    
    def create_table(self):
        query = """
        CREATE TABLE test
        (a VARCHAR(20), b VARCHAR(20),
        c REAL,        d INTEGER
        );"""
        # con = sqlite3.connect('mydata.sqlite')
        con.execute(query)
        con.commit()
        
    def insert_data(self):
        con = sqlite3.connect('mydata.sqlite')
        data = [('Atlanta', 'Georgia', 1.25, 6),
        ('Tallahassee', 'Florida', 2.6, 3),
        ('Sacramento', 'California', 1.7, 5)]
        stmt = "INSERT INTO test VALUES(?, ?, ?, ?)"
        con.executemany(stmt, data)
        con.commit()
    
    def query(self, sql="select * from test"):
        con = sqlite3.connect('mydata.sqlite')
        cursor = con.execute(sql)
        rows = cursor.fetchall()
        print(rows)
        
def main():
    s = sqlite3sample() 
    # s.create_table()
    s.insert_data()
    s.query()
 
 
if __name__=='__main__':
	main()