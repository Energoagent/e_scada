#from icecream import ic
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import AsIs

class  DatabaseWork:
    
    def __init__(self,  dbname,host,user,password):
        self.dbname=dbname
        self.host=host
        self.user=user
        self.password=password
        self.connection=None
        self.cursor=None
    def ConnectToDatabase(self):
        try: #  Подключиться к существующей базе данных
            self.connection = psycopg2.connect(dbname=self.dbname,  host=self.host, user=self.user, password=self.password)
            print('Connection to DB OK',self.connection)
            self.connection.autocommit = True
#            ic(self.connection)
            return self.connection
        except Exception as e:
            print(e)
            self.connection=None
            print('DB Not exist')
            quit()
    def Close(self):
        if self.connection:
            self.connection.close()
            self.connection=None
            self.cursor=None
#            print("Соединение с PostgreSQL закрыто")  

    def OpenCursor(self,connection):
        try: # Открыть курсор
            cursor = connection.cursor()
            return cursor
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)  
            
    def ReadFromDatabase(self,SqlString):
#        ic(self.connection)
        Rows=None
        RowsCount=0
        if self.connection is None  or self.connection.closed != 0:
#            print("ReadFrom Database",self.connection)
            self.connection=self.ConnectToDatabase()
#            ic(self.connection.closed)
        if self.cursor is None:
            self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(SqlString)
            Rows=self.cursor.fetchall()
            RowsCount=self.cursor.rowcount
        except (Exception, Error) as error:
            self.Close()
#        print(Rows, RowsCount)
        return Rows, RowsCount
    
    def ExecuteInDatabase(self,SqlString):
        
        if self.connection is None or self.connection.closed != 0:
            self.connection=self.ConnectToDatabase()
#            ic(self.connection.closed)
#            ic(self.connection.status)
        if self.cursor is None:
            self.cursor = self.connection.cursor()
        self.cursor.execute(SqlString)
        self.connection.commit()

