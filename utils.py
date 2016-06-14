import requests
import json

with open('developer_tokens.json') as data:
    developer_tokens = json.load(data)

"""
Internal Room Queries
"""
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
Internal Room Action Commands
"""
def create_room(token, room_name):
    legit_token = "Bearer " + token
    url = 'https://api.ciscospark.com/v1/rooms'
    headers = {
        'Authorization': legit_token
    }
    params = {
        'title': room_name
    }
    users_json = requests.post(url, headers=headers, data=params).json()
    room_id = users_json['id']
    return room_id

def delete_room(token, room_id):  
    legit_token = "Bearer " + token  
    url = 'https://api.ciscospark.com/v1/rooms/'+room_id
    headers = {
        'Authorization': legit_token
    }
    params = {
        'roomId': room_id
    }
    delete_output_code = requests.delete(url, headers=headers, params=params)
    return delete_output_code   

def add_members_to_room(token, room_id, room_members):
    legit_token = "Bearer " + token
    search_url = "https://api.ciscospark.com/v1/people"
    join_url = "https://api.ciscospark.com/v1/memberships"
    for member in room_members:
        headers = {
            'Authorization': legit_token
        }
        params = {
            'displayName': member
        }
        count =0
        matching_members = requests.get(search_url, headers=headers, params = params).json()
        for matched_member in matching_members['items']:
            count+= 1
        if count == 1:
            add_params = {
                'roomId': room_id,
                'personId':matching_members['items'][0]['id']
            }
            membership_create_response = requests.post(join_url, headers=headers, data=add_params).json()
        else: 
            print "Add functionality for multiple members!"

def change_room_name(token, old_name, new_name):
    legit_token = "Bearer " + token
    rooms = get_rooms(token)['items']
    for r in rooms:
        if r['title'] == old_name:
            update_url = 'https://api.ciscospark.com/v1/rooms/%s' % r['id']
            headers = {
                'Accept': 'application/json',
                'Authorization': legit_token
            }
            params = {
                'title': new_name
            }
            return requests.put(update_url, headers=headers, data=params).json()
    print 'Room \'%s\' could not be found' % old_name
    print 'No room updated'
    return None

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

# creates room and returns id of newly created room
def make_room(user, room_name):
    return create_room(developer_tokens[user], room_name)

# removes room and returns output code for delete
def remove_room(user, room_name):
    return delete_room(developer_tokens[user], get_roomid(room_name, developer_tokens[user]))

# adds room_members to room
def add_members(user, room_name, room_members):
    add_members_to_room(developer_tokens[user], get_roomid(room_name, developer_tokens[user]), room_members)

# changes an existing room's name and returns the output code (returns None if rooms doesn't exist)
def update_room_name(user, room_name, new_room_name):
    return change_room_name(developer_tokens[user], room_name, new_room_name)

##########################################

# users = get_users(developer_tokens['tanay'], 'Y2lzY29zcGFyazovL3VzL1JPT00vYjhhMmFhYjAtMmU5Mi0xMWU2LTg0YWEtNWY1MGViMDZhMjAx')
# print get_messages(developer_tokens['tanay'], 'Y2lzY29zcGFyazovL3VzL1JPT00vYjhhMmFhYjAtMmU5Mi0xMWU2LTg0YWEtNWY1MGViMDZhMjAx')
# print get_roomid('Hacker Squad', developer_tokens['chris'])
# print get_messages_for_user('chris', 'Hacker Squad')

# room_members = ["Christopher Chon", "Anjum Shaik", "Tanay Nathan"]
# rname = "test_room"
# print make_room('charu', rname)
# add_members('charu', rname, room_members)
# print remove_room('charu', rname)

# print update_room_name('chris', 'Hacker Squad', 'Chris Fan Club')
# print update_room_name('chris', 'Chris Fan Club', 'Sparky')
