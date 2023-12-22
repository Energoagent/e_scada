import json

TTTT={'ok': True, 'result': {'message_id': 34, 'sender_chat': {'id': -1002039512265, 'title': 'GercenInfo', 'type': 'channel'}, 'chat': {'id': -1002039512265, 'title': 'GercenInfo', 'type': 'channel'}, 'date': 1702326779, 'text': 'TEST'}}
#sartphone_dict = json.loads(TTTT)
result=TTTT["result"]

Message_id=result["message_id"]
# verify the type of the resulting variable
print(Message_id) # dict