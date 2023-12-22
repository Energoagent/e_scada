from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
#from icecream import ic
import json
import datetime
from email.message import Message
from  datetime  import datetime
import codecs
import logging
from db import * 
from Alarms import * 
from config import * 
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import AsIs

#Определяем константы
TAGPAGE =1
PAGE    =2
ALARMS  =3
FILE    =4
DATA    =5

LOWARN          =1  
HIWARN          =2  
LOALARM         =3  
HIALARM         =4  
STATUS_GOOD     =0
WARN_STATUS     =1
ALARM_STATUS    =2

PORT=8686

def run(server_class=ThreadingHTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', PORT)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()


 

def CheckStatus(var):
    VarValue=int(var[0])/var[10]
    LoAlarm=var[2]
    LoWarn=var[3]
    HiWarn=var[4]
    HiAlarm=var[5]
 #   ic(var)
    Status=STATUS_GOOD
    if(HiAlarm is not None and int(VarValue) >=HiAlarm/var[10]) : 
        VarStatus1=HIALARM
        Status= ALARM_STATUS               
    elif(LoAlarm is not None and int(VarValue)<=LoAlarm/var[10]) : 
        VarStatus1=LOALARM    
        Status= ALARM_STATUS               
    elif(HiWarn is not None and int(VarValue)>=HiWarn/var[10]) : 
        VarStatus1=HIWARN   
        Status= WARN_STATUS               
    elif(LoWarn is not None and int(VarValue)<=LoWarn/var[10]) : 
        VarStatus=LOWARN
        Status= WARN_STATUS
    
    return VarValue,Status             
      
    
def ReadWindowVariables(Db,WindowId):
    Variables=[]

        
 #   sqlstring="select tagname, value, timestamp from  solar.tag_last_value lv, solar.a_bus_tagsdescription td, "
 #   sqlstring=sqlstring+"solar.windowtag wt  where  lv.tag = td.tagname and td.tagname=wt.tagid  and wt.windowid={} ".format(WindowId)
    sqlstring="select  value,td.*, timestamp from  solar.tag_last_value lv, solar.a_bus_tagsdescription td,solar.windowtag wt "
    sqlstring=sqlstring+"WHERE( td.tagname=lv.tag and wt.tagid=lv.tag and wt.windowid={});".format(WindowId)
        


#    ic(sqlstring)
    Rows, RowsCount=Db.ReadFromDatabase(sqlstring)
    for row in Rows:
        Variables.append(row)
    return Variables

def GetWindowData(Db,WindowId):
    logging.debug('start %s', datetime.now())
    d=[]
    Variables=ReadWindowVariables(Db,WindowId)
    logging.debug('end %s', datetime.now())        
    for Var in Variables:

        Value,Status=CheckStatus(Var)
        if(Status==ALARM_STATUS ):
            TagColor='red'
        elif (Status==WARN_STATUS ):
            TagColor='orange'
        else:
            TagColor='black'
 #       print(Var[1],Value,Status,TagColor)            
        d.append({"ID": Var[1], "Value": Value, "color": TagColor})
    return d    

def ParseRequestLine(requestline):
    requestline=requestline.lower()
    logging.debug('requestline=%s',requestline)
    if(position:=requestline.find('/parameter/?page=')>0):
        Selector=TAGPAGE
        SelectorParam=requestline[position+21]
        if( not SelectorParam.isdigit()):
            return None,None
        return Selector,SelectorParam
    elif (position:=requestline.find(' / ')>0):
        Selector=PAGE
        SelectorParam='0'
#        if SelectorParam==' ':SelectorParam=0
        return Selector,SelectorParam
    elif (position:=requestline.find('page_')>0):
        Selector=PAGE
        SelectorParam=requestline[position+9]
        if(not SelectorParam.isdigit()):
            return None,None
        return Selector,SelectorParam
    elif (position:=requestline.find('alarms')>0):
        Selector=ALARMS
        SelectorParam=0
        logging.debug('ALARMS')
        return Selector,SelectorParam
    elif (position:=requestline.find('static')>0):
        Selector=FILE
        SelectorParam=requestline[position+11:]
        SelectorParam=SelectorParam[:SelectorParam.find(' ')]
        logging.debug('FILE %s',SelectorParam)
        return Selector,SelectorParam    
    elif (position:=requestline.find('data')>0):
        Selector=DATA
        SelectorParam=requestline[position+11:]
        SelectorParam=SelectorParam[:SelectorParam.find(' ')]
        logging.debug('FILE %s',SelectorParam)
        return Selector,SelectorParam    

    return None, None

            
class HttpProcessor(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*'); 
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # POST 
    def do_POST(self):
        print(self.requestline)
        starttime=datetime.now()
        Selector,SelectorParam=ParseRequestLine(self.requestline)
        logging.debug('Selector=%s,SelectorParam=%s',Selector,SelectorParam)
        if Selector==TAGPAGE:
            d=GetWindowData(Db1,SelectorParam)
            self.send_response(200)
            self._set_headers()
#            print(d)
            self.wfile.write(json.dumps(d).encode())
        elif  Selector== PAGE:
            i=1
        elif Selector== ALARMS:
            self.Send_Alarms()
        elif Selector== DATA:
            self.ParceDataRequest()    
            
        endtime=datetime.now()
        print('POST TotalTime=',endtime-starttime, 'requestline=', self.requestline, 'SelectorParam=',  SelectorParam)
        logging.debug('POST TotalTime=%s requestline=%s,  SelectorParam=%s',endtime-starttime, self.requestline, SelectorParam)
        
        
        
    def do_GET(self):
        starttime=datetime.now()
        Selector,SelectorParam=ParseRequestLine(self.requestline)
        logging.debug('Selector=%s,SelectorParam=%s',Selector,SelectorParam)
        if Selector==TAGPAGE:
            pass
#            d=GetWindowData(Db1,SelectorParam)
#            self.send_response(200)
#            self._set_headers()
#            self.send_header('Content-type', 'application/json')   
#            print(d)         
#            self.wfile.write(json.dumps(d).encode())
        elif  Selector== PAGE:
#            print(SelectorParam, PAGE,SelectorParam.isdigit())
            if(SelectorParam=='0'):           #Загружаем стартовую страницу
                PageFile="page_1.html"            
            elif(SelectorParam.isdigit()):
                PageFile="page_{}.html".format(SelectorParam)
                print(PageFile)
            else:
                return
            print(PageFile)
            with codecs.open( PageFile, "r", 'utf-8' ) as fp:
                
                # считываем сразу весь файл
                data = fp.read()
                fp.close()
            self.send_response(200)
            self._set_headers()
            self.send_header('Content-type', 'text/html' )
            self.send_header( 'charset', 'utf-8')
            self.wfile.write(data.encode('cp1251'))
        elif Selector== ALARMS:
            logging.debug('GET ALARMS')
            self.Send_Alarms()
        elif Selector== FILE:
            PageFile="./static/"+SelectorParam
            logging.debug('FILE %s',PageFile)
            with codecs.open( PageFile, "r", 'utf-8' ) as fp:
                
                # считываем сразу весь файл
                data = fp.read()
                fp.close()
            self.send_response(200)
            self._set_headers()
            self.send_header('Content-type', 'application/javascript' )
            self.send_header( 'charset', 'utf-8')
            self.wfile.write(data.encode('cp1251'))
        elif Selector== DATA:
            self.ParceDataRequest()    
        endtime=datetime.now()
        logging.debug('GET TotalTime=%s requestline=%s,  SelectorParam=%s',endtime-starttime, self.requestline, SelectorParam)
    def Send_Alarms(self):
            d=[]            
            GercenAlarms=Alarms(Db1,TOKEN, chat_id)
            CurrentAlarms=GercenAlarms.ReadCurrentAlarms()
            for Alarm in CurrentAlarms:
                print(Alarm)               
                d.append({"Type":Alarm[1],"ID": Alarm[2].strip(), "Value": Alarm[3], "t_raise": Alarm[4].strftime('%H:%M:%S %d.%m.%Y'),"m_raise": Alarm[0].strip(),"t_gone": None,"m_gone": Alarm[6]})
            self.send_response(200)
            self._set_headers()
            self.wfile.write(json.dumps(d).encode())
#            print(d)
    def ParceDataRequest(self):
        d=[]
        m = Message()
        m['content-type'] = self.headers.get('content-type')
        logging.debug("get_params=%s,charset=%s,content-type=%s",m.get_params(),m.get_params('charset'),m['content-type'])
        print(m.get_params())
        print(m.get_param('charset'))        
        print(m['content-type'])
        if(self.headers.get('content-length') is None):
            print("JSON отсутствует") 
            return
        length = int(self.headers.get('content-length'))
        print('L=',length)
        message = json.loads(self.rfile.read(length))
        Tag=message['parameterName']
        print(message)
        print(Tag)
        StartDate=message['periodStart']
        EndDate=message['periodEnd']
        if (StartDate=="datetime"):StartDate='2023-12-22 14:10:42'
        if (EndDate=="datetime"):EndDate='2023-12-22 14:25:42'        
        
        # refuse to receive non-json content
#        if ctype != 'application/json':
#            self.send_response(400)
#            self.end_headers()
#            return
            
        # read the message and convert it into a python dictionary
        
                    
        sqlstring="select  tag, timestamp,value,scale,lowarn,hiwarn,loalarm,hialarm from  solar.measurements ms, solar.a_bus_tagsdescription td  "
        sqlstring=sqlstring+"WHERE td.tagname=ms.tag and  tag='{}' and timestamp between  '{}' and '{}';".format(Tag,StartDate,EndDate)



#    ic(sqlstring)
        Rows, RowsCount=Db1.ReadFromDatabase(sqlstring)
        for row in Rows:
            loWarn=row[4]/row[3]
            hiWarn=row[5]/row[3]
            loAlarm=row[6]/row[3]
            hiAlarm=row[7]/row[3]
            d.append([row[1].strftime('%H:%M:%S %d.%m.%Y'),int(row[2])/row[3]])
        out={"parameterName":Tag,"loWarn": loWarn, "hiWarn": hiWarn,"loAlarm": loAlarm,"hiAlarm": hiAlarm,"values":d}
        self.send_response(200)
        self.send_header('Content-type', 'application/json' )
        self._set_headers()
        self.wfile.write(json.dumps(out).encode())
#        print(out)




Db1=DatabaseWork(dbname=DBNAME,  host=HOST, user=USER, password=PASSWORD)            
#Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")
def main():
   
#    Db=DatabaseWork(dbname="postgres",  host="192.168.22.21", user="solar", password="solar")
    logging.basicConfig(level=logging.DEBUG,format='%(levelname)s:%(asctime)s %(message)s', filename="./log/HTTPServer.log",filemode="w")
    logging.info('START HTTP Server')
    run(ThreadingHTTPServer, HttpProcessor)
    Db1.Close()     
    logging.info('STOP HTTP Server')
#    finally:





if __name__ == "__main__":
    main()
