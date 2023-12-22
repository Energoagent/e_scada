import csv
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import AsIs
from icecream import ic

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
            print('Connection to DB OK')
            ic(self.connection)
            return self.connection
        except Exception as e:
            ic(e)
            print('DB Not exist')
            quit()
    def Close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection=None
            self.cursor=None
        print("Соединение с PostgreSQL закрыто")  

    def OpenCursor(self,connection):
        try: # Открыть курсор
            cursor = connection.cursor()
            return cursor
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)  
    def ReadFromDatabase(self,SqlString):
        ic(self.connection)
        if self.connection is None:
            self.connection=self.ConnectToDatabase()
            ic(self.connection.closed)
        if self.cursor is None:
            
            cursor = self.connection.cursor()
        cursor.execute(SqlString)
        Rows=cursor.fetchall()
        RowsCount=cursor.rowcount
        return Rows, RowsCount
    def ExecuteInDatabase(self,SqlString):
        
        if self.connection is None:
            self.connection=self.ConnectToDatabase()
            ic(self.connection.closed)
            ic(self.connection.status)
        if self.cursor is None:
            cursor = self.connection.cursor()
        cursor.execute(SqlString)
        self.connection.commit()
        
        RowsCount=cursor.rowcount
        return RowsCount
    
def ReadCSV1(CSVFileName,delimiter):   
    sqlstring=[]
    Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")        
    with open(CSVFileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
#        sqlstring="INSERT INTO solar.windowtag (tagid,windowid) VALUES "
#        sqlstring=sqlstring+"('{}',{}),".format(row[0],row[1])
#	 
#	
#        sqlstring="update solar.a_bus_tagsdescription set loalarm={}}, sendmessage1={}},lowarn={}}, sendmessage2={}},"
#        sqlstring=sqlstring+"hiwarn={}},sendmessage3={}},hialarm={}}, sendmessage4={}},  scale=1 WHERE tagname={};".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
        for row in spamreader:
            ic(row)
        #    ic(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            sqlstring="update solar.a_bus_tagsdescription set " 
            if(row[1] !=''): 
                sqlstring=sqlstring+"tagdescription='{}', ".format(row[1])
            else:
                sqlstring=sqlstring+"hialarm=NULL,"            
            if(row[2]!=''): 
                sqlstring=sqlstring+"loalarm={},".format(row[2]) 
            else:
                sqlstring=sqlstring+"loalarm=NULL,"
            if(row[3] !=''): 
                sqlstring=sqlstring+"lowarn={}, ".format(row[3])
            else:
                sqlstring=sqlstring+"lowarn=NULL,"

            if(row[4] !=''): 
                sqlstring=sqlstring+"hiwarn={}, ".format(row[4])
            else:
                sqlstring=sqlstring+"hiwarn=NULL,"

            if(row[5] !=''): 
                sqlstring=sqlstring+"hialarm={},".format(row[5])
            else:
                sqlstring=sqlstring+"hialarm=NULL,"
             
            sqlstring=sqlstring[:-1]+ "  WHERE tagname='{}';".format(row[0])
            ic(sqlstring)
            Db.ExecuteInDatabase(sqlstring)
        
    
        Db.Close

def ReadCSV2(CSVFileName,delimiter):   
    sqlstring=[]
    Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")        
    with open(CSVFileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
	
	
#        sqlstring=sqlstring+"('{}',{}),".format(row[0],row[1])
#	 
#	
#        sqlstring="update solar.a_bus_tagsdescription set loalarm={}}, sendmessage1={}},lowarn={}}, sendmessage2={}},"
#        sqlstring=sqlstring+"hiwarn={}},sendmessage3={}},hialarm={}}, sendmessage4={}},  scale=1 WHERE tagname={};".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
        for row in spamreader:
            sqlstring="INSERT INTO solar.a_bus_tagsdescription (tagname, loalarm,sendmessage1, lowarn,sendmessage2, hiwarn,sendmessage3, hialarm, sendmessage4, pulltime, cybrono, scale) "
            sqlstring=sqlstring+"VALUES ('{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],5,16532,10)        
	
            ic(row)
            Db.ExecuteInDatabase(sqlstring)
        
    
        Db.Close

#Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")
def main():
   

    
    ReadCSV1("123.csv",';')
#    ReadCSV("Windowtag.csv",',')
        
#    finally:
    





if __name__ == "__main__":
    main()