from config import * 
from DB import * 
from Alarms import *
import logging



#Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")
def main():
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)s:%(asctime)s %(message)s',encoding='utf-8', filename="alarm_log.log",filemode="a")
    logging.info('START')
    Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")        
    GercenAlarms=Alarms(Db,TOKEN, chat_id)
    MyAlarms=GercenAlarms.ReadCurrentAlarms()
    for Alarm in MyAlarms:
        logging.debug(Alarm)
#        
    Db.Close()     
#    finally:





if __name__ == "__main__":
    main()
    
