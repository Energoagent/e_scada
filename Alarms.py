from SendTelegram import *
import logging

class Alarms:
    def __init__(self,  Db, token,chat_id): 
        self.Db=Db
        self.Teleram=SendTelegramMessage(token,chat_id)
    def ReadAlarmListToSend(self):
        Alarms=[]
#        sqlstring="select  value,td.*, timestamp from  solar.tag_last_value lv, solar.a_bus_tagsdescription td,solar.windowtag wt "
#        sqlstring=sqlstring+"WHERE( td.tagname=lv.tag and wt.tagid=lv.tag and wt.windowid={});".format(WindowId)
        sqlstring="select message, id FROM solar.alarms_to_send"
        Rows, RowsCount=self.Db.ReadFromDatabase(sqlstring)
        for row in Rows:
            Alarms.append(row)
#            print(row[0])
            logging.debug("Текущая тревога для отправки в Telegram %s ",row[0])
#            print(row)
        return Alarms
    def ReadCurrentAlarms(self):
        Alarms=[]
#        sqlstring="select  value,td.*, timestamp from  solar.tag_last_value lv, solar.a_bus_tagsdescription td,solar.windowtag wt "
#        sqlstring=sqlstring+"WHERE( td.tagname=lv.tag and wt.tagid=lv.tag and wt.windowid={});".format(WindowId)
        sqlstring="select  message,type, tag, value, timestamp_raise, timestamp_gone, message_gone FROM solar.current_alarms"
        Rows, RowsCount=self.Db.ReadFromDatabase(sqlstring)
        for row in Rows:
            Alarms.append(row)
 #           print(row[0])
            logging.debug("Текущая тревога  %s ",row[0])
            print(row[0])
        return Alarms
    
    def CheklAlarmSended(self,AlarmId,T_MessageID):
        Alarms=[]
#        sqlstring="select  value,td.*, timestamp from  solar.tag_last_value lv, solar.a_bus_tagsdescription td,solar.windowtag wt "
#        sqlstring=sqlstring+"WHERE( td.tagname=lv.tag and wt.tagid=lv.tag and wt.windowid={});".format(WindowId)
        sqlstring="update solar.alarms set sended_raise=NOW(),id_t_mes={} where id={}".format(T_MessageID,AlarmId)
        logging.debug('Отмечаем тревогу отправленной sqlstring=%s',sqlstring)
#        sqlstring="select message, tag, timestamp_raise FROM solar.alarms_to_send where tag='{}' and type={} and timestamp_raise='{}'".format(AlarmTag,AlarmType, Timestamp_raise)
        self.Db.ExecuteInDatabase(sqlstring)
    
    
    def SendAndCheckAlarmsSended(self):
        AlarmList=self.ReadAlarmListToSend()
#        ic(AlarmList)
        for Alarm in AlarmList:
            MessageID,request=self.Teleram.SendMessage(Alarm[0])
            logging.debug("Alarm sended ----- %s, MessageID %s",Alarm[0],MessageID)
            self.CheklAlarmSended(Alarm[1],MessageID)
#        self.RemoveOldSendedAlarms()

    def DeleteOldSendedAlarms(self):
        sqlstring="select id_t_mes, id FROM solar.alarms_delete_old_message"
#        print(sqlstring)
        Rows, RowsCount=self.Db.ReadFromDatabase(sqlstring)
#        print(Rows)
        for row in Rows:
            print(row[0])
            request=self.Teleram.DeleteMessage(row[0])
#            print(request)
            sqlstring="update solar.alarms set id_t_mes=NULL where id={}".format(row[1])
            self.Db.ExecuteInDatabase(sqlstring)
            logging.debug("Telegram message deleted  %s ",row[0])
        return Alarms
#        AlarmList=self.ReadAlarmListToDelete()
