import sqlalchemy as sqla
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
# define declarative base
Base = declarative_base()


class sqlalchemyDemo:
    
    def __init__(self):
        pass  
    
    def query_sqlite3(self):
        sqlite_db = sqla.create_engine('sqlite:///mydata.sqlite')
        result = pd.read_sql('select * from test', sqlite_db)
        print (result)
        
    def query_mysql(self):
        engine = sqla.create_engine('mysql://root:password@localhost/classicmodels') 
        engine.execute("USE Classicmodels") 
        metadata = sqla.MetaData(engine)
        metadata.reflect()

        class User(Base):
            __table__ = sqla.Table("employees", metadata)
    
        # call the session maker factory
        Session = sqla.orm.sessionmaker(engine)
        session = Session()

        # filter a record 
        result = session.query(User).filter().first()
        print (result.firstName)
        
def main():
    s = sqlalchemyDemo() 
    s.query_sqlite3()
    s.query_mysql()
 
 
if __name__=='__main__':
	main()