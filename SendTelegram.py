import requests
import logging
import json

class  SendTelegramMessage:

    def __init__(self,  token,chat_id):
        self.token=token
        self.chat_id=chat_id

    def SendMessage(self,message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}"
        request=requests.get(url).json()       # Эта строка отсылает сообщение
        result=request["result"]
        MessageID=result["message_id"]
#        logging.debug(request)
        return MessageID,request
    def DeleteMessage(self,MessageID):
        url = f"https://api.telegram.org/bot{self.token}/deleteMessage?chat_id={self.chat_id}&message_id={MessageID}"
        request=requests.get(url).json()
#        print(request)
#        MessageID=result["message_id"]
#        logging.debug(request)
        return request
