#! /usr/bin/env python2
import os
import utils
import json
from collections import defaultdict

#Should run this when application opens to create all required files

with open('developer_tokens.json') as data:
    developer_tokens = json.load(data)

def load_users_and_groups():
    user_names = defaultdict(list)
    get_rooms_output =utils.get_rooms(developer_tokens['charu'])
    for room in get_rooms_output['items']:
        curr_id = room['id']
        users_in_room = utils.get_users(developer_tokens['charu'], curr_id)
        for users in users_in_room:
            first_name = (users[0].split())[0]
            if first_name in user_names:
                already_exists = False
                for same_first_name in user_names[first_name]:
                    if same_first_name[1] == users[1]:
                        already_exists = True
                        break
                if not already_exists:
                    user_names[first_name].append(users)
            else:
                user_names[first_name].append(users)

    with open('suggested_users.json', 'w') as fp:
        json.dump(user_names, fp, sort_keys=True, indent=4) 


load_users_and_groups()