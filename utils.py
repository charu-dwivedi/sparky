import requests
import json

with open('developer_tokens.json') as data:
    developer_tokens = json.load(data)

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
        users.append((user['personDisplayName'], user['personEmail']))
    return users

def get_email_user(token, room_id):
    legit_token = "Bearer " + token
    url = 'https://api.ciscospark.com/v1/memberships'
    headers = {
        'Authorization': legit_token
    }
    params = {
        'roomId': room_id
    }
    users_json = requests.get(url, headers=headers, params=params).json()
    email_to_user = {}
    for user in users_json['items']:
        email_to_user[user['personEmail']] = user['personDisplayName']
    return email_to_user

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

"""
Use these functions
"""
# returns messages from a room
def get_messages_for_user(user, room_name):
    if user not in developer_tokens:
        raise Exception("User {} doesn't exist".format(user))
    return get_messages(developer_tokens[user], get_roomid(room_name, developer_tokens[user]))

# returns users, email tuple in a room
def get_users_for_room(user, room_name):
    if user not in developer_tokens:
        raise Exception("User {} doesn't exist".format(user))
    return get_users(developer_tokens[user], get_roomid(room_name, developer_tokens[user]))

# returns a dictionary with email-username pairs
def get_emails_with_users(user, room_name):
    if user not in developer_tokens:
        raise Exception("User {} doesn't exist".format(user))
    return get_email_user(developer_tokens[user], get_roomid(room_name, developer_tokens[user]))
