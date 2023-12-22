from config import * 
from DB import * 
from Alarms import *
import logging



#Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")
def main():
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)s:%(asctime)s %(message)s', filename="alarm_log.log",filemode="a")
    logging.info('START  ALARM SENDED')
    Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")        
    GercenAlarms=Alarms(Db,TOKEN, chat_id)
    GercenAlarms.SendAndCheckAlarmsSended()
    GercenAlarms.DeleteOldSendedAlarms()
    logging.info('STOP ALARM SENDED') 
    Db.Close()     
#    finally:





if __name__ == "__main__":
    main()
    
