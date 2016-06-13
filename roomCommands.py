#! /usr/bin/env python2
import requests
import json

CHARU_AUTHENTICATION_KEY="Bearer MTBkOWJlZjktNDVlMC00OTQyLTg2MjgtMDU3MmYzZDk0ODczOTQyM2RjOWYtZDE0"

def create_room(room_name):
    url = 'https://api.ciscospark.com/v1/rooms'
    headers = {
        'Authorization': CHARU_AUTHENTICATION_KEY
    }
    params = {
        'title': room_name
    }
    users_json = requests.post(url, headers=headers, data=params).json()
    room_id = users_json['id']
    return room_id

def delete_room():
    print "do other thing"

def add_members_to_room(room_id, room_members):
    search_url = "https://api.ciscospark.com/v1/people"
    join_url = "https://api.ciscospark.com/v1/memberships"
    for member in room_members:
        headers = {
            'Authorization': CHARU_AUTHENTICATION_KEY
        }
        params = {
            'displayName': member
        }
        count =0
        matching_members = requests.get(search_url, headers=headers, params = params).json()
        for matched_member in matching_members['items']:
            print matched_member['displayName']
            count+= 1
        if count ==1:
            add_params = {
                'roomId': room_id,
                'personId':matching_members['items'][0]['id']
            }
            membership_create_response = requests.post(join_url, headers=headers, data=add_params).json()
            print membership_create_response


room_members = ["Christopher Chon"]
rname = "test_room"
room_id = create_room(rname)
add_members_to_room(room_id, room_members)