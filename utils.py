import requests
import json

developer_tokens = {'tanay': 'YjA2OGJlOGMtZmMwYi00N2NjLWE4NmItNjg3NDUwZjllNTY1YjVhZWUzODEtNDU0',
                    'chris': 'NmU5NDA1YjctY2Q2Ni00MDcyLWE0YTItMWUyYWMzNjZiNWM0YmQ0ZjgyNTctZDQz',
                    'charu': 'MTBkOWJlZjktNDVlMC00OTQyLTg2MjgtMDU3MmYzZDk0ODczOTQyM2RjOWYtZDE0'}

def get_users(token, room_id):
    legit_token = "Bearer " + token
    url = 'https://api.ciscospark.com/v1/memberships'
    headers = {
        'Authorization': legit_token
    }
    params = {
        'roomId': room_id
    }
    users_json = requests.get(url, headers=headers, params=params).json()
    users = []
    for user in users_json['items']:
        print user['personDisplayName']
        users.append(user['personDisplayName'])
    return users

def get_messages(token, room_id, before=None, before_msg=None, max_msgs=float('inf')):
    legit_token = "Bearer " + token
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {
        'Accept': 'application/json',
        'Authorization': legit_token
    }
    params = {
        'roomId': room_id
    }
    if (max_msgs < float('inf') and max_msgs > 1):
        params['max'] = max_msgs
    if (before != None and before_msg != None):
        raise Exception('Can\'t have before and before_msg')
    elif (before != None):
        params['before'] = before
    elif (before_msg != None):
        params['beforeMessage'] = before_msg
    return requests.get(url, headers=headers, params=params).json()

def get_rooms(token, max_rooms=float('inf'), room_type=None):
    legit_token = "Bearer " + token
    url = 'https://api.ciscospark.com/v1/rooms'
    headers = {
        'Accept': 'application/json',
        'Authorization': legit_token
    }
    params = {}
    if room_type != None:
        params['type'] = room_type
    if (max_rooms < float('inf') and max_rooms > 1):
        params['max'] = max_rooms
    return requests.get(url, headers=headers, params=params).json()

def get_room(room_name, token, max_msgs=float('inf'), room_type=None):
    for room in get_rooms(token, max_msgs, room_type)['items']:
        if room['title'] == room_name:
            return room

def get_roomid(room_name, token, max_msgs=float('inf'), room_type=None):
    return get_room(room_name, token, max_msgs=float('inf'), room_type=None)['id']

def get_messages_for_user(user, room_name):
    if user not in developer_tokens:
        raise Exception("User {} doesn't exist".format(user))
    return get_messages(developer_tokens[user], get_roomid(room_name, developer_tokens[user]))

#users = get_users(developer_tokens['tanay'], 'Y2lzY29zcGFyazovL3VzL1JPT00vYjhhMmFhYjAtMmU5Mi0xMWU2LTg0YWEtNWY1MGViMDZhMjAx')
#print get_messages(developer_tokens['tanay'], 'Y2lzY29zcGFyazovL3VzL1JPT00vYjhhMmFhYjAtMmU5Mi0xMWU2LTg0YWEtNWY1MGViMDZhMjAx')
#print get_roomid('dockerize teamgold services', developer_tokens['tanay'])
#print get_messages_for_user('tanay', 'dockerize teamgold services')