import requests
import json
import speechtest as speech
from Tkinter import StringVar

with open('developer_tokens.json') as data:
    developer_tokens = json.load(data)

with open('suggested_users.json') as sugg:
    sugg_users = json.load(sugg)

def check_suggested_members_voice(member_name, text):
    if member_name in sugg_users:
        if (len(sugg_users[member_name])>1):
            did_you_mean = "Select which user you want by number:"
            speech.speech_play_test(did_you_mean)
            count =1
            output = did_you_mean + "\n"
            for suggested_member in sugg_users[member_name]:
                output += count + ": "+ suggested_member[0] + "\n"
                output += "   " + suggested_member[1] + "\n"
            return sugg_users[member_name][num-1][1]
        else:
            return sugg_users[member_name][0][1]
    else:
        return 0


def find_members_voice(user, member_input, text):
    finding_members = "Finding members"
    speech.speech_play_test(finding_members)
    final_member_list = []
    legit_token = "Bearer " + developer_tokens[user]
    search_url = "https://api.ciscospark.com/v1/people"
    for member in member_input:
        headers = {
            'Authorization': legit_token
        }
        params = {
            'displayName': member
        }
        matching_members = requests.get(search_url, headers=headers, params=params).json()
        if len(matching_members['items']) == 0:
            no_members = "No matching members for " + member
            speech.speech_play_test(member)
        elif len(matching_members['items']) == 1:
            final_member_list.append(matching_members['items'][0]['email'])
        elif len(matching_members['items']) > 5:
            found_member = check_suggested_members_voice((member.split())[0], text)
            if found_member == 0:
                specify_member = "Please specify " + member + "a bit more"
                speech.speech_play_test(member)
            else:
                final_member_list.append(found_member)
        else:
            for matched_member in matching_members['items']:
                print count + ": "+ matched_member
            num = raw_input("Respond with a number: ")
    return final_member_list